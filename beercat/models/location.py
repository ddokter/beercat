from django.db import models
from django.utils.translation import ugettext_lazy as _
from .province import Province


class Location(models.Model):

    """ Any geographic location, be it a city or a village """

    name = models.CharField(_("Name"), max_length=100, unique=True)
    synonyms = models.CharField(_("Synonyms"), max_length=255,
                                null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):

        return "%s (%s)" % (self.name, self.province.abbr)

    class Meta:

        app_label = "beercat"
        ordering = ["name"]
