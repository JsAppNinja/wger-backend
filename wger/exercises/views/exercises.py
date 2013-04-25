# -*- coding: utf-8 -*-

# This file is part of Workout Manager.
#
# Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
import logging
import json
import uuid

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from django.forms import ModelForm
from django.forms import ModelChoiceField
from django.core import mail
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import CreateView
from django.views.generic import UpdateView

from wger.manager.models import WorkoutLog

from wger.exercises.models import Exercise
from wger.exercises.models import ExerciseComment
from wger.exercises.models import ExerciseCategory
from wger.exercises.models import Muscle

from wger.utils.generic_views import YamlFormMixin
from wger.utils.generic_views import YamlDeleteMixin
from wger.utils.language import load_language


logger = logging.getLogger('workout_manager.custom')


def overview(request):
    '''
    Overview with all exercises
    '''
    language = load_language()

    template_data = {}
    template_data.update(csrf(request))

    categories = (ExerciseCategory.objects.filter(language=language.id)
                                          .filter(exercise__status__in=Exercise.EXERCISE_STATUS_OK)
                                          .distinct())

    template_data['categories'] = categories
    return render_to_response('overview.html',
                              template_data,
                              context_instance=RequestContext(request))


def view(request, id, slug=None):
    '''
    Detail view for an exercise
    '''

    template_data = {}
    template_data['comment_edit'] = False

    # Load the exercise itself
    exercise = get_object_or_404(Exercise, pk=id)
    template_data['exercise'] = exercise

    # Create the backgrounds that show what muscles the exercise works on
    backgrounds_back = []
    backgrounds_front = []

    for muscle in exercise.muscles.all():
        if muscle.is_front:
            backgrounds_front.append('images/muscles/main/muscle-%s.svg' % muscle.id)
        else:
            backgrounds_back.append('images/muscles/main/muscle-%s.svg' % muscle.id)

    for muscle in exercise.muscles_secondary.all():
        if muscle.is_front:
            backgrounds_front.append('images/muscles/secondary/muscle-%s.svg' % muscle.id)
        else:
            backgrounds_back.append('images/muscles/secondary/muscle-%s.svg' % muscle.id)

    # Append the "main" background, with the silhouette of the human body
    # This has to happen as the last step, so it is rendered behind the muscles.
    backgrounds_front.append('images/muscles/muscular_system_front.svg')
    backgrounds_back.append('images/muscles/muscular_system_back.svg')

    template_data['muscle_backgrounds_front'] = backgrounds_front
    template_data['muscle_backgrounds_back'] = backgrounds_back

    # If the user is logged in, load the log and prepare the entries for
    # rendering in the D3 chart
    entry_log = []
    chart_data = []
    if request.user.is_authenticated():
        entry = WorkoutLog()
        logs = WorkoutLog.objects.filter(user=request.user, exercise=exercise)
        entry_log, chart_data = entry.process_log_entries(logs)

    template_data['logs'] = entry_log
    template_data['json'] = chart_data
    template_data['svg_uuid'] = str(uuid.uuid4())
    template_data['reps'] = _("Reps")

    # Render
    return render_to_response('view.html',
                              template_data,
                              context_instance=RequestContext(request))


class ExercisesEditAddView(YamlFormMixin):
    '''
    Generic view to subclass from for exercise adding and editing, since they
    share all this settings
    '''
    model = Exercise
    sidebar = 'exercise/form.html'

    form_fields = ['name',
                   'category',
                   'muscles',
                   'muscles_secondary',
                   'description']

    title = ugettext_lazy('Add exercise')
    custom_js = 'init_tinymce();'
    clean_html = ('description', )

    def get_form_class(self):

        # Define the exercise form here because only at this point during the request
        # have we access to the currently used language. In other places Django defaults
        # to 'en-us'.
        class ExerciseForm(ModelForm):
            language = load_language()
            category = ModelChoiceField(queryset=ExerciseCategory.objects.filter(
                                        language=language.id))

            class Meta:
                model = Exercise

            class Media:
                js = ('js/tinymce/tiny_mce.js',)

        return ExerciseForm


class ExerciseUpdateView(ExercisesEditAddView, UpdateView):
    '''
    Generic view to update an existing exercise
    '''

    def get_context_data(self, **kwargs):
        context = super(ExerciseUpdateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('exercise-edit', kwargs={'pk': self.object.id})
        context['title'] = _('Edit %s') % self.object.name

        return context


class ExerciseAddView(ExercisesEditAddView, CreateView):
    '''
    Generic view to add a new exercise
    '''

    form_action = reverse_lazy('exercise-add')

    def form_valid(self, form):
        '''
        Set the user that submitted the exercise
        '''

        # set the submitter, if admin, set approrpiate status
        form.instance.user = self.request.user
        if self.request.user.has_perm('exercises.add_exercise'):
            form.instance.status = Exercise.EXERCISE_STATUS_ADMIN
        else:
            subject = _('New user submitted exercise')
            message = _('''The user {0} submitted a new exercise "{1}".'''.format(
                        self.request.user.username, form.instance.name))
            mail.mail_admins(_('New user submitted exercise'),
                             message,
                             fail_silently=True)

        return super(ExerciseAddView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        '''
        Demo users can't submit exercises
        '''
        if request.user.get_profile().is_temporary:
            return HttpResponseForbidden()

        return super(ExerciseAddView, self).dispatch(request, *args, **kwargs)


class ExerciseDeleteView(YamlDeleteMixin, DeleteView):
    '''
    Generic view to delete an existing exercise
    '''

    model = Exercise
    success_url = reverse_lazy('wger.exercises.views.exercises.overview')
    delete_message = ugettext_lazy('This will delete the exercise from all workouts.')
    messages = ugettext_lazy('Exercise successfully deleted')

    # Send some additional data to the template
    def get_context_data(self, **kwargs):
        context = super(ExerciseDeleteView, self).get_context_data(**kwargs)

        context['title'] = _('Delete exercise %s?') % self.object.name
        context['form_action'] = reverse('exercise-delete', kwargs={'pk': self.kwargs['pk']})

        return context


class PendingExerciseListView(ListView):
    '''
    Generic view to list all weight units
    '''

    model = Exercise
    template_name = 'exercise/pending.html'
    context_object_name = 'exercise_list'

    def get_queryset(self):
        '''
        Only show pending exercises
        '''
        return Exercise.objects.filter(status=Exercise.EXERCISE_STATUS_PENDING)


@permission_required('exercise.add_exercise')
def accept(request, pk):
    '''
    Accepts a pending user submitted exercise and emails the user, if possible
    '''
    exercise = get_object_or_404(Exercise, pk=pk)
    exercise.status = Exercise.EXERCISE_STATUS_ACCEPTED
    exercise.save()
    exercise.send_email(request)
    messages.success(request, _('Exercise was sucessfully added to the general database'))

    return HttpResponseRedirect(exercise.get_absolute_url())


@permission_required('exercise.add_exercise')
def decline(request, pk):
    '''
    Declines and deletes a pending user submitted exercise
    '''
    exercise = get_object_or_404(Exercise, pk=pk)
    exercise.status = Exercise.EXERCISE_STATUS_DECLINED
    exercise.save()
    messages.success(request, _('Exercise was sucessfully marked as rejected'))
    return HttpResponseRedirect(exercise.get_absolute_url())


def search(request):
    '''
    Search an exercise, return the result as a JSON list
    '''

    # Perform the search
    q = request.GET.get('term', '')
    user_language = load_language()
    exercises = (Exercise.objects.filter(name__icontains=q)
                                 .filter(category__language_id=user_language)
                                 .filter(status__in=Exercise.EXERCISE_STATUS_OK)
                                 .order_by('category__name', 'name')
                                 .distinct())

    # AJAX-request, this comes from the autocompleter. Create a list and send
    # it back as JSON
    if request.is_ajax():

        results = []
        for exercise in exercises:
            exercise_json = {}
            exercise_json['id'] = exercise.id
            exercise_json['name'] = exercise.name
            exercise_json['value'] = exercise.name
            exercise_json['category'] = exercise.category.name

            results.append(exercise_json)
        data = json.dumps(results)

        # Return the results to the server
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

    # Usual search (perhaps JS disabled), present the results as normal HTML page
    else:
        template_data = {}
        template_data.update(csrf(request))
        template_data['exercises'] = exercises
        template_data['search_term'] = q
        return render_to_response('exercise_search.html',
                                  template_data,
                                  context_instance=RequestContext(request))
