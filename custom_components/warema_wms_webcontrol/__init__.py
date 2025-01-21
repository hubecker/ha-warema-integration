"""Warema WMS WebControl Integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import Platform

from . import hub

import logging

from .const import (
    DOMAIN
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.COVER]

type HubConfigEntry = ConfigEntry[hub.Hub]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Warema WMS WebControl integration."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Warema WMS WebControl from a config entry."""
    # hass.data[DOMAIN][entry.entry_id] = entry.data
    entry.runtime_data = hub.Hub(hass, entry.data["host"])

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # This is called when an entry/configured device is to be removed. The class
    # needs to unload itself, and remove callbacks. See the classes for further
    # details
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    return unload_ok
