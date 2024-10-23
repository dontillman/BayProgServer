from django.contrib import admin

# Register your models here.
from .models import Album, Band, City, EquipmentMaker, Event, HomePageMessage, InstrumentMaker, Message, MusicStore, RecordStore, RepairShop, Venue

admin.site.register(Album)
admin.site.register(Band)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(City)
admin.site.register(HomePageMessage)
admin.site.register(InstrumentMaker)
admin.site.register(MusicStore)
admin.site.register(RepairShop)
admin.site.register(EquipmentMaker)
admin.site.register(RecordStore)
admin.site.register(Message)
