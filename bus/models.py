from django.db import models
from django.urls import reverse


class State(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=30)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=30)
    distance = models.IntegerField(default=0)
    time = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Stop(models.Model):
    name = models.CharField(max_length=30)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    distance = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    next = models.CharField(max_length=30)
    prev = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Bus(models.Model):
    name = models.CharField(max_length=30)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    next = models.CharField(max_length=30)
    prev = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class BusStop(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True)
    arrival = models.TimeField()
    departure = models.TimeField()

    def __str__(self):
        return str(self.bus) + "--" + str(self.stop)


class BusSchedule(models.Model):
    busstop = models.ForeignKey(BusStop, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    arrival = models.TimeField()
    departure = models.TimeField()
    status = models.CharField(max_length=50, default='NOT STARTED FROM TERMINAL')

    def __str__(self):
        return str(self.busstop) + ' | ' + str(self.arrival) + ' | ' + str(self.departure) +  ' | ' + self.status

    def update(self):
        return reverse('bus:update', args=[self.busstop])


class BusStopReal(models.Model):
    date = models.DateField()
    busstop = models.ForeignKey(BusStop, on_delete=models.CASCADE, null=True)
    arrival = models.TimeField()
    departure = models.TimeField()

    def __str__(self):
        return str(self.date)+'---'+str(self.busstop.bus) + "---" + str(self.busstop.stop)
