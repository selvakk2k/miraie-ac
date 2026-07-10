# MirAIe-AC-IN API for Python

A fork of [rkzofficial/miraie-ac](https://github.com/rkzofficial/miraie-ac), focused on Panasonic MirAIe AC models sold in India. This is a clean break from upstream — fixes and features here are scoped to Indian-market models and firmware, and are not intended to track or merge back into the original project.

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
    custom_components.miraie: debug
    ...
```

### Notes
[List of panasonic ACs](https://www.panasonic.com/in/consumer/air-conditioners/split-ac/?browsing=params&sort=Featured&page=1)
