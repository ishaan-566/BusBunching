from django.contrib import admin
from .models import *

admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(Bus)
admin.site.register(BusStop)
admin.site.register(BusStopReal)
admin.site.register(BusSchedule)
admin.site.register(State)
admin.site.register(City)
