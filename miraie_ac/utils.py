# Write a function check if the given string is a valid email address.

import re


def is_valid_email(addr):
    if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", addr):
        return True
    else:
        return False


def toFloat(value: str) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_room_temp(value: str, firmware_version: str = "") -> float | None:
    """Parse rmtmp, accounting for sub-degree high-resolution format in firmware 3.02+."""
    if not value:
        return None

    try:
        cleaned_version = "".join(c for c in firmware_version if c.isdigit() or c == '.')
        major, minor = cleaned_version.split('.')[:2]
        is_packed_firmware = (int(major), int(minor)) >= (3, 2)
    except (ValueError, AttributeError):
        is_packed_firmware = False

    if is_packed_firmware and '.' in value:
        try:
            prefix_str, temp_str = value.split('.')
            integer_temp = float(temp_str)
            if integer_temp <= 0:
                return None
            prefix_byte = int(prefix_str)
            return round(integer_temp + (prefix_byte / 256.0), 2)
        except (ValueError, IndexError):
            return toFloat(value)

    return toFloat(value)