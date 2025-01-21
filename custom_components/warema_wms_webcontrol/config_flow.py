from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class WaremaWMSWebControlConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Warema WMS WebControl."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            url = user_input.get("url")
            update_interval = user_input.get("update_interval")

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
                vol.Required("url", default="http://192.168.1.100"): str,
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
