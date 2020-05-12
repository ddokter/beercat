from django.db import models
from django.utils.translation import ugettext_lazy as _
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
    def surname_normalized(self):

        parts = self.surname.split(",")
        parts.reverse()

        return " ".join(parts).strip()

    def __str__(self):

        _str = "%s, %s" % (self.surname_normalized, self.name)

        if self.date_of_birth or self.date_of_death:
            _str += " (%s - %s)" % (
                (self.date_of_birth and self.date_of_birth.year) or '',
                (self.date_of_death and self.date_of_death.year) or ''
            )

        return _str

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

            _story.append(event.story(*_previous))
            _previous.append(event)

        return " ".join(_story)

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

            styles = role.brewery.brewerystyle_set.all()

            if self.date_of_death:
                styles = styles.exclude(started__gte=self.date_of_death)

            if role.from_date and role.to_date:
                styles = styles.exclude(
                    started__gte=role.to_date).exclude(
                        stopped__lte=role.from_date
                    )

            elif role.from_date:

                styles = styles.exclude(stopped__lte=role.from_date)

            elif role.to_date:

                styles = styles.exclude(started__gte=role.to_date)

        return [style.style for style in styles]

    class Meta:

        app_label = "beercat"
        ordering = ["surname"]
