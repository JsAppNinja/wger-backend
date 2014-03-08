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

from wger.manager.tests.testcase import WorkoutManagerTestCase
from wger.utils.helpers import next_weekday


# TODO: parse the generated calendar files with the icalendar library


class IcalToolsTestCase(WorkoutManagerTestCase):
    '''
    Tests some tools used for iCal generation
    '''

    def test_next_weekday(self):
        '''
        Test the next weekday function
        '''
        start_date = datetime.date(2013, 12, 5)

        # Find next monday
        self.assertEqual(next_weekday(start_date, 0), datetime.date(2013, 12, 9))

        # Find next wednesday
        self.assertEqual(next_weekday(start_date, 2), datetime.date(2013, 12, 11))

        # Find next saturday
        self.assertEqual(next_weekday(start_date, 5), datetime.date(2013, 12, 7))


class WorkoutICalExportTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting the ical file for a workout
    '''

    def export_ical(self, fail=False):
        '''
        Helper function
        '''

        response = self.client.get(reverse('workout-ical', kwargs={'pk': 3}))

        if fail:
            self.assertIn(response.status_code, (404, 302))
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'text/calendar')
            self.assertEqual(response['Content-Disposition'],
                             'attachment; filename=Calendar-workout-3.ics')

            # Approximate size
            self.assertGreater(len(response.content), 540)
            self.assertLess(len(response.content), 560)

    def test_export_ical_anonymous(self):
        '''
        Tests exporting a workout as an ical file as an anonymous user
        '''

        self.export_ical(fail=True)

    def test_export_ical_owner(self):
        '''
        Tests exporting a workout as an ical file as the owner user
        '''

        self.user_login('test')
        self.export_ical(fail=False)

    def test_export_ical_other(self):
        '''
        Tests exporting a workout as an ical file as a logged user not owning the data
        '''

        self.user_login('admin')
        self.export_ical(fail=True)


class ScheduleICalExportTestCase(WorkoutManagerTestCase):
    '''
    Tests exporting the ical file for a scheduel
    '''

    def export_ical(self, fail=False):
        '''
        Helper function
        '''

        response = self.client.get(reverse('schedule-ical', kwargs={'pk': 2}))

        if fail:
            self.assertIn(response.status_code, (404, 302))
        else:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'text/calendar')
            self.assertEqual(response['Content-Disposition'],
                             'attachment; filename=Calendar-schedule-2.ics')

            # Approximate size
            self.assertGreater(len(response.content), 1650)
            self.assertLess(len(response.content), 1660)

    def test_export_ical_anonymous(self):
        '''
        Tests exporting a schedule as an ical file as an anonymous user
        '''

        self.export_ical(fail=True)

    def test_export_ical_owner(self):
        '''
        Tests exporting a schedule as an ical file as the owner user
        '''

        self.user_login('admin')
        self.export_ical(fail=False)

    def test_export_ical_other(self):
        '''
        Tests exporting a schedule as an ical file as a logged user not owning the data
        '''

        self.user_login('test')
        self.export_ical(fail=True)
