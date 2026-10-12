from unittest import TestCase

from appgoblin_play_scraper.features.app import _has_tv_permission


class TestAppParser(TestCase):
    def test_read_tv_permission(self):
        self.assertTrue(_has_tv_permission(["read TV channel/program information"]))

    def test_write_tv_permission(self):
        self.assertTrue(_has_tv_permission({"permissions": [
            [None, "write TV channel/program information"]
        ]}))

    def test_unrelated_permissions(self):
        self.assertFalse(_has_tv_permission({"permissions": [
            "transmit infrared",
            "receive data from Internet",
        ]}))

    def test_partial_permission_name_does_not_match(self):
        self.assertFalse(_has_tv_permission("read TV channel/program"))