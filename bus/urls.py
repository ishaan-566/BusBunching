from django.urls import path
from .views import *
app_name = 'bus'

urlpatterns = [
    path('', home, name='home'),
    path('reset', reset, name='reset'),
    path('time_sys', sys_time, name='sys_time'),
    path('bus-schedule', schedule, name='schedule'),
    path('bus-schedule-real', realSchedule, name='real-schedule'),
    path('bus-test/<bus>', bus_test, name='bus-test'),
    path('stop-test/<stop>', stop_test, name='stop-test'),
    path('bus', bus, name='bus'),
    path('stop', stop, name='stop'),
    path('update<busstop>', update, name='update'),
    path('img', image, name='image'),
    path('jam', jam, name='jam'),
]
