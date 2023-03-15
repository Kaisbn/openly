# Openly

![main](https://github.com/kaisbn/openly/actions/workflows/branch.yaml/badge.svg?branch=main)
![release](https://github.com/kaisbn/openly/actions/workflows/release.yaml/badge.svg)

Openly is a Python API wrapper for simple access to the Rently Smart Home API.

**DISCLAIMER**: Rently is a registered trademark of Consumer 2.0 Inc., which I'm not affiliated to.
This is not an official wrapper.

Rently provides a publicly available documentation, which was very helpful to create this library:

[Rently API Documentation](https://apidocs.rently.com)

Shoutout to Rently's engineering team who provide us with very interesting reads on their blog:

[Rently Engineering Blog](https://engineering.rently.com)

## Installation

> :globe_with_meridians: **Coming soon** - For now, clone the repo and install from local files using `pip` or `poetry`

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the library.

```bash
pip install openly-core
```

## Usage

```python
from openly import RentlyCloud

cloud = RentlyCloud("BASE URL HERE", "BASE LOGIN URL HERE")

# Login to retrieve your token
cloud.login(username, password) # Set username and password here

# Retrieve the list of hubs
cloud.get_hubs()

# Retrieve information about a single hub
cloud.get_hubs()

# Retrieve the list of devices in a hub
cloud.get_devices("HUB ID") # Set hub id here
```

## Implementation

The library currently supports the following devices:

- Hub
- Dimmer
- Leak Sensor
- Lock
- Switch
- Thermostat

Each device is represented by a class that implements the actions supported by the API. Example:

```python
    # Retrieve the door lock
    door = cloud.get_device("DEVICE ID HERE")

    # Call the device locking action
    door.lock()

    # Call the device unlocking action
    door.unlock()
```

```python
    # Retrieve the switch
    switch = cloud.get_device("DEVICE ID HERE")

    # Call the device `on` action
    switch.on()

    # Call the device `off` action
    switch.off()
```

More information about each device can be found in the corresponding class in `openly/devices`.
Some resources or actions might not be supported currently. I will work on adding them gradually.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

Refer to `LICENSE` file
