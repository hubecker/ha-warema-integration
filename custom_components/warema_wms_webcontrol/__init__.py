<<<<<<< HEAD
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

DOMAIN = "warema_wms_control"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the custom cover integration."""
=======
"""Warema WMS WebControl Integration."""

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Warema WMS WebControl integration."""
>>>>>>> 11cc338 (update)
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
<<<<<<< HEAD
    """Set up the custom cover from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data
=======
    """Set up Warema WMS WebControl from a config entry."""
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Add the cover entity
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "cover")
    )
>>>>>>> 11cc338 (update)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id)
<<<<<<< HEAD
    return True
=======

    # Remove the cover entity
    await hass.config_entries.async_forward_entry_unload(entry, "cover")
    return True
>>>>>>> 11cc338 (update)
