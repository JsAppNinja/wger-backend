from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

from manager.views import WorkoutEditView
from manager.views import WorkoutDeleteView

from manager.views import DayEditView
from manager.views import DayCreateView


urlpatterns = patterns('manager.views',

    # The index page
    url(r'^$', 'index'),
    
    # User
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
    url(r'^user/registration$', 'registration'),
    url(r'^user/preferences$', 'preferences'),
    url(r'^user/password/change$', 'change_password'),
        
    # Workout
    url(r'^workout/overview$', 'overview'),
    url(r'^workout/add$', 'add'),
    
    url(r'^workout/(?P<pk>\d+)/edit/$',
        login_required(WorkoutEditView.as_view()),
        name = 'workout-edit'),
    url(r'^workout/(?P<pk>\d+)/delete/$',
        login_required(WorkoutDeleteView.as_view()),
        name = 'workout-delete'),
    url(r'^workout/(?P<id>\d+)/view/$', 'view_workout'),
    
    
    # Days
    url(r'^workout/day/(?P<pk>\d+)/edit/$',
        login_required(DayEditView.as_view()),
        name = 'day-edit'),
    
    url(r'^workout/(?P<pk>\d+)/day/add/$',
        login_required(DayCreateView.as_view()),
        name = 'day-add'),
    
    url(r'^workout/(?P<id>\d+)/delete/day/(?P<day_id>\d+)$', 'delete_day'),
    url(r'^workout/day/view/(?P<id>\d+)$', 'view_day'),
    
    # Sets and Settings
    url(r'^workout/(?P<id>\d+)/day/(?P<day_id>\d+)/edit/set/(?P<set_id>\w*)$', 'edit_set'),
    url(r'^workout/(?P<id>\d+)/day/(?P<day_id>\d+)/delete/set/(?P<set_id>\d+)$', 'delete_set'),
    url(r'^workout/(?P<id>\d+)/set/(?P<set_id>\d+)/exercise/(?P<exercise_id>\d+)/edit/setting/(?P<setting_id>\d*)$', 'edit_setting'),
    url(r'^workout/(?P<id>\d+)/set/(?P<set_id>\d+)/exercise/(?P<exercise_id>\d+)/delete/setting$', 'delete_setting'),
    
    # AJAX
    url(r'^workout/api/edit-set$', 'api_edit_set'),
    url(r'^workout/api/edit-settting$', 'api_edit_setting'),
    url(r'^workout/api/user-preferences$', 'api_user_preferences'),
)

# PDF stuff is in a different file
urlpatterns = urlpatterns + patterns('manager.pdf',
     url(r'^workout/(?P<id>\d+)/pdf/$', 'workout_log'))
