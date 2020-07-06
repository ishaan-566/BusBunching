from .models import *
import datetime

def coordinates(time):
    t = datetime.time(int(time[:2]), int(time[3:]))
    route = Route.objects.get(name='Route 1')
    bus = Bus.objects.get(prev='NA', route=route)
    bus_list = []
    y1 = []
    y2 = []
    
    while True:
        bus_list.append(bus)
        bus = bus.next
        if bus == 'NA':
            break
        else:
            bus = Bus.objects.get(route=route, name=bus)

    stop = Stop.objects.get(prev='NA', route=route)
    stop_list = []
    while True:
        stop_list.append(stop)
        stop = stop.next
        if stop == 'NA':
            break
        else:
            stop = Stop.objects.get(route=route, name=stop)
    x2=x1 = [i+1 for i in range(len(bus_list))]
    for b in bus_list:
        i = 0
        for s in stop_list:
            i+=1
            busstop = BusStop.objects.get(bus=b, stop=s, route=route)
            if busstop.arrival == t or busstop.departure == t:
                y1.append(i)
                break
            elif busstop.arrival < t < busstop.departure:
                y1.append(i)
                break
            elif t > busstop.departure:
                try:
                    ts = Stop.objects.get(name=busstop.stop.next, route=route)
                    temp = BusStop.objects.get(bus=b, stop=ts, route=route)
                    if t < temp.arrival:
                        y1.append(i+0.5)
                        break
                except:
                    y1.append(len(stop_list))
                    break
                

    for b in bus_list:
        i = 0
        for s in stop_list:
            i+=1
            bsst = BusStop.objects.get(bus=b, stop=s, route=route)
            busstop = BusSchedule.objects.get(busstop=bsst)
            if busstop.arrival == t or busstop.departure == t:
                y2.append(i)
                break
            elif busstop.arrival < t < busstop.departure:
                y2.append(i)
                break
            elif t > busstop.departure:
                try:
                    ts = Stop.objects.get(name=bsst.stop.next, route=route)
                    tem = BusStop.objects.get(bus=b, stop=ts, route=route)
                    temp = BusSchedule.objects.get(busstop=tem)
                    if t < temp.arrival:
                        y2.append(i+0.5)
                        break
                except:
                    y2.append(len(stop_list))
                    break

    return {
        'xlable':bus_list,
        'ylable':stop_list,
        'x1':x1,
        'y1':y1,
        'x2':x2,
        'y2':y2
        }
            


    
def update_fun(busstop, min):
    if min<0:
        min = 0
    stops = []
    
    temp = busstop.stop
    route = Route.objects.get(name='Route 1')
    bus = busstop.bus
    while True:
        stops.append(temp)
        next = temp.next
        if next == 'NA':
            break
        else:
            temp = Stop.objects.get(name=next, route=busstop.route)
    for s in stops:
        print(busstop)
        busstoptemp = BusStop.objects.get(route=route, bus=bus, stop=s)
        real = BusSchedule.objects.get(busstop=busstoptemp)
        if real.arrival != datetime.time(0,0):
            time = (datetime.datetime.combine(datetime.date(1, 1, 1), real.arrival) + datetime.timedelta(minutes=min)).time()
            real.arrival = time
        if real.departure != datetime.time(0,0):
            real.departure = (datetime.datetime.combine(datetime.date(1, 1, 1), real.departure) + datetime.timedelta(minutes=min)).time()
        real.save()
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
                if diff < 5 and real.departure != datetime.time(0,0):
                    real.departure = (datetime.datetime.combine(datetime.date(1, 1, 1), real.departure) + datetime.timedelta(minutes=5-diff)).time()
                    real.save()
            else:
                update_fun(next_busstop,(10+diff))
    return