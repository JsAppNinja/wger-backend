# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy
from django.utils import translation
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as Django_User, User
from django.contrib.auth.views import login as django_loginview
from django.contrib import messages
from django.views.generic import RedirectView, UpdateView, DetailView
from django.conf import settings
from rest_framework.authtoken.models import Token

from wger.utils.constants import USER_TAB
from wger.utils.generic_views import WgerPermissionMixin
from wger.utils.generic_views import WgerFormMixin
from wger.utils.user_agents import check_request_amazon
from wger.utils.user_agents import check_request_android
from wger.core.forms import UserPreferencesForm, UserPersonalInformationForm
from wger.core.forms import PasswordConfirmationForm
from wger.core.forms import RegistrationForm
from wger.core.forms import RegistrationFormNoCaptcha
from wger.core.models import Language
from wger.manager.models import WorkoutLog
from wger.manager.models import WorkoutSession
from wger.manager.models import Workout
from wger.nutrition.models import NutritionPlan
from wger.config.models import GymConfig
from wger.weight.models import WeightEntry
from wger.gym.models import AdminUserNote, GymUserConfig

logger = logging.getLogger(__name__)


def login(request):
    '''
    Small wrapper around the django login view
    '''

    context = {'hide_persona': check_request_amazon(request) or check_request_android(request),
               'active_tab': USER_TAB}
    if request.REQUEST.get('next'):
        context['next'] = request.REQUEST.get('next')

    return django_loginview(request,
                            template_name='user/login.html',
                            extra_context=context)


@login_required()
def delete(request, user_pk=None):
    '''
    Delete a user account and all his data, requires password confirmation first

    If no user_pk is present, the user visiting the URL will be deleted, otherwise
    a gym administrator is deleting a different user
    '''

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
        form_action = reverse('core:user:delete', kwargs={'user_pk': user_pk})

        # Forbidden if the user has not enough rights, doesn't belong to the
        # gym or is an admin as well
        if (not request.user.has_perm('gym.manage_gym')
                or request.user.userprofile.gym_id != user.userprofile.gym_id
                or user.has_perm('gym.manage_gym')
                or user.has_perm('gym.gym_trainer')
                or user.has_perm('gym.manage_gyms')):
            return HttpResponseForbidden()
    else:
        user = request.user
        form_action = reverse('core:user:delete')

    form = PasswordConfirmationForm(user=request.user)

    if request.method == 'POST':
        form = PasswordConfirmationForm(data=request.POST, user=request.user)
        if form.is_valid():

            user.delete()
            messages.success(request,
                             _('Account "{0}" was successfully deleted').format(user.username))

            if not user_pk:
                django_logout(request)
                return HttpResponseRedirect(reverse('software:features'))
            else:
                gym_pk = request.user.userprofile.gym_id
                return HttpResponseRedirect(reverse('gym:gym:user-list', kwargs={'pk': gym_pk}))
    context = {'form': form,
               'user_delete': user,
               'form_action': form_action}

    return render(request, 'user/delete_account.html', context)


@login_required()
def trainer_login(request, user_pk):
    '''
    Allows a trainer to 'log in' as the selected user
    '''
    user = get_object_or_404(User, pk=user_pk)
    orig_user_pk = request.user.pk

    # Changing only between the same gym
    if request.user.userprofile.gym != user.userprofile.gym:
        return HttpResponseForbidden()

    # No changing if identity is not set
    if not request.user.has_perm('gym.gym_trainer') \
            and not request.session.get('trainer.identity'):
        return HttpResponseForbidden()

    # Changing between trainers or managers is not allowed
    if request.user.has_perm('gym.gym_trainer') \
            and (user.has_perm('gym.gym_trainer')
                 or user.has_perm('gym.manage_gym')
                 or user.has_perm('gym.manage_gyms')):
        return HttpResponseForbidden()

    # Check if we're switching back to our original account
    own = False
    if (user.has_perm('gym.gym_trainer')
            or user.has_perm('gym.manage_gym')
            or user.has_perm('gym.manage_gyms')):
        own = True

    # Note: it seems we have to manually set the authentication backend here
    # - https://docs.djangoproject.com/en/1.6/topics/auth/default/#auth-web-requests
    # - http://stackoverflow.com/questions/3807777/django-login-without-authenticating
    if own:
        del(request.session['trainer.identity'])
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    django_login(request, user)

    if not own:
        request.session['trainer.identity'] = orig_user_pk
        if request.GET.get('next'):
            return HttpResponseRedirect(request.GET['next'])
        else:
            return HttpResponseRedirect(reverse('core:index'))
    else:
        return HttpResponseRedirect(reverse('gym:gym:user-list',
                                            kwargs={'pk': user.userprofile.gym_id}))


def logout(request):
    '''
    Logout the user. For temporary users, delete them.
    '''
    user = request.user
    django_logout(request)
    if user.is_authenticated() and user.userprofile.is_temporary:
        user.delete()
    return HttpResponseRedirect(reverse('core:user:login'))


def registration(request):
    '''
    A form to allow for registration of new users
    '''
    template_data = {}
    template_data.update(csrf(request))

    # Don't use captcha when registering through an app
    is_app = check_request_amazon(request) or check_request_android(request)
    FormClass = RegistrationFormNoCaptcha if is_app else RegistrationForm

    # Don't show captcha if the global parameter is false
    if not settings.WGER_SETTINGS['USE_RECAPTCHA']:
        FormClass = RegistrationFormNoCaptcha

    # Redirect regular users, in case they reached the registration page
    if request.user.is_authenticated() and not request.user.userprofile.is_temporary:
        return HttpResponseRedirect(reverse('core:dashboard'))

    if request.method == 'POST':
        form = FormClass(data=request.POST)

        # If the data is valid, log in and redirect
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = Django_User.objects.create_user(username,
                                                   email,
                                                   password)
            user.save()

            # Pre-set some values of the user's profile
            language = Language.objects.get(short_name=translation.get_language())
            user.userprofile.notification_language = language

            # Set default gym, if needed
            gym_config = GymConfig.objects.get(pk=1)
            if gym_config.default_gym:
                user.userprofile.gym = gym_config.default_gym

                # Create gym user configuration object
                config = GymUserConfig()
                config.gym = gym_config.default_gym
                config.user = user
                config.save()

            user.userprofile.save()

            user = authenticate(username=username, password=password)
            django_login(request, user)
            messages.success(request, _('You were successfully registered'))
            return HttpResponseRedirect(reverse('core:dashboard'))
    else:
        form = FormClass()

    template_data['form'] = form
    template_data['title'] = _('Register')
    template_data['form_fields'] = [i for i in form]
    template_data['form_action'] = reverse('core:user:registration')
    template_data['submit_text'] = _('Register')
    template_data['extend_template'] = 'base.html'

    return render(request, 'form.html', template_data)


@login_required
def preferences(request):
    '''
    An overview of all user preferences
    '''
    template_data = {}
    template_data.update(csrf(request))
    redirect = False

    # Process the preferences form
    if request.method == 'POST':

        form = UserPreferencesForm(data=request.POST, instance=request.user.userprofile)
        form.user = request.user

        # Save the data if it validates
        if form.is_valid():
            form.save()
            redirect = True
    else:
        form = UserPreferencesForm(instance=request.user.userprofile)

    # Process the email form
    if request.method == 'POST':
        email_form = UserPersonalInformationForm(data=request.POST, instance=request.user)

        if email_form.is_valid() and redirect:
            email_form.save()
            redirect = True
        else:
            redirect = False
    else:
        email_form = UserPersonalInformationForm(instance=request.user)

    template_data['form'] = form
    template_data['email_form'] = email_form

    if redirect:
        messages.success(request, _('Settings successfully updated'))
        return HttpResponseRedirect(reverse('core:user:preferences'))
    else:
        return render(request, 'user/preferences.html', template_data)


class UserDeactivateView(WgerPermissionMixin, RedirectView):
    '''
    Deactivates a user
    '''
    permanent = False
    model = User
    permission_required = ('gym.manage_gym', 'gym.gym_trainer')

    def dispatch(self, request, *args, **kwargs):
        '''
        Only managers and trainers for this gym can access the members
        '''
        edit_user = get_object_or_404(User, pk=self.kwargs['pk'])
        if (request.user.has_perm('gym.manage_gym') or request.user.has_perm('gym.gym_trainer')
                and request.user.userprofile.gym_id == edit_user.userprofile.gym_id):
            return super(UserDeactivateView, self).dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_redirect_url(self, pk):
        edit_user = get_object_or_404(User, pk=pk)
        edit_user.is_active = False
        edit_user.save()
        messages.success(self.request, _('The user was successfully deactivated'))
        return reverse('core:user:overview', kwargs=({'pk': pk}))


class UserActivateView(WgerPermissionMixin, RedirectView):
    '''
    Activates a previously deactivated user
    '''
    permanent = False
    model = User
    permission_required = ('gym.manage_gym', 'gym.gym_trainer')

    def dispatch(self, request, *args, **kwargs):
        '''
        Only managers and trainers for this gym can access the members
        '''
        edit_user = get_object_or_404(User, pk=self.kwargs['pk'])
        if (request.user.has_perm('gym.manage_gym') or request.user.has_perm('gym.gym_trainer')
                and request.user.userprofile.gym_id == edit_user.userprofile.gym_id):
            return super(UserActivateView, self).dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_redirect_url(self, pk):
        edit_user = get_object_or_404(User, pk=pk)
        edit_user.is_active = True
        edit_user.save()
        messages.success(self.request, _('The user was successfully activated'))
        return reverse('core:user:overview', kwargs=({'pk': pk}))


class UserEditView(WgerFormMixin, UpdateView):
    '''
    View to update the personal information of an user by an admin
    '''

    model = User
    title = ugettext_lazy('Edit user')
    permission_required = 'gym.manage_gym'
    form_class = UserPersonalInformationForm

    def dispatch(self, request, *args, **kwargs):
        '''
        Only managers and trainers for this gym can access the members
        '''
        if request.user.is_authenticated() \
                and request.user.userprofile.gym == self.get_object().userprofile.gym:
            return super(UserEditView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('core:user:overview', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(UserEditView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('core:user:edit', kwargs={'pk': self.object.id})
        context['title'] = _('Edit {0}'.format(self.object))
        return context


@login_required
def api_key(request):
    '''
    Allows the user to generate an API key for the REST API
    '''

    context = {}
    context.update(csrf(request))

    try:
        token = Token.objects.get(user=request.user)
    except Token.DoesNotExist:
        token = False
    if request.GET.get('new_key'):
        if token:
            token.delete()

        token = Token.objects.create(user=request.user)

        # Redirect to get rid of the GET parameter
        return HttpResponseRedirect(reverse('core:user:api-key'))

    context['token'] = token

    return render(request, 'user/api_key.html', context)


class UserDetailView(WgerPermissionMixin, DetailView):
    '''
    User overview for gyms
    '''
    model = User
    permission_required = ('gym.manage_gym', 'gym.gym_trainer')
    template_name = 'user/overview.html'
    context_object_name = 'current_user'

    def dispatch(self, request, *args, **kwargs):
        '''
        Only managers for this gym can access the members
        '''
        user = request.user
        if user.is_authenticated() and user.userprofile.gym == self.get_object().userprofile.gym:
            return super(UserDetailView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(UserDetailView, self).get_context_data(**kwargs)
        out = []
        workouts = Workout.objects.filter(user=self.object).all()
        for workout in workouts:
            logs = WorkoutLog.objects.filter(workout=workout)
            out.append({'workout': workout,
                        'logs': logs.dates('date', 'day').count(),
                        'last_log': logs.last()})
        context['workouts'] = out
        context['weight_entries'] = WeightEntry.objects.filter(user=self.object)\
            .order_by('-date')[:5]
        context['nutrition_plans'] = NutritionPlan.objects.filter(user=self.object)\
            .order_by('-creation_date')[:5]
        context['session'] = WorkoutSession.objects.filter(user=self.object).order_by('-date')[:10]
        context['admin_notes'] = AdminUserNote.objects.filter(member=self.object)[:5]
        return context
