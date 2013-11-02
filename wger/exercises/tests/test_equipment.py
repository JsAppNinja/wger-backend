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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from django.core.urlresolvers import reverse

from wger.exercises.models import Equipment

from wger.manager.tests.testcase import WorkoutManagerTestCase
from wger.manager.tests.testcase import WorkoutManagerDeleteTestCase
from wger.manager.tests.testcase import WorkoutManagerEditTestCase
from wger.manager.tests.testcase import WorkoutManagerAddTestCase
from wger.manager.tests.testcase import ApiBaseResourceTestCase

from wger.utils.constants import PAGINATION_OBJECTS_PER_PAGE


class AddEquipmentTestCase(WorkoutManagerAddTestCase):
    '''
    Tests adding a new equipment
    '''

    object_class = Equipment
    url = 'equipment-add'
    data = {'name': 'A new equipment'}
    pk = 4


class DeleteEquipmentTestCase(WorkoutManagerDeleteTestCase):
    '''
    Tests deleting an equipment
    '''

    object_class = Equipment
    url = 'equipment-delete'
    pk = 1


class EditEquipmentTestCase(WorkoutManagerEditTestCase):
    '''
    Tests editing an equipment
    '''

    object_class = Equipment
    url = 'equipment-edit'
    pk = 1
    data = {'name': 'A new name'}


class EquipmentOverviewTestCase(WorkoutManagerTestCase):
    '''
    Tests the equipment overview page
    '''

    def test_overview(self):

        # Add more equipments so we can test the pagination
        self.user_login('admin')
        data = {"name": "A new entry"}
        for i in range(0, 50):
            self.client.post(reverse('equipment-add'), data)

        # Page exists and the pagination works
        response = self.client.get(reverse('equipment-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['equipment_list']), PAGINATION_OBJECTS_PER_PAGE)

        response = self.client.get(reverse('equipment-list'), {'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['equipment_list']), PAGINATION_OBJECTS_PER_PAGE)

        response = self.client.get(reverse('equipment-list'), {'page': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['equipment_list']), 3)

        # 'last' is a special case
        response = self.client.get(reverse('equipment-list'), {'page': 'last'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['equipment_list']), 3)

        # Page does not exist
        response = self.client.get(reverse('equipment-list'), {'page': 100})
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('equipment-list'), {'page': 'foobar'})
        self.assertEqual(response.status_code, 404)


class EquipmentApiTestCase(ApiBaseResourceTestCase):
    '''
    Tests the equipment overview resource
    '''
    resource = 'equipment'
    user = None
    resource_updatable = False


class EquipmentDetailApiTestCase(ApiBaseResourceTestCase):
    '''
    Tests accessing a specific equipment
    '''
    resource = 'equipment/1'
    user = None
    resource_updatable = False
