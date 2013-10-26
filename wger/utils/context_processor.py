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

from django.conf import settings

from wger import get_version
from wger.utils import constants
from wger.utils.language import load_language


def processor(request):

    language = load_language()
    full_path = request.get_full_path()
    i18n_path = {}
    for lang in settings.LANGUAGES:
        i18n_path[lang[0]] = '/{0}{1}'.format(lang[0], full_path[3:])

    context = {
        # Application version
        'version': get_version(),

        # User language
        'language': language,

        # Available application languages
        'languages': settings.LANGUAGES,

        # The current path
        'request_full_path': full_path,

        # Translation links
        'i18n_path': i18n_path,

        # Translation links
        'datepicker_i18n_path': 'js/jquery.ui.datepicker-{0}.js'.format(language.short_name),

        # Flag for guest users
        'has_demo_data': request.session.get('has_demo_data', False),

        # Don't show messages on AJAX requests (they are deleted if shown)
        'no_messages': request.META.get('HTTP_X_WGER_NO_MESSAGES', False),

        # Default cache time for template fragment caching
        'cache_timeout': settings.CACHES['default']['TIMEOUT']
    }

    # Pseudo-intelligent navigation here
    if '/software/' in request.get_full_path() \
       or '/contact' in request.get_full_path():
            context['active_tab'] = constants.SOFTWARE_TAB

    elif '/exercise/' in request.get_full_path():
        context['active_tab'] = constants.EXERCISE_TAB

    elif '/nutrition/' in request.get_full_path():
        context['active_tab'] = constants.NUTRITION_TAB

    elif '/weight/' in request.get_full_path():
        context['active_tab'] = constants.WEIGHT_TAB

    elif '/workout/' in request.get_full_path():
        context['active_tab'] = constants.WORKOUT_TAB

    else:
        context['active_tab'] = constants.USER_TAB

    return context
