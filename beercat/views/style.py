from django.template.loader import render_to_string
from ..utils import get_model_name
from ..models.style import Style
from .base import DetailView


# TODO: translatable
MARKERS = {
    '=': '',
    '~': 'ca.',
    '<': 'voor',
    '>': 'na'
}


class StyleDetailView(DetailView):

    model = Style

    def repr(self, obj):

        _model = get_model_name(obj)

        if _model == "brewerystyle":

            _dict = {'obj': obj.brewery}

            _date = ""

            if obj.started:
                _date += " v.a. %s %s" % (MARKERS.get(obj.started.marker, ''),
                                          obj.started.year)

            if obj.stopped:
                _date += " tot %s %s" % (MARKERS.get(obj.stopped.marker, ''),
                                         obj.stopped.year)

            _dict['date'] = _date

            return render_to_string("snippets/title/brewerystyle.html", _dict)
        else:
            return super().repr(obj)
