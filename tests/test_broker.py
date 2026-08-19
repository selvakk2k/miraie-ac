"""Unit tests for MirAIeBroker message routing, payload building, and topic subscriptions."""

import unittest
from unittest.mock import MagicMock, AsyncMock
import json

from miraie_ac.broker import MirAIeBroker
from miraie_ac.enums import PowerMode, HVACMode, FanMode, PresetMode, SwingMode, ConvertiMode, DisplayMode


class TestMirAIeBroker(unittest.IsolatedAsyncioTestCase):
    """Test MirAIeBroker routing and payload builders."""

    def setUp(self):
        self.broker = MirAIeBroker()

    def test_topic_callback_registration_and_dispatch(self):
        """Test on_message dispatches received JSON payload to topic handler."""
        received_payload = None
        def topic_cb(payload):
            nonlocal received_payload
            received_payload = payload

        topic = "miraie/v1/status/dev_123"
        self.broker.register_device_callback(topic, topic_cb)

        mock_msg = MagicMock()
        mock_msg.topic.value = topic
        mock_msg.payload = json.dumps({"ps": "on", "actmp": "24"}).encode("utf-8")

        self.broker.on_message(mock_msg)

        self.assertIsNotNone(received_payload)
        self.assertEqual(received_payload["ps"], "on")
        self.assertEqual(received_payload["actmp"], "24")

    def test_topic_callback_removal(self):
        """Test remove_device_callback unbinds topic listener."""
        call_count = 0
        def topic_cb(payload):
            nonlocal call_count
            call_count += 1

        topic = "miraie/v1/status/dev_123"
        self.broker.register_device_callback(topic, topic_cb)
        self.broker.remove_device_callback(topic)

        mock_msg = MagicMock()
        mock_msg.topic.value = topic
        mock_msg.payload = b'{"ps": "on"}'

        self.broker.on_message(mock_msg)
        self.assertEqual(call_count, 0)

    def test_build_power_payload(self):
        """Test build_power_payload formats correctly."""
        p_on = self.broker.build_power_payload(PowerMode.ON)
        self.assertEqual(p_on["ps"], "on")
        self.assertEqual(p_on["ki"], 1)

        p_off = self.broker.build_power_payload(PowerMode.OFF)
        self.assertEqual(p_off["ps"], "off")

    def test_build_temperature_payload(self):
        """Test build_temperature_payload formats whole numbers vs decimals."""
        p_int = self.broker.build_temperature_payload(24.0)
        self.assertEqual(p_int["actmp"], "24")

        p_float = self.broker.build_temperature_payload(24.5)
        self.assertEqual(p_float["actmp"], "24.5")

    def test_build_hvac_mode_payload(self):
        """Test build_hvac_mode_payload formats string value."""
        p_cool = self.broker.build_hvac_mode_payload(HVACMode.COOL)
        self.assertEqual(p_cool["acmd"], "cool")

        p_dry = self.broker.build_hvac_mode_payload(HVACMode.DRY)
        self.assertEqual(p_dry["acmd"], "dry")

    async def test_publish_when_connected(self):
        """Test publish succeeds when client is connected."""
        mock_client = AsyncMock()
        self.broker.client = mock_client
        self.broker.connected.set()

        await self.broker.set_power("test/topic", PowerMode.ON)
        mock_client.publish.assert_awaited_once()

    async def test_publish_timeout_when_disconnected(self):
        """Test publish raises MqttError when broker stays disconnected past timeout."""
        from aiomqtt import MqttError
        self.broker.client = None
        self.broker.connected.clear()

        with self.assertRaises(MqttError):
            await self.broker.publish("test/topic", "{}", timeout=0.05)


if __name__ == "__main__":
    unittest.main()
