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

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy
from django.db import models
from django.forms import ModelForm
from django.forms import ModelChoiceField

from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from wger.manager.models import Schedule
from wger.manager.models import ScheduleStep
from wger.manager.models import Workout

from wger.utils.generic_views import WgerFormMixin
from wger.utils.generic_views import WgerDeleteMixin
from wger.utils.generic_views import WgerPermissionMixin


logger = logging.getLogger('wger.custom')


class StepCreateView(WgerFormMixin, CreateView, WgerPermissionMixin):
    '''
    Creates a new workout schedule
    '''

    model = ScheduleStep
    title = ugettext_lazy('Add workout')
    login_required = True

    def get_form_class(self):
        '''
        The form can only show the workouts belonging to the user.

        This is defined here because only at this point during the request
        have we access to the current user
        '''

        class StepForm(ModelForm):
            workout = ModelChoiceField(queryset=Workout.objects.filter(user=self.request.user))

            class Meta:
                model = ScheduleStep

        return StepForm

    def get_context_data(self, **kwargs):
        context = super(StepCreateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('step-add',
                                         kwargs={'schedule_pk': self.kwargs['schedule_pk']})
        return context

    def get_success_url(self):
        return reverse('schedule-view', kwargs={'pk': self.kwargs['schedule_pk']})

    def form_valid(self, form):
        '''Set the schedule and the order'''

        schedule = Schedule.objects.get(pk=self.kwargs['schedule_pk'])

        max_order = schedule.schedulestep_set.all().aggregate(models.Max('order'))
        form.instance.schedule = schedule
        form.instance.order = (max_order['order__max'] or 0) + 1
        return super(StepCreateView, self).form_valid(form)


class StepEditView(WgerFormMixin, UpdateView, WgerPermissionMixin):
    '''
    Generic view to update an existing schedule step
    '''

    model = ScheduleStep
    title = ugettext_lazy('Edit workout')
    form_action_urlname = 'step-edit'
    login_required = True

    def get_form_class(self):
        '''
        The form can only show the workouts belonging to the user.

        This is defined here because only at this point during the request
        have we access to the current user
        '''

        class StepForm(ModelForm):
            workout = ModelChoiceField(queryset=Workout.objects.filter(user=self.request.user))

            class Meta:
                model = ScheduleStep

        return StepForm

    def get_success_url(self):
        return reverse('schedule-view', kwargs={'pk': self.object.schedule_id})


class StepDeleteView(WgerDeleteMixin, DeleteView, WgerPermissionMixin):
    '''
    Generic view to delete a schedule step
    '''

    model = ScheduleStep
    title = ugettext_lazy('Delete workout')
    form_action_urlname = 'step-delete'
    messages = ugettext_lazy('Workout was successfully deleted')
    login_required = True

    def get_success_url(self):
        return reverse('schedule-view', kwargs={'pk': self.object.schedule.id})
