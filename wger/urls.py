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
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.

from tastypie.api import Api

from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import patterns

from wger.exercises.sitemap import ExercisesSitemap
from wger.exercises.api import resources as exercises_api
from wger.nutrition.sitemap import NutritionSitemap
from wger.nutrition.api import resources as nutrition_api
from wger.utils.generic_views import TextTemplateView
from wger.utils.generic_views import WebappManifestView
from wger.manager.api import resources as manager_api
from wger.core.api import resources as core_api
from wger.weight.api import resources as weight_api

#
# REST API
#
v1_api = Api(api_name='v1')

# Exercises app
v1_api.register(exercises_api.ExerciseCategoryResource())
v1_api.register(exercises_api.ExerciseCommentResource())
v1_api.register(exercises_api.ExerciseImageResource())
v1_api.register(exercises_api.ExerciseResource())
v1_api.register(exercises_api.MuscleResource())
v1_api.register(exercises_api.EquipmentResource())

# Nutrition app
v1_api.register(nutrition_api.IngredientResource())
v1_api.register(nutrition_api.WeightUnitResource())
v1_api.register(nutrition_api.NutritionPlanResource())
v1_api.register(nutrition_api.MealResource())
v1_api.register(nutrition_api.MealItemResource())
v1_api.register(nutrition_api.IngredientToWeightUnit())

# Manager app
v1_api.register(manager_api.WorkoutResource())
v1_api.register(manager_api.ScheduleResource())
v1_api.register(manager_api.ScheduleStepResource())
v1_api.register(manager_api.DayResource())
v1_api.register(manager_api.SetResource())
v1_api.register(manager_api.SettingResource())
v1_api.register(manager_api.WorkoutLogResource())
v1_api.register(manager_api.WorkoutSessionResource())

# Weight app
v1_api.register(weight_api.WeightEntryResource())


# Core app
v1_api.register(core_api.LanguageResource())
v1_api.register(core_api.DaysOfWeekResource())
v1_api.register(core_api.UserProfileResource())
v1_api.register(core_api.LicenseResource())


from django.contrib import admin
admin.autodiscover()

#
# Sitemaps
#
sitemaps = {'exercises': ExercisesSitemap,
            'nutrition': NutritionSitemap}


#
# The actual URLs
#
urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('wger.core.urls', namespace='core', app_name='core')),
    url(r'^', include('wger.manager.urls')),
    url(r'exercise/', include('wger.exercises.urls')),
    url(r'weight/', include('wger.weight.urls')),
    url(r'nutrition/', include('wger.nutrition.urls')),
    url(r'software/', include('wger.software.urls', namespace='software', app_name='software')),
    url(r'config/', include('wger.config.urls', namespace='config', app_name='config')),
    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^sitemap\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': sitemaps},
        name='sitemap')
)

# Send these static files without any language prefix
urlpatterns = urlpatterns + patterns('',
    url(r'^robots\.txt$',
        TextTemplateView.as_view(template_name="robots.txt"),
        name='robots'),
    url(r'^manifest\.webapp$',
        WebappManifestView.as_view(template_name="manifest.webapp"),
       ),url(r'^amazon-manifest\.webapp$',
        WebappManifestView.as_view(template_name="amazon-manifest.webapp"),
       ),
   (r'^api/', include(v1_api.urls)),
)
