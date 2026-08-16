"""Unit tests for MirAIeHub authentication, energy querying, pagination, and lifecycle."""

import unittest
import asyncio
from datetime import date, timedelta
from unittest.mock import MagicMock, AsyncMock, patch

from miraie_ac import MirAIeHub
from miraie_ac.user import User
from miraie_ac.enums import ConsumptionPeriodType


class TestMirAIeHub(unittest.IsolatedAsyncioTestCase):
    """Test MirAIeHub initialization, authentication, energy history, and teardown."""

    async def test_hub_init_offline_mode_safe_close(self):
        """Verify hub and devices can be initialized and closed safely without a broker (offline/REST mode)."""
        hub = MirAIeHub()
        self.assertIsNone(hub.broker)
        # Closing hub without broker should complete cleanly with zero exceptions
        await hub.close()

    async def test_hub_authenticate_success(self):
        """Test successful authentication and token acquisition."""
        hub = MirAIeHub()
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={
            "accessToken": "test_access_token_123",
            "refreshToken": "test_refresh_token_456",
            "expiresIn": 3600,
            "userId": "usr_1",
        })
        mock_session = MagicMock()
        mock_session.post = AsyncMock(return_value=mock_resp)

        hub.http = mock_session

        await hub._authenticate("user@example.com", "password123")
        self.assertIsNotNone(hub.user)
        self.assertEqual(hub.user.access_token, "test_access_token_123")
        self.assertEqual(hub.user.user_id, "usr_1")

    async def test_hub_authenticate_invalid_credentials(self):
        """Test authentication failure raises Exception."""
        hub = MirAIeHub()
        mock_resp = MagicMock()
        mock_resp.status = 401
        mock_resp.json = AsyncMock(return_value={"message": "Invalid username or password"})
        mock_session = MagicMock()
        mock_session.post = AsyncMock(return_value=mock_resp)

        hub.http = mock_session

        with self.assertRaises(Exception):
            await hub._authenticate("user@example.com", "wrongpassword")

    async def test_get_energy_consumption_full_chunking(self):
        """Test get_energy_consumption_full cleanly splits a 14-month range into 6-month API chunks."""
        hub = MirAIeHub()
        hub.user = User("token_abc", "refresh_abc", "usr_1", 3600)
        mock_device = MagicMock()
        mock_device.id = "dev_living"

        start_date = date(2025, 1, 1)
        end_date = date(2026, 3, 1)  # 14 months

        call_count = 0
        async def fake_get_energy(device, period, from_date, to_date):
            nonlocal call_count
            call_count += 1
            return {from_date: 2.5}

        hub.get_energy_consumption = AsyncMock(side_effect=fake_get_energy)

        res = await hub.get_energy_consumption_full(
            mock_device,
            ConsumptionPeriodType.DAILY,
            start_date,
            end_date
        )

        self.assertEqual(call_count, 3)
        self.assertIsInstance(res, dict)
        self.assertGreaterEqual(len(res), 1)

    async def test_get_energy_consumption_success(self):
        """Test get_energy_consumption correctly parses and maps API array response."""
        hub = MirAIeHub()
        hub.user = User("token_abc", "refresh_abc", "usr_1", 3600)
        mock_device = MagicMock()
        mock_device.id = "dev_living"

        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value=[
            {"day": "01012026", "power": 3.5},
            {"day": "02012026", "power": 4.2},
        ])

        mock_session = MagicMock()
        mock_session.get = AsyncMock(return_value=mock_resp)
        hub.http = mock_session

        res = await hub.get_energy_consumption(
            mock_device,
            ConsumptionPeriodType.DAILY,
            from_date="01012026",
            to_date="02012026",
        )

        self.assertIn("01012026", res)
        self.assertEqual(res["01012026"], 3.5)
        self.assertEqual(res["02012026"], 4.2)


if __name__ == "__main__":
    unittest.main()
