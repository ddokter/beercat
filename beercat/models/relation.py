from django.db import models
from django.utils.translation import ugettext_lazy as _
from .person import Person


RELATION_VOCAB = [
    (0, 'ongespecificeerd'),
    (1, 'vader van'),
    (-1, 'zoon van'),
    (2, 'man van'),
    (-2, 'vrouw van'),
    (3, 'broer van'),
    (4, 'zus van'),
    (5, 'aangetrouwd'),
    (6, 'zwager van'),
]

STATUS_VOCAB = [
    (1, 'fact'),
    (2, 'assumption')
]


class Relation(models.Model):

    subj = models.ForeignKey(Person,
                             related_name='subj',
                             on_delete=models.CASCADE)
    name = models.IntegerField(choices=RELATION_VOCAB)
    obj = models.ForeignKey(Person, on_delete=models.CASCADE,
                            related_name='obj')
    details = models.TextField(_("Details"), null=True, blank=True)
    status = models.IntegerField(choices=STATUS_VOCAB, default=1)

    @property
    def name_label(self):

        return self._meta.model.get_name_display(self)

    @property
    def name_label_inverse(self):

        class Foo:

            name = -self.name

        label = self._meta.model.get_name_display(Foo())

        if label == -self.name:
            label = self.name_label

        return label

    def __str__(self):

        return "%s: %s %s" % (
            self.subj.short(),
            self.name_label,
            self.obj.short())

    class Meta:

        app_label = "beercat"
        ordering = ["name"]
