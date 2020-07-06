from django.shortcuts import render, HttpResponse,redirect
# from django.http import HttpResponse as ht
import datetime
from .models import *
from .function import update_fun, coordinates

from io import BytesIO
import base64
import matplotlib.pyplot as plt
import numpy as np



def reset(request):
    request.session.flush()
    bus = BusStop.objects.all()
    for b in bus:
        t = BusSchedule.objects.get(busstop=b)
        t.arrival = b.arrival
        t.departure = b.departure
        t.status = "NOT STARTED FROM TERMINAL"
        t.save()
    return redirect('/')

def home(request):
    return render(request, 'index.html')


def sys_time(request):
    if 'time' in request.POST:
        time = request.POST['time']
    else:
        time = request.session['time']
    t = datetime.time(int(time[:2]), int(time[3:]))
    request.session['time'] = time
    blank = datetime.time(00, 00)
    route = Route.objects.get(name='Route 1')
    bus = BusSchedule.objects.filter(route=route)
    for b in bus:

        if b.departure < t and not (b.departure == blank):
            b.status = 'Departed From ' + b.busstop.stop.name
            b.save()
            try:
                real = BusStopReal.objects.get(busstop=b.busstop, date=datetime.date.today())
                if b.departure == real.departure:
                    pass
                else:
                    real.arrival = b.arrival
                    real.departure = b.departure
                    real.save()
            except:
                real = BusStopReal(date=datetime.date.today(), busstop=b.busstop, arrival=b.arrival,
                                   departure=b.departure)
                real.save()
        elif b.departure == t :
            b.status = 'DEPARTING FROM ' + b.busstop.stop.name
            b.save()
            try:
                real = BusStopReal.objects.get(busstop=b.busstop, date=datetime.date.today())
                if b.departure == real.departure:
                    pass
                else:
                    real.arrival = b.arrival
                    real.departure = b.departure
                    real.save()
            except:
                real = BusStopReal(date=datetime.date.today(), busstop=b.busstop, arrival=b.arrival,
                                   departure=b.departure)
                real.save()
        else:
            if b.arrival == blank and b.departure>t:
                b.status = 'NOT STARTED FROM TERMINAL'
                b.save()
            else:
                ti = b.arrival
                h = ti.hour - t.hour
                min = ti.minute - t.minute
                min += h*60
                if min < 0:
                    b.status = 'END OF JOURNEY'
                elif min == 0:
                    b.status = 'AT STOP '+b.busstop.stop.name
                else:
                    b.status = str(min) + ' MINs TO STOP ' + b.busstop.stop.name
                b.save()
    return render(request, 'schedule-real.html', {'bus':bus})


def bus_test(request, bus):

    bus_name = Bus.objects.get(name=bus)
    bus_stop = BusStop.objects.filter(bus=bus_name)
    bus_real_list = []
    for bs in bus_stop:
        bus_real = BusSchedule.objects.get(busstop=bs)
        bus_real_list.append(bus_real)
    return render(request, 'schedule-real.html', {'bus': bus_real_list})


def stop_test(request, stop):

    stop_name = Stop.objects.get(name=stop)
    bus_stop = BusStop.objects.filter(stop=stop_name)
    stop_real_list = []
    for bs in bus_stop:
        stop_real = BusSchedule.objects.get(busstop=bs)
        stop_real_list.append(stop_real)
    return render(request, 'schedule-real.html', {'bus': stop_real_list})


def schedule(request):
    route = Route.objects.get(name='Route 1')
    sch = BusStop.objects.filter(route=route)
    context = {
        'schedule': sch,
    }
    template = 'schedule.html'
    return render(request, template, context)


def realSchedule(request):
    route = Route.objects.get(name='Route 1')
    sch = BusSchedule.objects.filter(route=route)
    context = {
        'bus': sch,
    }
    template = 'schedule-real.html'
    return render(request, template, context)

def bus(request):
    route = Route.objects.get(name='Route 1')
    bus_list = Bus.objects.filter(route=route)
    template = 'bus.html'
    context = {
        'list': bus_list,
        'name': 'bus'
    }
    return render(request, template, context)


def stop(request):
    route = Route.objects.get(name='Route 1')
    stop_list = Stop.objects.filter(route=route)
    template = 'bus.html'
    context = {
        'list': stop_list,
        'name': 'stop',
    }
    return render(request, template, context)





def update(request, busstop):
    bus = busstop.split('--')[0]
    stop = busstop.split('--')[1]
    try:
        bus = Bus.objects.get(name=bus)
        stop = Stop.objects.get(name=stop)
    except:
        return HttpResponse('ERROR')
    
    if request.method == 'GET':
        route = Route.objects.get(name='Route 1')
        bus_stop = BusStop.objects.get(route=route, bus=bus, stop=stop)
        sch = BusSchedule.objects.get(busstop=bus_stop)
        context = {
            'bus' : bus,
            'stop' : stop,
            'arrival' : sch.arrival,
            'departure' : sch.departure,
        }
        return render(request, 'update.html', context=context)
    else:
        min = int(request.POST['min'])
        if min < 0:
            #arrival time will be changed departure will remain same
            route = Route.objects.get(name='Route 1')
            bus_stop = BusStop.objects.get(route=route, bus=bus, stop=stop)
            real = BusSchedule.objects.get(busstop=bus_stop)
            time = (datetime.datetime.combine(datetime.date(1, 1, 1), real.arrival) - datetime.timedelta(minutes=-min)).time()
            real.arrival = time
            real.save()
            return sys_time(request)
        else:
            route = Route.objects.get(name='Route 1')
            bus_stop = BusStop.objects.get(route=route, bus=bus, stop=stop)
            update_fun(bus_stop, min)
            return sys_time(request)

def image(request):
    crd = coordinates(request.session['time'])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    print(crd['x1'],crd['y1'])
    print(crd['x2'],crd['y2'])
    ax.plot(crd['x1'], crd['y1'], color='lightblue', label='Original')
    ax.plot(crd['x2'], crd['y2'], color='darkgreen', label='Real-Time')
    ax.legend()
    pos = [i+1 for i in range(len(crd['ylable']))]
    ax.set_yticks(pos)
    ax.set_yticklabels(crd['ylable'])
    ax.set_xticklabels(crd['xlable'])
    ax.set_xticks(crd['x1'])
    ax.set_xlabel('Buses')
    ax.set_ylabel('Stops')
    ax.set_title('BUS STOP')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'graphic.html',{'graphic':graphic})

def jam(request):
    time = int(request.POST['jam'])
    start = datetime.time(int(request.session['time'][:2]), int(request.session['time'][3:]))
    end = (datetime.datetime.combine(datetime.date(1, 1, 1), start) + datetime.timedelta(minutes=time)).time()
    route = Route.objects.get(name="Route 1")
    stops = Stop.objects.filter(route=route)
    buses = Bus.objects.filter(route=route)
    for stop in stops:
        for bus in buses:
            busstop = BusStop.objects.get(bus=bus, stop=stop, route=route)
            busschedule = BusSchedule.objects.get(busstop=busstop)
            # print(busschedule.departure, start)
            if  busschedule.departure>=start or busschedule.departure == datetime.time(00,00):
                # next_stop = stop.next   
                # next_stop = Stop.objects.get(name=next_stop, route=route)
                # next_bus_stop = BusStop.objects.get(bus=bus, stop=next_stop, route=route)
                if busschedule.arrival>=start and busschedule.arrival != datetime.time(0,0):
                    busschedule.arrival = (datetime.datetime.combine(datetime.date(1, 1, 1), busschedule.arrival) + datetime.timedelta(minutes=time)).time()
                    busschedule.save()
                if busschedule.departure != datetime.time(00,00):
                    busschedule.departure = (datetime.datetime.combine(datetime.date(1, 1, 1), busschedule.departure) + datetime.timedelta(minutes=time)).time()
                    busschedule.save()
    for bus in buses:
        for s in stops:
            busstoptemp = BusStop.objects.get(route=route, bus=bus, stop=s)
            real = BusSchedule.objects.get(busstop=busstoptemp)
            if real.busstop.bus.next == 'NA':
                pass
            else:
                next_bus = Bus.objects.get(name=real.busstop.bus.next, route=route)
                next_busstop = BusStop.objects.get(bus=next_bus, stop=s, route=route)
                next_real = BusSchedule.objects.get(busstop=next_busstop)
                h = real.arrival.hour - next_real.arrival.hour
                m = real.arrival.minute - next_real.arrival.minute
                diff = h*60 + m
                if diff > 0:
                    if diff < 5:
                        real.departure = (datetime.datetime.combine(datetime.date(1, 1, 1), real.departure) + datetime.timedelta(minutes=5-diff)).time()
                        real.save()
                else:
                    update_fun(next_busstop,(10+diff))
    
    return sys_time(request)
                

