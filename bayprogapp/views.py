#from django.http import HttpResponse
from django.shortcuts import render
from .models import Album, Band, City, Event, EquipmentMaker, HomePageMessage, InstrumentMaker, Message, MusicStore, RecordStore, RepairShop, Venue
from math import ceil
from itertools import groupby
from datetime import date, datetime, timedelta
from django.contrib.auth import logout
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

import logging
logger = logging.getLogger('django')

# Find recently added events.
# Event objects don't save their creatiion dates, so instead
# we go over recent log entries.
#   The log entry must be an ADDITION.
#   The event must still exist (wasn't subsequently deleted).
#   The event shouldn't have already occured.
#   (Ie., the event was added too late, like for historical reference.)
def get_recently_added_events():

    # Given a log entry, return the event object if it exists,
    # else None.
    def log_event(entry):
        try:
            return entry.get_edited_object()
        except Event.DoesNotExist:
            return None;

    today = datetime.now().date()
    recently = today - timedelta(days=7)
    eventtype = ContentType.objects.get_for_model(Event)
    logs = LogEntry.objects.filter(content_type=eventtype,
                                   action_flag=ADDITION,
                                   action_time__gte=recently)
    return [e
            for e in map(log_event, logs)
            if e and today <= e.date]

# A ?logout=true query logs out as a side effect.
def home(request):
    if request.GET.get('logout'):
        logout(request)
        logger.debug('logged out')

    messages = [msgobj.text.strip()
                for msgobj in list(HomePageMessage.objects.all())]

    # event reminders
    week = date.today() + timedelta(days=7)
    upcoming_events = Event.objects.filter(date__gte=date.today(),
                                           date__lt=week)
    context = {'messages': messages,
               'upcoming_events': upcoming_events.reverse(),
               'new_events': get_recently_added_events(),
               'albums': list(Album.objects.all()[:8])}
    return render(request, 'bayprogapp/home.html', context)

def listBands(**keys):
    bands = list(Band.objects.filter(**keys).all())
    split = ceil(len(bands) / 2)
    return (bands[0:split], bands[split:])

def bands(request):
    context = {'activeBands': listBands(active=True, tribute=False),
               'tributeBands': listBands(active=True, tribute=True),
               'inactiveBands': listBands(active=False)}
    return render(request, 'bayprogapp/bands.html', context)

## split the objects up by their city's region
def regionsplit(items):
    return [(pretty, [item for item in items if item.city.region == region])
            for region, pretty in City.REGIONS]

# python 3.9 has this 
def removeprefix(prefix, text):
    if text.startswith(prefix):
        return text[len(prefix):]
    else:
        return text

def venues(request):
    venueObjs = sorted(Venue.objects.all(),
                       key=lambda venue: removeprefix('The ', venue.name))
    context = {'regionvenues': regionsplit(venueObjs)}
    return render(request, 'bayprogapp/venues.html', context)

def albums(request):
    context = {'albums': list(Album.objects.all())}
    return render(request, 'bayprogapp/albums.html', context)

def musicstores(request):
    context = {'musicstoresbyregion': regionsplit(list(MusicStore.objects.all()))}
    return render(request, 'bayprogapp/musicstores.html', context)

# get the objects in the class and split them up by category
def categorysplit(modelclass):
    items = list(modelclass.objects.all())
    return [(pretty, [item
                      for item in items
                      if item.category == category])
            for category, pretty in modelclass.CATEGORIES]

def instrumentmakers(request):
    context = {'categorymakers': categorysplit(InstrumentMaker)}
    return render(request, 'bayprogapp/instrumentmakers.html', context)

def equipmentmakers(request):
    context = {'categorymakers': categorysplit(EquipmentMaker)}
    return render(request, 'bayprogapp/equipmentmakers.html', context)

def repairshops(request):
    context = {'categoryrepairshops': categorysplit(RepairShop)}
    return render(request, 'bayprogapp/repair.html', context)

def recordstores(request):
    stores = list(RecordStore.objects.all())
    context = {'recordstores': filter(lambda store: store.city, stores),
               'mailorderrecords': filter(lambda store: not store.city, stores),}
    return render(request, 'bayprogapp/recordstores.html', context)

# Events page
# Events are grouped by month.
# Only include events after the previous month.
# Return:
#   'monthevents': [[month, [event,...]],...]
def events(request):
    thismonth = date.today().replace(day=1)
    lastmonth = (thismonth - timedelta(days=1)).replace(day=1)
    evtobjs = Event.objects.filter(date__gte=lastmonth).order_by('date')

    monthevents = [[m, list(es)]
                   for (m, es) in groupby(evtobjs, lambda e: e.month())]

    context = {'monthevents': monthevents}
    return render(request, 'bayprogapp/events.html', context)

def messages(request):
    if request.method == 'POST':
        message = Message(author=request.user,
                          text=request.POST['text'])
        message.save()

    messages = [{'date': message.date,
                 'author': message.author,
                 'authorname': message.author.get_full_name(),
                 'text': message.text}
                 for message in Message.objects.order_by('-date')]
    context = {'messages': messages}
    return render(request, 'bayprogapp/messages.html', context)

