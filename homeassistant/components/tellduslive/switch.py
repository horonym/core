"""Support for Tellstick switches using Tellstick Net."""
from homeassistant.components import switch, tellduslive
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entry import TelldusLiveEntity


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up tellduslive sensors dynamically."""

    async def async_discover_switch(device_id):
        """Discover and add a discovered sensor."""
        client = hass.data[tellduslive.DOMAIN]
        async_add_entities([TelldusLiveSwitch(client, device_id)])

    async_dispatcher_connect(
        hass,
        tellduslive.TELLDUS_DISCOVERY_NEW.format(switch.DOMAIN, tellduslive.DOMAIN),
        async_discover_switch,
    )


class TelldusLiveSwitch(TelldusLiveEntity, ToggleEntity):
    """Representation of a Tellstick switch."""

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.device.is_on

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self.device.turn_on()
        self._update_callback()

    def turn_off(self, **kwargs):
        """Turn the switch off."""
        self.device.turn_off()
        self._update_callback()
