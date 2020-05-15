from django.db.models import TextField


class MDField(TextField):

    def formfield(self, **kwargs):
        kwargs['strip'] = False
        return super(MDField, self).formfield(**kwargs)
