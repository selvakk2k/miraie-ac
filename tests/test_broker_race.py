import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from aiomqtt import MqttError

from miraie_ac.broker import MirAIeBroker
from miraie_ac.hub import MirAIeHub
from miraie_ac.device import Device
from miraie_ac.home import Home
from miraie_ac.user import User


class MockAsyncContextManager:
    def __init__(self, enter_delay=0.05, raise_mqtt_error_first=False):
        self.enter_delay = enter_delay
        self.raise_mqtt_error_first = raise_mqtt_error_first
        self.call_count = 0
        self.stop_event = asyncio.Event()
        self.publish = AsyncMock()
        self.subscribe = AsyncMock()

    @property
    def messages(self):
        return self._messages()

    async def _messages(self):
        await self.stop_event.wait()
        if False:
            yield None

    async def __aenter__(self):
        self.call_count += 1
        if self.enter_delay > 0:
            await asyncio.sleep(self.enter_delay)
        if self.raise_mqtt_error_first and self.call_count == 1:
            raise MqttError("Connection failed")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


class NeverConnectingContextManager:
    async def __aenter__(self):
        await asyncio.sleep(3600)  # Hangs indefinitely

    async def __aexit__(self, exc_type, exc, tb):
        pass


class TestBrokerRace(unittest.IsolatedAsyncioTestCase):

    @patch("miraie_ac.broker.Client")
    async def test_race_condition_resolved(self, mock_client_cls):
        """Confirm hub.init waits for connection readiness so subsequent commands succeed."""
        mock_client = MockAsyncContextManager(enter_delay=0.1)
        mock_client_cls.return_value = mock_client

        broker = MirAIeBroker()
        broker.use_ssl = False

        device = Device(
            id="dev1",
            name="test-device",
            friendly_name="Test Device",
            control_topic="topic/control",
            status_topic="topic/status",
            connection_status_topic="topic/conn",
            broker=broker,
        )
        home = Home(id="home1", devices=[device])

        hub = MirAIeHub(session=AsyncMock())
        hub._authenticate = AsyncMock()
        hub._get_home_details = AsyncMock()
        hub.get_all_device_status = AsyncMock()
        hub.home = home
        hub.user = User(access_token="token", refresh_token="refresh", user_id="uid", expires_in=3600)

        # hub.init should block until broker.connected event is set
        await hub.init("user", "pass", broker)

        self.assertTrue(broker.connected.is_set())
        
        # Turn off command should succeed without AttributeError
        await device.turn_off()
        mock_client.publish.assert_called_once()

        mock_client.stop_event.set()
        await hub.close()

    @patch("miraie_ac.broker.Client")
    async def test_reconnect_mqtt_error_clears_and_resets_connected(self, mock_client_cls):
        """Confirm connected event is False on MqttError retry and becomes set after successful retry."""
        mock_client = MockAsyncContextManager(enter_delay=0.05, raise_mqtt_error_first=True)
        mock_client_cls.return_value = mock_client

        broker = MirAIeBroker()
        broker.use_ssl = False
        broker.reconnect_interval = 0.05

        device = Device(
            id="dev1",
            name="test-device",
            friendly_name="Test Device",
            control_topic="topic/control",
            status_topic="topic/status",
            connection_status_topic="topic/conn",
            broker=broker,
        )
        home = Home(id="home1", devices=[device])

        hub = MirAIeHub(session=AsyncMock())
        hub._authenticate = AsyncMock()
        hub._get_home_details = AsyncMock()
        hub.get_all_device_status = AsyncMock()
        hub.home = home
        hub.user = User(access_token="token", refresh_token="refresh", user_id="uid", expires_in=3600)

        # During first attempt (MqttError), connected must be False before retry succeeds
        self.assertFalse(broker.connected.is_set())

        await hub.init("user", "pass", broker)

        # After retry succeeds, connected should be set and mock_client called twice
        self.assertTrue(broker.connected.is_set())
        self.assertEqual(mock_client.call_count, 2)

        mock_client.stop_event.set()
        await hub.close()

    @patch("miraie_ac.hub.LOGGER.warning")
    @patch("miraie_ac.broker.Client")
    async def test_timeout_path_does_not_hard_fail_setup(self, mock_client_cls, mock_logger_warning):
        """Confirm that if broker never connects, _init_broker returns after timeout and logs warning."""
        mock_client_cls.return_value = NeverConnectingContextManager()

        broker = MirAIeBroker()
        broker.use_ssl = False

        device = Device(
            id="dev1",
            name="test-device",
            friendly_name="Test Device",
            control_topic="topic/control",
            status_topic="topic/status",
            connection_status_topic="topic/conn",
            broker=broker,
        )
        home = Home(id="home1", devices=[device])

        hub = MirAIeHub(session=AsyncMock())
        hub._authenticate = AsyncMock()
        hub._get_home_details = AsyncMock()
        hub.get_all_device_status = AsyncMock()
        hub.home = home
        hub.user = User(access_token="token", refresh_token="refresh", user_id="uid", expires_in=3600)

        # Patch asyncio.wait_for to use a short timeout for test speed
        original_wait_for = asyncio.wait_for
        async def fast_wait_for(fut, timeout):
            return await original_wait_for(fut, timeout=0.1)

        with patch("asyncio.wait_for", side_effect=fast_wait_for):
            # hub.init should not raise, but return normally after timeout
            await hub.init("user", "pass", broker)

        self.assertFalse(broker.connected.is_set())
        mock_logger_warning.assert_called_once_with(
            "MQTT broker connection did not complete within 30s; "
            "commands issued before it connects may fail until it does."
        )

        await hub.close()


if __name__ == "__main__":
    unittest.main()
