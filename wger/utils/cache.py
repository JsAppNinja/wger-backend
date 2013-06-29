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


import hashlib
from django.core.cache import cache
from django.utils.encoding import force_bytes


def delete_template_fragment_cache(fragment_name='', *args):

    key = u':'.join([str(arg) for arg in args])
    key_name = hashlib.md5(force_bytes(key)).hexdigest()
    cache.delete('template.cache.{0}.{1}'.format(fragment_name, key_name))


class CacheKeyMapper(object):
    '''
    Simple class for mapping the cache keys of different objects
    '''

    # Keys used by the cache
    LANGUAGE_CACHE_KEY = 'language-{0}'
    EXERCISE_CACHE_KEY = 'exercise-{0}'
    EXERCISE_CACHE_KEY_MUSCLE_BG = 'exercise-muscle-bg-{0}'
    INGREDIENT_CACHE_KEY = 'ingredient-{0}'

    def get_exercise_key(self, param):
        '''
        Return the exercise cache key
        '''
        if type(param) == int:
            pk = param
        else:
            pk = param.pk

        return self.EXERCISE_CACHE_KEY.format(pk)

    def get_exercise_muscle_bg_key(self, param):
        '''
        Return the exercise muscle background cache key
        '''
        if type(param) == int:
            pk = param
        else:
            pk = param.pk

        return self.EXERCISE_CACHE_KEY_MUSCLE_BG.format(pk)

    def get_language_key(self, param):
        '''
        Return the language cache key
        '''
        if type(param) in (str, unicode):
            pk = param
        else:
            pk = param.short_name

        return self.LANGUAGE_CACHE_KEY.format(pk)

    def get_ingredient_key(self, param):
        '''
        Return the ingredient cache key
        '''
        if type(param) == int:
            pk = param
        else:
            pk = param.pk

        return self.INGREDIENT_CACHE_KEY.format(pk)


cache_mapper = CacheKeyMapper()
