from django.db import models
from django.utils.translation import ugettext_lazy as _


class Province(models.Model):

    """ Any geographic location, be it a city or a village """

    name = models.CharField(_("Name"), max_length=100, unique=True)
    abbr = models.CharField(_("Abbrevation"), max_length=3, unique=True)
    synonyms = models.CharField(_("Synonyms"), max_length=255,
                                null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):

        return self.name

    class Meta:

        app_label = "beercat"
        ordering = ["name"]
