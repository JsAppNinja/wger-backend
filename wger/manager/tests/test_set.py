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
from django.core.cache import cache

from wger.manager.models import Set
from wger.manager.models import Setting
from wger.manager.models import Day
from wger.exercises.models import Exercise

from wger.manager.tests.testcase import STATUS_CODES_FAIL
from wger.manager.tests.testcase import WorkoutManagerTestCase
from wger.manager.tests.testcase import WorkoutManagerAddTestCase
from wger.manager.tests.testcase import ApiBaseResourceTestCase
from wger.utils.cache import get_template_cache_name


logger = logging.getLogger('wger.custom')


class SetAddTestCase(WorkoutManagerAddTestCase):
    '''
    Test adding a set to a day
    '''

    object_class = Set
    url = reverse_lazy('set-add', kwargs={'day_pk': 5})
    pk = 4
    user_success = 'test'
    user_fail = 'admin'
    data = {'exercises': [1, ],
            'sets': 4,
            'exercise1-TOTAL_FORMS': 4,
            'exercise1-INITIAL_FORMS': 0,
            'exercise1-MAX_NUM_FORMS': 1000}
    data_ignore = ('exercise1-TOTAL_FORMS',
                   'exercise1-INITIAL_FORMS',
                   'exercise1-MAX_NUM_FORMS')

    def test_add_set(self, fail=False):
        '''
        Tests adding a set and corresponding settings at the same time
        '''

        # POST the data
        self.user_login('test')
        exercises_id = [1, 2]
        post_data = {'exercises': exercises_id,
                     'sets': 4,
                     'exercise1-TOTAL_FORMS': 4,
                     'exercise1-INITIAL_FORMS': 0,
                     'exercise1-MAX_NUM_FORMS': 1000,
                     'exercise1-0-reps': 10,
                     'exercise1-1-reps': 12,
                     'exercise1-2-reps': 10,
                     'exercise1-3-reps': 12,
                     'exercise2-TOTAL_FORMS': 4,
                     'exercise2-INITIAL_FORMS': 0,
                     'exercise2-MAX_NUM_FORMS': 1000,
                     'exercise2-0-reps': 8}
        response = self.client.post(reverse_lazy('set-add', kwargs={'day_pk': 5}), post_data)
        self.assertEqual(response.status_code, 302)

        set_obj = Set.objects.get(pk=4)
        exercise1 = Exercise.objects.get(pk=1)
        exercise2 = Exercise.objects.get(pk=2)

        # Check that everything got where it's supposed to
        for exercise in set_obj.exercises.all():
            self.assertIn(exercise.id, exercises_id)

        settings = Setting.objects.filter(set=set_obj)
        for setting in settings:
            if setting.exercise == exercise1:
                self.assertIn(setting.reps, (10, 12))
            else:
                self.assertEqual(setting.reps, 8)


class SetDeleteTestCase(WorkoutManagerTestCase):
    '''
    Tests deleting a set from a workout
    '''

    def delete_set(self, fail=True):
        '''
        Helper function to test deleting a set from a workout
        '''

        # Fetch the overview page
        count_before = Set.objects.count()
        response = self.client.get(reverse('wger.manager.views.set.delete', kwargs={'pk': 3}))
        count_after = Set.objects.count()

        if fail:
            self.assertIn(response.status_code, (302, 403))
            self.assertEqual(count_before, count_after)
        else:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(count_before - 1, count_after)
            self.assertRaises(Set.DoesNotExist, Set.objects.get, pk=3)

    def test_delete_set_anonymous(self):
        '''
        Tests deleting a set from a workout as an anonymous user
        '''

        self.delete_set(fail=True)

    def test_delete_set_owner(self):
        '''
        Tests deleting a set from a workout as the owner user
        '''

        self.user_login('admin')
        self.delete_set(fail=True)

    def test_delete_set_other(self):
        '''
        Tests deleting a set from a workout as a logged user not owning the data
        '''

        self.user_login('test')
        self.delete_set(fail=False)


class TestSetOrderTestCase(WorkoutManagerTestCase):
    '''
    Tests that the order of the (existing) sets in a workout is preservead
    when adding new ones
    '''

    def add_set(self, exercises_id):
        '''
        Helper function that adds a set to a day
        '''
        nr_sets = 4
        post_data = {'exercises': exercises_id, 'sets': nr_sets}
        for exercise_id in exercises_id:
            post_data['exercise{0}-TOTAL_FORMS'.format(exercise_id)] = nr_sets
            post_data['exercise{0}-INITIAL_FORMS'.format(exercise_id)] = 0
            post_data['exercise{0}-MAX_NUM_FORMS'.format(exercise_id)] = 1000

        response = self.client.post(reverse('set-add', kwargs={'day_pk': 5}),
                                    post_data)

        return response

    def get_order(self):
        '''
        Helper function that reads the order of the the sets in a day
        '''

        day = Day.objects.get(pk=5)
        order = ()

        for day_set in day.set_set.select_related():
            order += (day_set.id,)

        return order

    def test_set_order(self, logged_in=False):
        '''
        Helper function to test creating workouts
        '''

        # Add some sets and check the order
        self.user_login('test')
        orig = self.get_order()
        exercises = (1, 2, 3, 81, 84, 91, 111)

        for i in range(0, 7):
            self.add_set([exercises[i]])
            prev = self.get_order()
            orig += (i + 4,)
            self.assertEqual(orig, prev)


class TestSetAddFormset(WorkoutManagerTestCase):
    '''
    Tests the functionality of the formset mini-view that is used in the add
    set page
    '''

    def get_formset(self):
        '''
        Helper function
        '''
        exercise = Exercise.objects.get(pk=1)
        response = self.client.get(reverse('set-get-formset',
                                   kwargs={'exercise_pk': 1, 'reps': 4}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['exercise'], exercise)
        self.assertTrue(response.context['formset'])

    def test_get_formset_logged_in(self):
        '''
        Tests the formset view as an authorized user
        '''

        self.user_login('test')
        self.get_formset()


class SetEditEditTestCase(WorkoutManagerTestCase):
    '''
    Tests editing a set
    '''

    def edit_set(self, fail=False):
        '''
        Helper function
        '''

        # Fetch the edit page
        response = self.client.get(reverse('set-edit', kwargs={'pk': 3}))
        entry_before = Set.objects.get(pk=3)

        if fail:
            self.assertIn(response.status_code, STATUS_CODES_FAIL)
        else:
            self.assertEqual(response.status_code, 200)

        # Try to edit the object
        response = self.client.post(reverse('set-edit', kwargs={'pk': 3}),
                                    {'exercise2-TOTAL_FORMS': 4,
                                     'exercise2-INITIAL_FORMS': 1,
                                     'exercise2-MAX_NUM_FORMS': 1000,
                                     'exercise2-0-reps': 5,
                                     'exercise2-0-id': 3,
                                     'exercise2-0-DELETE': False,
                                     'exercise2-1-reps': 13,
                                     'exercise2-1-id': '',
                                     'exercise2-1-DELETE': False})

        entry_after = Set.objects.get(pk=3)

        # Check the results
        if fail:
            self.assertIn(response.status_code, STATUS_CODES_FAIL)
            self.assertEqual(entry_before, entry_after)

        else:
            self.assertEqual(response.status_code, 302)

            # The page we are redirected to doesn't trigger an error
            response = self.client.get(response['Location'])
            self.assertEqual(response.status_code, 200)

            # Settings were updated and a new one created
            setting = Setting.objects.get(pk=3)
            self.assertEqual(setting.reps, 5)

            setting = Setting.objects.get(pk=4)
            self.assertEqual(setting.reps, 13)

        self.post_test_hook()

    def test_edit_set_authorized(self):
        '''
        Tests editing the object as an authorized user
        '''

        self.user_login('admin')
        self.edit_set(fail=True)

    def test_edit_set_other(self):
        '''
        Tests editing the object as an unauthorized, logged in user
        '''

        self.user_login('test')
        self.edit_set(fail=False)


class WorkoutCacheTestCase(WorkoutManagerTestCase):
    '''
    Workout cache test case
    '''

    def test_workout_view_set(self):
        '''
        Test the workout view cache is correctly generated on visit
        '''

        self.user_login('admin')
        self.client.get(reverse('wger.manager.views.workout.view', kwargs={'id': 1}))

        # Edit a set
        set1 = Set.objects.get(pk=1)
        set1.order = 99
        set1.save()
        self.assertFalse(cache.get(get_template_cache_name('day-view', 1)))
        self.assertTrue(cache.get(get_template_cache_name('day-view', 2)))

        set1.delete()
        self.assertFalse(cache.get(get_template_cache_name('day-view', 1)))
        self.assertTrue(cache.get(get_template_cache_name('day-view', 2)))

    def test_workout_view_setting(self):
        '''
        Test the workout view cache is correctly generated on visit
        '''

        self.user_login('admin')
        self.client.get(reverse('wger.manager.views.workout.view', kwargs={'id': 1}))

        # Edit a setting
        setting1 = Setting.objects.get(pk=1)
        setting1.reps = 20
        setting1.save()
        self.assertFalse(cache.get(get_template_cache_name('day-view', 1)))
        self.assertTrue(cache.get(get_template_cache_name('day-view', 2)))

        setting1.delete()
        self.assertFalse(cache.get(get_template_cache_name('day-view', 1)))
        self.assertTrue(cache.get(get_template_cache_name('day-view', 2)))


class SetpiTestCase(ApiBaseResourceTestCase):
    '''
    Tests the set overview resource
    '''
    resource = 'set'
    resource_updatable = False


class SetDetailApiTestCase(ApiBaseResourceTestCase):
    '''
    Tests accessing a specific set
    '''
    resource = 'set/3'
