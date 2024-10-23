from django.db.models import BooleanField, CharField, CASCADE, DateField, DateTimeField, ForeignKey, ImageField, IntegerField, Model, SET_NULL, TextField, URLField
from django.db.models.functions import Coalesce
from django.utils import timezone
from bayproguser.models import BayProgUser
from PIL import Image

class HomePageMessage(Model):
    text = TextField()
    pinned = BooleanField('Pin?', default=False)
    date = DateTimeField('Posting date and time', default=timezone.now)

    class Meta:
        ordering = ['-pinned', '-date']

    def __str__(self):
        return self.text[:80]


class Band(Model):
    name = CharField('Name', max_length=64, unique=True)
    alpha = CharField('Alphabetized name (optional)',
                             blank=True, null=True, max_length=32)
    url = URLField('Web site')
    tribute = BooleanField('Tribute band?', default=False)
    active =  BooleanField('Active?', default=True)

    class Meta:
        ordering = [Coalesce('alpha', 'name')]

    def __str__(self):
        return self.name

class Album(Model):
    band = CharField('Artist name', max_length=64)
    name = CharField('Album name', max_length=80)
    url = URLField('Web site')
    image = ImageField('Cover art', upload_to='bayprogapp/albums')
    date = DateField('Release date (for sorting)', default=timezone.now)

    class Meta:
        ordering = ['-date', 'band']

    def __str__(self):
        return self.band + ', ' + self.name


class City(Model):
    REGIONS = [('north', 'North, Sacramento'),
               ('east', 'East Bay, East'),
               ('sanfrancisco', 'San Francisco'),
               ('peninsula', 'Penninsula, San Jose'),
               ('south', 'South')]
    name = CharField('Name', primary_key=True, max_length=64)
    region = CharField('Region', choices=REGIONS, max_length=64)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Venue(Model):
    name = CharField('Venue name', max_length=64)
    prefix_the = BooleanField('Prefix with "the"?', default=False)
    url = URLField('Web site')
    note = CharField('Note (optional)', blank=True, max_length=80)
    address = CharField('Address', max_length=80)
    city = ForeignKey(City, null=True, on_delete=SET_NULL)
    capacity = IntegerField('Capacity (optional)', null=True, blank=True)

    class Meta:
        ordering = ['name']

    # Venues might need a "the" prefix in the listings.
    def the_name(self):
        return ('the ' + self.name) if self.prefix_the else self.name

    def __str__(self):
        return self.name + ((', ' + self.city.name) if self.city else '')

    def pretty_capacity(self):
        if self.capacity:
            return f'cap: {self.capacity:,}'
        return ''

# we store out posters at this size
postersize = (256, 768)

class Event(Model):
    date = DateField()
    description = CharField(max_length=80)
    url = URLField('URL')
    venue = ForeignKey(Venue, null=True, blank=True, on_delete=SET_NULL)
    note = CharField('Non-venue or note (optional)', blank=True, max_length=80)

    def imagepath(instance, filename):
        return f'bayprogapp/posters/{instance.id}-{filename}'
    poster = ImageField('Poster (optional, portrait orientation)',
                               upload_to=imagepath,
                               blank=True)

    def save(self, *args, **kwargs):
        super(Event, self).save(*args, **kwargs)
        # resave the image out to a consistent size
        if (self.poster):
            image = Image.open(self.poster.path)
            image.thumbnail(postersize)
            image.save(self.poster.path)

    # Used in the event listings.
    def prettydate(self):
        return self.date.strftime('%b %-d, %A')

    # Used to filter by months in the event listings.
    def month(self):
        return self.date.strftime('%B')

    # Brief description used for listing updates on the home page.
    # "Event, Venue, Weds Mar 1"
    def brief(self):
        venue = self.venue.name if self.venue else self.note
        date = self.date.strftime("%a %b %-d")
        return f'{self.description}, {venue}, {date}'

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.brief()

class MusicStore(Model):
    name = CharField('Name', max_length=64)
    url = URLField('Web site')
    note = CharField('Note (optional)', blank=True, max_length=80)
    address = CharField('Address (optional)', blank=True, max_length=80)
    city = ForeignKey(City, null=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ', ' + self.city.name

class InstrumentMaker(Model):
    CATEGORIES = [('guitars', 'Guitars, Basses, Mandolins, Ukuleles'),
                  ('bowed', 'Bowed Strings'),
                  ('synthesizers', 'Synthesizers'),
                  ('drums', 'Drums, Percussion'),
                  ('more', 'More'),
                  ('accessories', 'Accessories')]
    name = CharField('Name', max_length=64)
    alpha = CharField('Alphabetized name (optional)',
                             blank=True, null=True, max_length=32)
    category = CharField('Category', choices=CATEGORIES, max_length=64)
    url = URLField('Web site')
    note = CharField('Note (optional)', blank=True, max_length=80)
    city = ForeignKey(City, null=True, on_delete=SET_NULL)

    class Meta:
        ordering = [Coalesce('alpha', 'name')]

    def __str__(self):
        return self.name + ', ' + self.city.name

class RepairShop(Model):
    CATEGORIES = [('instruments', 'Instruments'),
                  ('electronics', 'Electronics')]
    name = CharField('Name', max_length=64)
    category = CharField('Category', choices=CATEGORIES, max_length=64)
    url = URLField('Web site')
    note = CharField('Note (optional)', blank=True, max_length=80)
    address = CharField('Address (optional)', blank=True, max_length=80)
    city = ForeignKey(City, null=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ', ' + self.city.name

class EquipmentMaker(Model):
    CATEGORIES = [('amps', 'Guitar Amplifiers and Speakers'),
                  ('effects', 'Guitar Effects'),
                  ('parts', 'Instrument Parts'),
                  ('pickups', 'Guitar Pickups'),
                  ('software', 'Software, Apps, Services'),
                  ('equipment', 'Equipment')]
    name = CharField('Name', max_length=64)
    category = CharField('Category', choices=CATEGORIES, max_length=64)
    url = URLField('Web site')
    note = CharField('Note (optional)', blank=True, max_length=80)
    city = ForeignKey(City, null=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ((', ' + self.city.name) if self.city else '')

class RecordStore(Model):
    name = CharField('Name', max_length=64)
    url = URLField('Web site')
    address = CharField('Address (for brick and mortar)', blank=True, null=True, max_length=80)
    city = ForeignKey(City, null=True, blank=True, on_delete=SET_NULL,
                             verbose_name='City (for brick and mortar)')
    note = CharField('Note (optional)', blank=True, max_length=80)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name + ((', ' + self.city.name) if self.city else '')

# class Company(Model):
#     name = CharField(max_length=50)
#     url = URLField()
#     city = CharField(max_length=50)

# class Resource(Model):
#     name = CharField(max_length=50)
#     url = URLField()
#     text = TextField()

class Message(Model):
    date = DateTimeField('Posting date and time', default=timezone.now)
    author = ForeignKey(BayProgUser, on_delete=CASCADE,
                               verbose_name='Author')
    text = TextField()
    pinned = BooleanField('Pin?', default=False)

    class Meta:
        ordering = ['-pinned', '-date']

    def __str__(self):
        return self.text[:80]
