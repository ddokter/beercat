from django.views.generic import TemplateView
# from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from ..models.brewery import Brewery
from ..models.style import Style
from ..models.person import Person


class Search(TemplateView):

    template_name = "search.html"

    def list_items(self):

        results = []

        if self.request.GET.get('q'):

            query = self.request.GET.get('q')

            for brewery in Brewery.objects.filter(name__icontains=query):
                results.append(brewery)

            for person in Person.objects.filter(
                    Q(name__icontains=query) | Q(surname__icontains=query)):
                results.append(person)

            for style in Style.objects.filter(
                    Q(name__icontains=query) | Q(synonyms__icontains=query)):
                results.append(style)

        return results
