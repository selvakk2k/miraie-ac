# MirAIe-AC-IN API for Python

A fork of [rkzofficial/miraie-ac](https://github.com/rkzofficial/miraie-ac), to expand features and add hardware-specific adaptations that may break if merged with upstream.

### Installation

```
pip install miraie-ac-in
```

### Get started

```Python
import asyncio
from miraie_ac import MirAIeHub, MirAIeBroker

async def setup():
  # Instantiate a MirAIeHub object
  broker = MirAIeBroker()

  # Instantiate a MirAIeHub object
  hub = MirAIeHub()

  # Intialize the hub (+91xxxxxxxxxx, password, broker)
  await hub.init("<mobile>", "<password>", broker)
  
  # Display list of available devices
  print( hub.home.devices )
  
  # Wait till connection has been established with the broker
  async def waitForClient():
    while not hasattr(broker, 'client') or getattr(broker, 'client') is None:
      await asyncio.sleep(1)
  await waitForClient()

  # Now you can run any operation on the device(s)
  hub.home.devices[0].turn_off()
    
asyncio.run(setup())


```

### Logs can be enabled in Home Assistant as follows

```
logger:
  ...
  logs:
    ...
    custom_components.miraie_in: debug
    ...
```

### Notes
[List of panasonic ACs](https://www.panasonic.com/in/consumer/air-conditioners/split-ac/?browsing=params&sort=Featured&page=1)

---

## Fork Features
* **Firmware 3.02+ Room Temperature Fix**: Parsed packed room temperature string values based on version checking.
* **Converti 8-in-1 support**: Added extra enums for 60% and 50% capacity modes.
* **Stability Improvement**: Implemented `close()` method to cancel/await active MQTT loop tasks and close the HTTP ClientSession cleanly, preventing process/resource leaks.
* **Email Validation**: Upgraded the email regex to support subdomains and hyphenated domains (e.g. `user@mail.co.uk`).
* **Sensor/Control Parsing**: Added parsing of `acng` (Nanoe), `acfc` (Filter Clean), `rssi` (Wi-Fi RSSI), and `cnt` (Control Source).

## Credits
This fork was developed with the assistance of [Claude](https://claude.ai) (Anthropic) and [Antigravity](https://github.com/google-deepmind) (Google DeepMind).
