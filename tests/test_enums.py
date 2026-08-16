"""Unit tests for miraie_ac enums and conversion logic."""

import unittest
from miraie_ac.enums import (
    PowerMode,
    HVACMode,
    FanMode,
    PresetMode,
    SwingMode,
    ConvertiMode,
    DisplayMode,
    ConsumptionPeriodType,
)


class TestEnums(unittest.TestCase):
    """Test Enum mappings and values."""

    def test_power_modes(self):
        self.assertEqual(PowerMode("on"), PowerMode.ON)
        self.assertEqual(PowerMode("off"), PowerMode.OFF)

    def test_hvac_modes(self):
        self.assertEqual(HVACMode("cool"), HVACMode.COOL)
        self.assertEqual(HVACMode("dry"), HVACMode.DRY)
        self.assertEqual(HVACMode("fan"), HVACMode.FAN)
        self.assertEqual(HVACMode("auto"), HVACMode.AUTO)

    def test_swing_modes(self):
        self.assertEqual(SwingMode(0), SwingMode.AUTO)
        self.assertEqual(SwingMode(1), SwingMode.ONE)
        self.assertEqual(SwingMode(5), SwingMode.FIVE)

    def test_converti_modes(self):
        self.assertEqual(ConvertiMode(0), ConvertiMode.OFF)
        self.assertEqual(ConvertiMode(40), ConvertiMode.C40)
        self.assertEqual(ConvertiMode(55), ConvertiMode.C55)
        self.assertEqual(ConvertiMode(70), ConvertiMode.C70)
        self.assertEqual(ConvertiMode(80), ConvertiMode.C80)
        self.assertEqual(ConvertiMode(90), ConvertiMode.C90)
        self.assertEqual(ConvertiMode(100), ConvertiMode.FC)
        self.assertEqual(ConvertiMode(110), ConvertiMode.HC)

    def test_consumption_period_types(self):
        self.assertEqual(ConsumptionPeriodType.DAILY.value, "Daily")
        self.assertEqual(ConsumptionPeriodType.WEEKLY.value, "Weekly")
        self.assertEqual(ConsumptionPeriodType.MONTHLY.value, "Monthly")
        self.assertEqual(ConsumptionPeriodType.DAILY.response_key(), "day")
        self.assertEqual(ConsumptionPeriodType.WEEKLY.response_key(), "week")
        self.assertEqual(ConsumptionPeriodType.MONTHLY.response_key(), "month")


if __name__ == "__main__":
    unittest.main()
