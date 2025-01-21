"""Warema WMS WebControl Integration."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Warema WMS WebControl integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Warema WMS WebControl from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Add the cover entity
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "cover")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)

    # Remove the cover entity
    await hass.config_entries.async_forward_entry_unload(entry, "cover")
    return True
