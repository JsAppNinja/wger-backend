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

import datetime

from django.core.urlresolvers import reverse

from wger.manager.models import Workout

from wger.manager.tests.testcase import WorkoutManagerTestCase
from wger.manager.tests.testcase import WorkoutManagerDeleteTestCase
from wger.manager.tests.testcase import WorkoutManagerEditTestCase
from wger.manager.tests.testcase import ApiBaseResourceTestCase


class AddWorkoutTestCase(WorkoutManagerTestCase):
    '''
    Tests adding a Workout
    '''

    def create_workout(self):
        '''
        Helper function to test creating workouts
        '''

        # Create a workout
        count_before = Workout.objects.count()
        response = self.client.get(reverse('workout-add'))
        count_after = Workout.objects.count()

        # There is always a redirect
        self.assertEqual(response.status_code, 302)

        # Test creating workout
        self.assertGreater(count_after, count_before)

        # Test accessing workout
        response = self.client.get(reverse('workout-view', kwargs={'id': 1}))

        workout = Workout.objects.get(pk=1)
        self.assertEqual(response.context['workout'], workout)
        self.assertEqual(response.status_code, 200)

    def test_create_workout_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''

        self.user_login()
        self.create_workout()
        self.user_logout()


class DeleteTestWorkoutTestCase(WorkoutManagerDeleteTestCase):
    '''
    Tests deleting a Workout
    '''

    object_class = Workout
    url = 'workout-delete'
    pk = 3
    user_success = 'test'
    user_fail = 'admin'


class EditWorkoutTestCase(WorkoutManagerEditTestCase):
    '''
    Tests editing a Workout
    '''

    object_class = Workout
    url = 'workout-edit'
    pk = 3
    user_success = 'test'
    user_fail = 'admin'
    data = {'comment': 'A new comment'}


class WorkoutOverviewTestCase(WorkoutManagerTestCase):
    '''
    Tests the workout overview
    '''

    def get_workout_overview(self):
        '''
        Helper function to test the workout overview
        '''

        response = self.client.get(reverse('workout-overview'))

        # Page exists
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['workouts']), 2)

    def test_dashboard_logged_in(self):
        '''
        Test creating a workout a logged in user
        '''
        self.user_login()
        self.get_workout_overview()


class WorkoutModelTestCase(WorkoutManagerTestCase):
    '''
    Tests other functionality from the model
    '''

    def test_unicode(self):
        '''
        Test the unicode representation
        '''

        workout = Workout()
        workout.creation_date = datetime.date.today()
        self.assertEqual(workout.__unicode__(),
                         u'{0} ({1})'.format(u'Workout', datetime.date.today()))

        workout.comment = u'my description'
        self.assertEqual(workout.__unicode__(), u'my description')


class WorkoutApiTestCase(ApiBaseResourceTestCase):
    '''
    Tests the workout overview resource
    '''
    resource = 'workout'
    resource_updatable = False


class WorkoutDetailApiTestCase(ApiBaseResourceTestCase):
    '''
    Tests accessing a specific workout
    '''
    resource = 'workout/3'
