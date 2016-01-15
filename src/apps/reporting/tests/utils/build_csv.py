from apps.reporting.utils.build_csv import BuildCsv

from django.test import TestCase

from hamcrest import assert_that


class TestBuildCsv(TestCase):
    """
    TestBuildCsv
    """
    def test_csv_build(self):
        s = {
            "field": "value",
            "field2": "value2"
        }

        csv = BuildCsv()
        csv.input_json_structure(json=s)
        data = csv.build()
        assert_that(
            data,
            'field2,field\n\
            value2,value'
        )
