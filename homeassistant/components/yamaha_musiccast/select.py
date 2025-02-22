"""The select entities for musiccast."""
from __future__ import annotations

from aiomusiccast.capabilities import OptionSetter

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, MusicCastCapabilityEntity, MusicCastDataUpdateCoordinator
from .const import DEVICE_CLASS_MAPPING


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up MusicCast select entities based on a config entry."""
    coordinator: MusicCastDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    select_entities = []

    for capability in coordinator.data.capabilities:
        if isinstance(capability, OptionSetter):
            select_entities.append(SelectableCapapility(coordinator, capability))

    for zone, data in coordinator.data.zones.items():
        for capability in data.capabilities:
            if isinstance(capability, OptionSetter):
                select_entities.append(
                    SelectableCapapility(coordinator, capability, zone)
                )

    async_add_entities(select_entities)


class SelectableCapapility(MusicCastCapabilityEntity, SelectEntity):
    """Representation of a MusicCast Select entity."""

    capability: OptionSetter

    async def async_select_option(self, option: str) -> None:
        """Select the given option."""
        value = {val: key for key, val in self.capability.options.items()}[option]
        await self.capability.set(value)

    @property
    def device_class(self) -> str | None:
        """Return the device class, to identify the entity for translations."""
        return DEVICE_CLASS_MAPPING.get(self.capability.id)

    @property
    def options(self):
        """Return the list possible options."""
        return list(self.capability.options.values())

    @property
    def current_option(self):
        """Return the currently selected option."""
        return self.capability.options[self.capability.current]
