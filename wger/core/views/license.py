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
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.views.generic import ListView
from django.views.generic import DeleteView
from django.views.generic import CreateView
from django.views.generic import UpdateView

from wger.utils.generic_views import WgerFormMixin
from wger.utils.generic_views import WgerDeleteMixin
from wger.utils.generic_views import WgerPermissionMixin

from wger.core.models import License


logger = logging.getLogger('wger.custom')


class LicenseListView(WgerPermissionMixin, ListView):
    '''
    Overview of all available licenses
    '''
    model = License
    permission_required = 'core.add_license'
    template_name = 'license/list.html'


class LicenseAddView(WgerFormMixin, CreateView, WgerPermissionMixin):
    '''
    View to add a new license
    '''

    model = License
    success_url = reverse_lazy('core:license-list')
    title = ugettext_lazy('Add license')
    form_action = reverse_lazy('core:license-add')
    permission_required = 'core.add_license'


class LicenseUpdateView(WgerFormMixin, UpdateView, WgerPermissionMixin):
    '''
    View to update an existing license
    '''

    model = License
    title = ugettext_lazy('Edit license')
    success_url = reverse_lazy('core:license-list')
    permission_required = 'core.change_license'

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(LicenseUpdateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('core:license-edit', kwargs={'pk': self.object.id})
        context['title'] = _('Edit {0}'.format(self.object))
        return context


class LicenseDeleteView(WgerDeleteMixin, DeleteView, WgerPermissionMixin):
    '''
    View to delete an existing license
    '''

    model = License
    success_url = reverse_lazy('core:license-list')
    permission_required = 'core.delete_license'

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(LicenseDeleteView, self).get_context_data(**kwargs)
        context['title'] = _('Delete license {0}?'.format(self.object))
        context['form_action'] = reverse('core:license-delete', kwargs={'pk': self.kwargs['pk']})
        return context
