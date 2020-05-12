from django.db import models
from django.utils.translation import ugettext_lazy as _
from .datefield import FlexDateField


ROLE_VOCAB = [
    (0, 'Onbekend'),
    (1, 'Brouwer'),
    (2, 'Brouwknecht'),
    (3, 'Directeur'),
    (4, 'Commissaris'),
    (5, 'Eigenaar'),
    (6, 'Secretaris'),
    (7, 'Adviseur')
]

STATUS_VOCAB = [
    (1, 'fact'),
    (2, 'assumption')
]


# Roles that are considered 'brewer' roles
#
BREWER_ROLES = [0, 1, 2, 3, 5]


class Role(models.Model):

    name = models.IntegerField(choices=ROLE_VOCAB)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    brewery = models.ForeignKey('Brewery', on_delete=models.CASCADE)

    from_date = FlexDateField()
    to_date = FlexDateField()

    details = models.TextField(_("Details"), null=True, blank=True)
    status = models.IntegerField(choices=STATUS_VOCAB, default=1)

    @property
    def name_label(self):

        return self._meta.model.get_name_display(self)

    def __str__(self):

        return "%s: %s %s (%s - %s)" % (
            self.person.short(),
            self.name_label,
            self.brewery,
            (self.from_date and self.from_date.year) or '',
            (self.to_date and self.to_date.year) or '')

    @property
    def detail_proxy(self):

        return self.person

    class Meta:

        app_label = "beercat"
        ordering = ["name"]
