from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN  # pylint:disable=unused-import
from .hub import Hub

_LOGGER = logging.getLogger(__name__)


class WaremaWMSWebControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Warema WMS WebControl."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            url = user_input.get("webcontrol_server_addr")
            update_interval = user_input.get("update_interval")

            hub = Hub(hass, data["webcontrol_server_addr"])
            # The dummy hub provides a `test_connection` method to ensure it's working
            # as expected
            result = await hub.test_connection()
            if not result:
                # If there is an error, raise an exception to notify HA that there was a
                # problem. The UI will also show there was a problem
                raise CannotConnect


            # Validate URL and update interval
            if not self._is_valid_url(url):
                errors["url"] = "invalid_url"
            elif update_interval < 5:
                errors["update_interval"] = "too_short"
            else:
                return self.async_create_entry(title=f"Cover ({url})", data=user_input)

        # Schema for the form
        data_schema = vol.Schema(
            {
                vol.Required("webcontrol_server_addr", default="http://192.168.178.73"): str,
                vol.Optional("update_interval", default=30): int,
            }
        )
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    def _is_valid_url(url):
        """Validate a URL."""
        from urllib.parse import urlparse

        parsed = urlparse(url)
        return all([parsed.scheme in ("http", "https"), parsed.netloc])

class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""

