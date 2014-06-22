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

from django.db import models
from south.modelsinspector import add_introspection_rules

from wger.utils.widgets import Html5FormDateField
from wger.utils.widgets import Html5FormTimeField

logger = logging.getLogger('wger.custom')

#
#
# Please note: it is necessary to import these fields with these names,
# otherwise migrating from older versions will not work. Only if the migrations
# are squashed one day (perhaps with django 1.7), can the imports be removed.
#
#
from django.db.models import DecimalField as Html5DecimalField
from django.db.models import FloatField as Html5FloatField
from django.db.models import IntegerField as Html5IntegerField


class Html5TimeField(models.TimeField):
    '''
    Custom Time field that uses the Html5TimeInput widget
    '''

    def formfield(self, **kwargs):
        '''
        Use our custom field
        '''
        defaults = {'form_class': Html5FormTimeField}
        defaults.update(kwargs)
        return super(Html5TimeField, self).formfield(**defaults)


class Html5DateField(models.DateField):
    '''
    Custom Time field that uses the Html5DateInput widget
    '''

    def formfield(self, **kwargs):
        '''
        Use our custom field
        '''
        defaults = {'form_class': Html5FormDateField}
        defaults.update(kwargs)
        return super(Html5DateField, self).formfield(**defaults)


#
# Add instrospection rules so south can still work with these fields
#
add_introspection_rules([], ["^wger\.utils\.fields\.Html5TimeField"])
add_introspection_rules([], ["^wger\.utils\.fields\.Html5DateField"])
