from django.test import TestCase
from ..models.datefield import FlexDateField


class TestDateField(TestCase):

    def setUp(self):

        self.fdf = FlexDateField()

    def test_to_python(self):

        value = self.fdf.to_python("1866")

        self.assertEquals(value.mod, "=")
        self.assertEquals(value.year, "1866")
        self.assertEquals(value.month, None)
        self.assertEquals(value.day, None)

        value = self.fdf.to_python("<03-1866")

        self.assertEquals(value.mod, "<")
        self.assertEquals(value.year, "1866")
        self.assertEquals(value.month, "03")
        self.assertEquals(value.day, None)

        value = self.fdf.to_python("<20-03-1866")

        self.assertEquals(value.mod, "<")
        self.assertEquals(value.year, "1866")
        self.assertEquals(value.month, "03")
        self.assertEquals(value.day, "20")

    def test_get_prep_value(self):

        value = self.fdf.to_python("<20-03-1866")

        prep = self.fdf.get_prep_value(value)

        self.assertEquals(prep, "<18660320")

    def test_from_db_value(self):

        value = self.fdf.from_db_value("<18660320", None, None)

        self.assertEquals(value.year, "1866")
        self.assertEquals(value.mod, "<")
        self.assertEquals(value.month, "03")
        self.assertEquals(value.day, "20")
