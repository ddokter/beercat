import re
from django.db import models


class FlexDate:

    """
    Represent a date that may be incomplete.  The date is represented
    like so:

      <mod><<dd->mm->yyyy

    Year is always there. Month may be there and if day is there,
    month must be there as well. Modifier may be one of:
      < > = ~
    to signify: before, after, exact, approx. If modifier is omitted,
    exact is assumed.

    DB storage is in reverse, to allow ordering on the data:

      <mod>yyyymmdd

    mm and dd may be unset. In that case the DB representation is 00.

    """

    year = None
    month = None
    day = None
    mod = None

    def __init__(self, day, month, year, mod="="):

        self.day = day
        self.month = month
        self.year = year
        self.mod = mod

    def __str__(self):

        parts = []

        for val in [self.year, self.month, self.day]:

            if val and val != "00":
                parts.insert(0, val)

        _str = "-".join(parts)

        if self.mod != '=':
            _str = "%s%s" % (self.mod, _str)

        return _str

    def db_val(self):

        return "%s%s%s%s" % (self.mod or '=',
                             self.year,
                             self.month or '00',
                             self.day or '00')

    def __len__(self):

        return str(self).__len__()

    def __lt__(self, other):

        return self.db_val() < other.db_val()

    def xx__eq__(self, other):

        return self.db_val() == other.db_val()

    @property
    def marker(self):

        return self.mod


class FlexDateField(models.CharField):

    def __init__(self, *args, **kwargs):

        kwargs['max_length'] = 11

        if 'null' not in kwargs:
            kwargs['null'] = True

        if 'blank' not in kwargs:
            kwargs['blank'] = True

        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):

        """ Parse from DB value """

        if value is None:
            return value

        return FlexDate(value[7:9], value[5:7], value[1:5], mod=value[0])

    def to_python(self, value):

        """ Parse from user defined input """

        if isinstance(value, FlexDate) or value is None:
            return value

        res = re.match(r"(?P<mod>[=<>~])?(?P<date>.*)", value)

        mod = res.group('mod') or '='

        parts = res.group("date").split("-")

        if len(parts) > 2:
            day = parts[-3]
        else:
            day = None

        if len(parts) > 1:
            month = parts[-2]
        else:
            month = None

        year = parts[-1]

        return FlexDate(day, month, year, mod=mod)

    def get_prep_value(self, value):

        if value is None:
            return value

        return value.db_val()
