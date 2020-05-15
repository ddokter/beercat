from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from .base import CreateView, UpdateView, DetailView
from ..models.person import Person
from ..models.event import PersonEvent
from ..utils import get_model_name


class FormSetMixin:

    def get_form(self, form_class=None):

        form = super().get_form(form_class=form_class)

        # form.fields.pop('style')

        return form

    @property
    def formset_label(self):

        return _("Events")

    @property
    def formset(self):

        factory = inlineformset_factory(Person, PersonEvent, exclude=[])

        kwargs = {}

        if self.request.method == "POST":
            kwargs['data'] = self.request.POST

        if self.object:
            kwargs['instance'] = self.object

        return factory(**kwargs)

    def form_valid(self, form):

        self.object = form.save()

        _formset = self.formset

        if _formset.is_valid():
            _formset.save()

        return HttpResponseRedirect(self.get_success_url())


class PersonDetailView(DetailView):

    model = Person

    def repr(self, obj):

        _model = get_model_name(obj)

        if _model == "relation":

            if self.object == obj.subj:
                _dict = {'obj': obj.obj, 'name': obj.name_label}
            else:
                _dict = {'obj': obj.subj, 'name': obj.name_label_inverse}

            return render_to_string("snippets/title/relation.html", _dict)

        elif _model == "role":

            _dict = {
                'obj': obj.brewery,
                'name': obj.name_label
            }

            _date = ""

            if obj.from_date:
                _date += "v.a. %s" % obj.from_date.year

            if obj.to_date:
                _date += " tot %s" % obj.to_date.year

            _dict.update({'date': _date})

            return render_to_string("snippets/title/personrole.html", _dict)
        else:
            return super().repr(obj)


class PersonCreateView(FormSetMixin, CreateView):

    model = Person


class PersonUpdateView(FormSetMixin, UpdateView):

    model = Person
