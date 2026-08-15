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

    def test_hub_context_manager_and_session_auto_init(self):
        import asyncio
        from unittest.mock import patch, AsyncMock
        from miraie_ac.hub import MirAIeHub

        async def _run_test():
            async with MirAIeHub() as hub:
                self.assertIsNotNone(hub.http)
                mock_resp = AsyncMock(status=200)
                mock_resp.json = AsyncMock(return_value={
                    "accessToken": "test_token",
                    "refreshToken": "test_refresh",
                    "userId": "test_user",
                    "expiresIn": 3600,
                })
                with patch.object(hub.http, "post", new_callable=AsyncMock, return_value=mock_resp):
                    await hub._authenticate("user@example.com", "pass")
                    self.assertEqual(hub.user.access_token, "test_token")

        asyncio.run(_run_test())


if __name__ == "__main__":
    unittest.main()

