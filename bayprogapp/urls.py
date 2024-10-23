from django.urls import include, path
from . import views

urlpatterns = [
    path('albums', views.albums, name='albums'),
    path('bands', views.bands, name='bands'),
    path('events', views.events, name='events'),
    path('venues', views.venues, name='venues'),
    path('musicstores', views.musicstores, name='musicstores'),
    path('instrumentmakers', views.instrumentmakers, name='instrumentmakers'),
    path('equipmentmakers', views.equipmentmakers, name='equipmentmakers'),
    path('repair', views.repairshops, name='repair'),
    path('recordstores', views.recordstores, name='recordstores'),    
    path('messages', views.messages, name='messages'),
    #path('accounts/', include('bayproguser.urls')),
    path('', views.home, name='home'),
]

