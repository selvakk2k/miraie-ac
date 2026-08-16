"""Unit tests for Device status parsing, commands, callbacks, and offline mode."""

import unittest
from unittest.mock import MagicMock, AsyncMock

from miraie_ac.device import Device, DeviceStatus, DeviceDetails
from miraie_ac.enums import (
    PowerMode,
    HVACMode,
    FanMode,
    SwingMode,
    DisplayMode,
    PresetMode,
    ConvertiMode,
)


class TestDevice(unittest.IsolatedAsyncioTestCase):
    """Test Device parsing, callbacks, and commands."""

    def setUp(self):
        self.mock_broker = MagicMock()
        self.mock_broker.register_device_callback = MagicMock()
        self.mock_broker.remove_device_callback = MagicMock()
        self.mock_broker.publish = AsyncMock()
        self.mock_broker.set_power = AsyncMock()
        self.mock_broker.set_temperature = AsyncMock()
        self.mock_broker.set_hvac_mode = AsyncMock()
        self.mock_broker.set_fan_mode = AsyncMock()
        self.mock_broker.set_v_swing_mode = AsyncMock()
        self.mock_broker.set_h_swing_mode = AsyncMock()
        self.mock_broker.set_preset_mode = AsyncMock()
        self.mock_broker.set_converti_mode = AsyncMock()
        self.mock_broker.set_display_mode = AsyncMock()
        self.mock_broker.set_nanoe = AsyncMock()

        self.device = Device(
            id="dev_living",
            name="Living Room AC",
            friendly_name="Living Room AC",
            control_topic="miraie/v1/control/dev_living",
            status_topic="miraie/v1/status/dev_living",
            connection_status_topic="miraie/v1/connection/dev_living",
            broker=self.mock_broker,
        )

        initial_status = DeviceStatus(
            is_online=True,
            temperature=24.0,
            room_temperature=26.0,
            power_mode=PowerMode.ON,
            fan_mode=FanMode.AUTO,
            v_swing_mode=SwingMode.AUTO,
            h_swing_mode=SwingMode.AUTO,
            display_mode=DisplayMode.ON,
            hvac_mode=HVACMode.COOL,
            preset_mode=PresetMode.NONE,
            converti_mode=ConvertiMode.OFF,
        )
        self.device.set_status(initial_status)

    async def test_status_handler_parsing(self):
        """Test status_handler parses all payload attributes accurately."""
        callback_called = False
        def my_callback():
            nonlocal callback_called
            callback_called = True

        self.device.register_callback(my_callback)

        payload = {
            "actmp": "22.5",
            "rmtmp": "25.0",
            "ps": "on",
            "acfs": "high",
            "acvs": 0,
            "achs": 0,
            "acdc": "off",
            "acmd": "dry",
            "acpm": "on",
            "acem": "off",
            "acec": "off",
            "cnv": 80,
            "acngs": "on",
            "acfc": "on",
            "rssi": -65,
            "cnt": "ir",
        }

        self.device.status_handler(payload)

        self.assertTrue(callback_called)
        status = self.device.status
        self.assertEqual(status.temperature, 22.5)
        self.assertEqual(status.room_temperature, 25.0)
        self.assertEqual(status.power_mode, PowerMode.ON)
        self.assertEqual(status.fan_mode, FanMode.HIGH)
        self.assertEqual(status.hvac_mode, HVACMode.DRY)
        self.assertEqual(status.preset_mode, PresetMode.BOOST)
        self.assertEqual(status.converti_mode, ConvertiMode.C80)
        self.assertEqual(status.nanoe_mode, "on")
        self.assertTrue(status.filter_clean_alert)
        self.assertEqual(status.wifi_signal, -65)
        self.assertEqual(status.control_source, "ir")

    async def test_callback_registration_and_removal(self):
        """Test registering and unregistering callbacks."""
        call_count = 0
        def cb():
            nonlocal call_count
            call_count += 1

        self.device.register_callback(cb)
        self.device.refresh()
        self.assertEqual(call_count, 1)

        self.device.remove_callback(cb)
        self.device.refresh()
        self.assertEqual(call_count, 1)

    async def test_turn_on_and_turn_off_commands(self):
        """Test turn_on and turn_off dispatch through broker."""
        await self.device.turn_on()
        self.mock_broker.set_power.assert_awaited_with(
            "miraie/v1/control/dev_living",
            PowerMode.ON
        )

        await self.device.turn_off()
        self.mock_broker.set_power.assert_awaited_with(
            "miraie/v1/control/dev_living",
            PowerMode.OFF
        )

    async def test_set_temperature(self):
        """Test set_temperature dispatches through broker."""
        await self.device.set_temperature(23.5)
        self.mock_broker.set_temperature.assert_awaited_with(
            "miraie/v1/control/dev_living",
            23.5
        )

    async def test_set_hvac_mode(self):
        """Test set_hvac_mode dispatches through broker."""
        await self.device.set_hvac_mode(HVACMode.FAN)
        self.mock_broker.set_hvac_mode.assert_awaited_with(
            "miraie/v1/control/dev_living",
            HVACMode.FAN
        )

    async def test_set_converti_mode(self):
        """Test set_converti_mode dispatches through broker."""
        await self.device.set_converti_mode(ConvertiMode.C55)
        self.mock_broker.set_converti_mode.assert_awaited_with(
            "miraie/v1/control/dev_living",
            ConvertiMode.C55
        )

    async def test_set_preset_mode(self):
        """Test preset mode transitions."""
        await self.device.set_preset_mode(PresetMode.BOOST)
        self.mock_broker.set_preset_mode.assert_awaited_with(
            "miraie/v1/control/dev_living",
            PresetMode.BOOST
        )

    async def test_headless_device_safe_close(self):
        """Test headless device (broker=None) can be closed safely without errors."""
        headless_dev = Device(
            id="headless_1",
            name="Headless AC",
            friendly_name="Headless AC",
            control_topic="ctrl",
            status_topic="stat",
            connection_status_topic="conn",
            broker=None,
        )
        headless_dev.close()


if __name__ == "__main__":
    unittest.main()
