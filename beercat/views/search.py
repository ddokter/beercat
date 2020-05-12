from django.views.generic import TemplateView


class Search(TemplateView):

    template_name = "search.html"

    def list_items(self):

        return []
