import re
from operator import itemgetter
from markdown import markdown
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from ..utils import normalize_name
from .role import BREWER_ROLES


GENDER_CHOICES = [
    (0, 'male'),
    (1, 'female')
]


class Person(models.Model):

    """ Any geographic location, be it a city or a village """

    name = models.CharField(_("Name"), max_length=50)
    surname = models.CharField(_("Surname"), max_length=50)
    description = models.TextField(_("Description"), null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES)

    @property
    def initials(self):

        """ Turn the person's name into initials """

        return re.sub(r'[^A-Z\?\-]+', '.', self.name)

    @property
    def surname_normalized(self):

        """ Normalize surname in case of use of comma's """

        return normalize_name(self.surname)

    def __str__(self):

        return "%s %s" % (self.initials, self.surname_normalized)

    def short(self):

        return "%s, %s" % (self.surname_normalized, self.name)

    @property
    def date_of_birth(self):

        try:
            return self.personevent_set.filter(name=1).first().date
        except:
            return None

    @property
    def date_of_death(self):

        try:
            return self.personevent_set.filter(name=2).first().date
        except:
            return None

    def story(self):

        _story = []
        _previous = []

        for event in self.personevent_set.all():

            _story.append((event.date, event.story(*_previous)))
            _previous.append(event)

        for role in self.list_roles().filter(from_date__isnull=False):
            _story.append((role.from_date, role.story()))

        _story.sort(key=itemgetter(0))

        text = "\n".join([part[1] for part in _story])

        return mark_safe(markdown(text, extensions=['footnotes']))

    def story_str(self):

        return self.surname_normalized

    def list_roles(self):

        return self.role_set.all()

    def list_relations(self):

        return self.obj.all() | self.subj.all()

    def list_beers(self):

        """ List the beers that this person may have come to know
        as a brewer.
        """

        styles = []

        for role in self.role_set.filter(name__in=BREWER_ROLES):

            bstyles = role.brewery.brewerystyle_set.all()

            if self.date_of_death:
                bstyles = bstyles.exclude(started__gte=self.date_of_death)

            if role.from_date and role.to_date:
                bstyles = bstyles.exclude(
                    started__gte=role.to_date).exclude(
                        stopped__lte=role.from_date
                    )

            elif role.from_date:

                bstyles = bstyles.exclude(stopped__lte=role.from_date)

            elif role.to_date:

                bstyles = bstyles.exclude(started__gte=role.to_date)

            for bstyle in bstyles:
                if bstyle.style not in styles:
                    styles.append(bstyle.style)

        return styles

    class Meta:

        app_label = "beercat"
        ordering = ["surname"]
