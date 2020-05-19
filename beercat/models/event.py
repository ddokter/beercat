import random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel
from .datefield import FlexDateField


PERSON_EVENT_VOCAB = [
    (1, _('Birth')),
    (2, _('Death')),
    (3, _('Move')),
    (4, _('End brewing career'))
]


# TODO: op/in
PERSON_EVENT_STORY = {

    1: ["%(person)s wordt geboren in %(date)s in %(location)s.",
        "In %(date)s wordt %(person)s geboren te %(location)s"],
    2: ["%(person)s overlijdt in %(date)s."],
    3: ["%(person)s verhuist naar %(location)s in %(date)s."]
}

BREWERY_EVENT_VOCAB = [
    (1, _('Start')),
    (2, _('End')),
    (3, _('Auction')),
    (4, _('Move')),
    (5, _('Remodel')),
    (6, _('Sold')),
    (7, _('Merge')),
    (8, _('Liquidation'))
]


class EventMixin:

    """ Event base class """

    @property
    def name_label(self):

        return self._meta.model.get_name_display(self)

    def __str__(self):

        return "%s %s" % (self.name_label, self.date)

    def to_dict(self, *previous_events):

        _dict = {}

        for fld in self._meta.fields:

            value = getattr(self, fld.name)

            if hasattr(value, 'story_str'):
                value = value.story_str()

            _dict[fld.name] = value

        return _dict


class PersonEvent(EventMixin, models.Model):

    """ Person related events """

    name = models.IntegerField(choices=PERSON_EVENT_VOCAB)
    date = FlexDateField(null=False, blank=False)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    location = models.ForeignKey('Location', on_delete=models.CASCADE,
                                 null=True, blank=True)
    details = models.TextField(_("Description"), null=True, blank=True)

    def story(self, *previous_events):

        tpl = random.choice(PERSON_EVENT_STORY[self.name])

        _dict = {'date': self.date.year}

        if self.location:
            _dict.update({'location': self.location.name})
        else:
            _dict.update({'location': '?'})

        if self.name == 2:
            _dict['person'] = self.person.surname_normalized
        else:
            if previous_events:
                if self.person.gender == 0:
                    _dict['person'] = 'hij'
                else:
                    _dict['person'] = 'zij'
            else:
                _dict['person'] = "%s %s" % (self.person.name,
                                             self.person.surname_normalized)

        return tpl % _dict

    class Meta:

        ordering = ['date']


class BreweryEvent(EventMixin, PolymorphicModel):

    """ Brewery related events """

    name = models.IntegerField(choices=BREWERY_EVENT_VOCAB)
    brewery = models.ForeignKey('Brewery', on_delete=models.CASCADE)
    date = FlexDateField()
    details = models.TextField(_("Description"), null=True, blank=True)


class BreweryMerge(BreweryEvent):

    """ Brewery merge """

    # TODO: fill name field with 'merge'

    into_brewery = models.ForeignKey('Brewery',
                                     related_name="into",
                                     on_delete=models.CASCADE)
    name_label = 'merge'

    def __str__(self):

        return "%s %s -> %s" % (self.name_label, self.date, self.into_brewery)
