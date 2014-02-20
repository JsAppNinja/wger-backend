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
import datetime

from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from django.views.generic import UpdateView
from django.views.generic import CreateView
from wger.manager.forms import WorkoutSessionForm

from wger.manager.models import Workout, WorkoutSession

from wger.utils.generic_views import WgerFormMixin
from wger.utils.generic_views import WgerPermissionMixin


logger = logging.getLogger('wger.custom')

'''
Workout session
'''


class WorkoutSessionUpdateView(WgerFormMixin, UpdateView, WgerPermissionMixin):
    '''
    Generic view to edit an existing workout session entry
    '''
    model = WorkoutSession
    form_class = WorkoutSessionForm
    login_required = True

    def get_context_data(self, **kwargs):
        context = super(WorkoutSessionUpdateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('workout-session-edit', kwargs={'pk': self.object.id})
        context['title'] = _('Edit workout impression for {0}').format(self.object.date)

        return context

    def get_success_url(self):
        return reverse('workout-calendar')


class WorkoutSessionAddView(WgerFormMixin, CreateView, WgerPermissionMixin):
    '''
    Generic view to add a new workout session entry
    '''
    model = WorkoutSession
    form_class = WorkoutSessionForm
    login_required = True

    def get_date(self):
        '''
        Returns a date object from the URL parameters or None if no date
        could be created
        '''
        try:
            date = datetime.date(int(self.kwargs['year']),
                                 int(self.kwargs['month']),
                                 int(self.kwargs['day']))
        except ValueError:
            date = None

        return date

    def dispatch(self, request, *args, **kwargs):
        '''
        Check for ownership
        '''
        workout = Workout.objects.get(pk=kwargs['workout_pk'])
        if workout.get_owner_object().user != request.user:
            return HttpResponseForbidden()

        if not self.get_date():
            return HttpResponseBadRequest('You need to use a valid date')

        return super(WorkoutSessionAddView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WorkoutSessionAddView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('workout-session-add',
                                         kwargs={'workout_pk': self.kwargs['workout_pk'],
                                                 'year': self.kwargs['year'],
                                                 'month': self.kwargs['month'],
                                                 'day': self.kwargs['day']})
        context['title'] = _('New workout impression for the {0}'.format(self.get_date()))
        return context

    def get_success_url(self):
        return reverse('workout-calendar')

    def form_valid(self, form):
        '''
        Set the workout and the user
        '''

        workout = Workout.objects.get(pk=self.kwargs['workout_pk'])
        form.instance.workout = workout
        form.instance.user = self.request.user
        form.instance.date = self.get_date()
        return super(WorkoutSessionAddView, self).form_valid(form)
