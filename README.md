# MirAIe AC API Client (`miraie-ac-in`)

[![PyPI version](https://badge.fury.io/py/miraie-ac-in.svg)](https://badge.fury.io/py/miraie-ac-in)
[![Python Version](https://img.shields.io/pypi/pyversions/miraie-ac-in.svg)](https://pypi.org/project/miraie-ac-in/)
[![Version](https://img.shields.io/github/v/release/selvakk2k/miraie-ac-in?style=flat-square)](https://github.com/selvakk2k/miraie-ac-in/releases)
[![AI-Assisted](https://img.shields.io/badge/AI%20Assisted-Antigravity%20%7C%20Claude-blueviolet?style=flat-square&logo=google)](https://github.com/selvakk2k)
[![AI Attribution](https://img.shields.io/badge/AI%20Attribution-AIA%20PAI%20Nc%20Hin-orange?style=flat-square)](https://aiattribution.github.io/interpret-attribution)

A Python API client wrapper for controlling Panasonic MirAIe-enabled Air Conditioners. This library handles MQTT message parsing, connection loops, and telemetry status decoding.

This repository is a feature fork of `rkzofficial/miraie-ac` to provide updates for newer firmware versions, expand capacity control options, and improve connection stability.

> [!IMPORTANT]
> This project is designed **exclusively** for Panasonic Air Conditioners that use the **MirAIe** application. It is **not compatible** with Panasonic ACs that use the global **Comfort Cloud** application.

---

## Enhancements in This Fork

* **Firmware 3.02+ Room Temperature Fix**: Panasonic AC units running firmware `3.02+` report ambient room temperature in a packed decimal format. This fork introduces version-aware decoding to display this value correctly, while retaining traditional decoding for older firmware.
* **Converti 8-in-1 Support**: Expands compressor capacity control options by mapping the `60%` and `50%` steps, enabling full 8-in-1 capacity features on supported models.
* **MQTT & Resource Lifecycle Cleanup**: Adds an explicit `close()` method to cleanly cancel and await active MQTT tasks and terminate the underlying HTTP client session, preventing resource leaks.
* **Telemetry Parsing**: Adds status parsing for Nanoe™ air purifiers (`acng`), Filter Clean alerts (`acfc`), Wi-Fi RSSI signal strength (`rssi`), and last control source (`cnt`).
* **Input Validation**: Upgraded user credential validation with improved regex supporting subdomains and hyphenated domains.

---

## Installation

Install the package via `pip`:

```bash
pip install miraie-ac-in
```

---

## Quick Start

```python
import asyncio
from miraie_ac import MirAIeHub, MirAIeBroker

async def main():
    broker = MirAIeBroker()
    hub = MirAIeHub()

    # Initialize the hub (phone number format: +91XXXXXXXXXX)
    await hub.init("+919999999999", "your_password", broker)
    
    # List discovered devices
    print("Discovered Devices:", hub.home.devices)
    
    # Wait for the MQTT connection to establish
    while not hasattr(broker, "client") or getattr(broker, "client") is None:
        await asyncio.sleep(1)

    # Example: Turn off the first device
    if hub.home.devices:
        device = hub.home.devices[0]
        await device.turn_off()
        
    await hub.close()

asyncio.run(main())
```

---

## Credits & License

### Upstream Authors & Contributors
* Originally authored and developed by [@rkzofficial](https://github.com/rkzofficial).
* Features contributed by upstream community developers: [@deCodeIt](https://github.com/deCodeIt), [@gutpull](https://github.com/gutpull), and [@ankitduseja](https://github.com/ankitduseja).

### Fork Maintainers & Contributors
* **Lead Architecture & API Design**: [@selvakk2k](https://github.com/selvakk2k) — physical device telemetry capture, MQTT protocol analysis, and domain requirements.
* **Code Implementation & Engineering**: **Antigravity** (Google DeepMind) — asyncio MQTT connection lifecycles, memory leak resolution, Converti 8-in-1 decoding, and pytest suite.
* **Pre-Release Code Review & Auditing**: **Claude** (Anthropic) — independent architectural review, code audits, and edge-case verification.

Licensed under the **MIT License**. See the `LICENSE` file for the original license text.
