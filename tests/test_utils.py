import unittest
from miraie_ac.utils import parse_room_temp, toFloat

class TestUtils(unittest.TestCase):

    def test_parse_room_temp_firmware_3_02_packed(self):
        # Firmware 3.02 packed format tests
        self.assertEqual(parse_room_temp("128.28", "3.02"), 28.50)
        self.assertEqual(parse_room_temp("193.29", "3.02"), 29.75)
        self.assertEqual(parse_room_temp("61.26", "3.02"), 26.24)
        self.assertEqual(parse_room_temp("01.28", "3.02"), 28.00)
        self.assertEqual(parse_room_temp("00.24", "3.02"), 24.00)

    def test_parse_room_temp_edge_cases(self):
        # Zero/uninitialized temperature returns None
        self.assertIsNone(parse_room_temp("00.0", "3.02"))
        # None or empty
        self.assertIsNone(parse_room_temp(None, "3.02"))

    def test_parse_room_temp_legacy_firmware(self):
        # Older firmware (e.g. 2.0 or 3.0) returns float directly
        self.assertEqual(parse_room_temp("25.5", "2.04"), 25.5)
        self.assertEqual(parse_room_temp("26.0", "3.00"), 26.0)

    def test_build_temperature_payload(self):
        from miraie_ac.broker import MirAIeBroker
        broker = MirAIeBroker()
        self.assertEqual(broker.build_temperature_payload(27.0)["actmp"], "27")
        self.assertEqual(broker.build_temperature_payload(27)["actmp"], "27")
        self.assertEqual(broker.build_temperature_payload(26.5)["actmp"], "26.5")

if __name__ == "__main__":
    unittest.main()

