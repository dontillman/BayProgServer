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
# Event objects don't save their creation dates, so instead
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

# [[prettycategory, objs], ...]
def group_by_category(clss):
    return [(pretty, clss.objects.filter(category=category))
            for (category, pretty) in clss.CATEGORIES]

# [[prettyregion, objs], ...]
def group_by_region(clss):
    return [(pretty, clss.objects.filter(city__region=region))
            for region, pretty in City.REGIONS]

# {'catbands': {cat: [col1, col2],...}}
def bands(request):
    def two_columns(items):
        split = ceil(len(items) / 2)
        return [items[0:split], items[split:]]

    catbandcols = [(cat, two_columns(bands))
                   for (cat, bands) in group_by_category(Band)]
    context = {'catbands': catbandcols}
    return render(request, 'bayprogapp/bands.html', context)

# {'regionvenues': {region: [venue,...],...}}
def venues(request):
    context = {'regionvenues': group_by_region(Venue)}
    return render(request, 'bayprogapp/venues.html', context)

# {'regionstores': {region: [store,...],...}}
def musicstores(request):
    context = {'regionstores': group_by_region(MusicStore)}
    return render(request, 'bayprogapp/musicstores.html', context)

# {'albums': [album,...]}
def albums(request):
    context = {'albums': list(Album.objects.all())}
    return render(request, 'bayprogapp/albums.html', context)

# {'categorymakers': {cat: [maker,...],...}}
def instrumentmakers(request):
    context = {'categorymakers': group_by_category(InstrumentMaker)}
    return render(request, 'bayprogapp/instrumentmakers.html', context)

# {'categorymakers': {cat: [maker,...],...}}
def equipmentmakers(request):
    context = {'categorymakers': group_by_category(EquipmentMaker)}
    return render(request, 'bayprogapp/equipmentmakers.html', context)

# {'categoryshops': {cat: [shop,...],...}}
def repairshops(request):
    context = {'categoryshops': group_by_category(RepairShop)}
    return render(request, 'bayprogapp/repair.html', context)

# {'stores': [store,...],
#  'mailorder': [store,...]}
def recordstores(request):
    stores = list(RecordStore.objects.all())
    context = {'stores': filter(lambda store: store.city, stores),
               'mailorder': filter(lambda store: not store.city, stores)}
    return render(request, 'bayprogapp/recordstores.html', context)

# Events are grouped by month.
# Only include events after the previous month.
# Return:
# {'monthevents': [[month, [event,...]],...]}
def events(request):
    thismonth = date.today().replace(day=1)
    lastmonth = (thismonth - timedelta(days=1)).replace(day=1)
    evtobjs = Event.objects.filter(date__gte=lastmonth).order_by('date')

    monthevents = [[m, list(es)]
                   for (m, es) in groupby(evtobjs, lambda e: e.month())]

    context = {'monthevents': monthevents}
    return render(request, 'bayprogapp/events.html', context)

#{'messages': [message,...]}
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
