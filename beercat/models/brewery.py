from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..utils import normalize_name
from .location import Location
from .datefield import FlexDateField
from .event import BreweryMerge
from .mdfield import MDField


class Brewery(models.Model):

    """ Any geographic location, be it a city or a village """

    name = models.CharField(_("Name"), max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    description = models.TextField(_("Description"), null=True, blank=True)
    style = models.ManyToManyField('Style', through='BreweryStyle')

    def __str__(self):

        return "%s - %s" % (normalize_name(self.name), self.location)

    def list_styles(self):

        return self.brewerystyle_set.all()

    def list_people(self):

        return self.role_set.all().order_by('person__surname')

    def list_events(self):

        return self.breweryevent_set.all()

    @property
    def closed(self):

        return self.stopped or self.merged

    @property
    def stopped(self):

        return self.breweryevent_set.filter(name=2).exists()

    @property
    def merged(self):

        return self.breweryevent_set.instance_of(BreweryMerge).exists()

    class Meta:

        app_label = "beercat"
        ordering = ["name"]
        verbose_name_plural = _("Breweries")


class BreweryStyle(models.Model):

    brewery = models.ForeignKey('Brewery', on_delete=models.CASCADE)
    style = models.ForeignKey('Style', on_delete=models.CASCADE)
    started = FlexDateField()
    stopped = FlexDateField()
    details = MDField(_("Details"), null=True, blank=True)

    def __str__(self):

        return "%s %s" % (self.brewery, self.style)
