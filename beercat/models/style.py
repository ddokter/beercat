from django.db import models
from django.utils.translation import ugettext_lazy as _
from .role import BREWER_ROLES


class Style(models.Model):

    """ Beer style """

    name = models.CharField(_("Name"), max_length=100)
    synonyms = models.CharField(_("Synonyms"), max_length=255,
                                null=True, blank=True)
    description = models.TextField(_("Description"), null=True, blank=True)

    def __str__(self):

        _str = self.name

        if self.synonyms:
            _str += " (%s)" % self.synonyms

        return _str

    def list_breweries(self):

        return self.brewerystyle_set.all().order_by("started")

    def list_brewers(self):

        """ Find brewers that have brewed this style """

        _brewers = []

        for bs in self.list_breweries():

            roles = bs.brewery.role_set.filter(name__in=BREWER_ROLES)

            if bs.started and bs.stopped:

                roles = roles.exclude(from_date__gte=bs.stopped).exclude(
                    to_date__lte=bs.started
                )

            elif bs.started:

                roles = roles.exclude(to_date__lte=bs.started)

            elif bs.stopped:

                roles = roles.exclude(from_date__gte=bs.stopped)

            for role in roles:
                if role.person not in _brewers:
                    _brewers.append(role.person)

        return _brewers

    class Meta:
        app_label = "beercat"
        ordering = ["name"]
