import logging
from datetime import datetime, timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.cover import (
    ATTR_POSITION,
    ATTR_TILT_POSITION,
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
    PLATFORM_SCHEMA
)

from warema_wms import Shade, WmsController

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Warema WMS WebControl cover platform from a config entry."""
    
    url = config_entry.data["webcontrol_server_addr"]
    update_interval = config_entry.data["update_interval"]

    _LOGGER.debug("URL: {}".format(url))

    # Create an instance of the WMSWebControl library
    wms_client = WmsController(url)

    shades = Shade.get_all_shades(wms_client, time_between_cmds=0.5)

    _LOGGER.debug("SHADES: {}".format(shades))

    async_add_entities(WaremaShade(s, update_interval) for s in shades)

class WaremaShade(CoverEntity):
    """Represents a warema shade"""

    def __init__(self, shade, update_interval: int):
        self._name = f"Warema WMS Cover ({webcontrol_server_addr})"
        self.shade = shade
        self.room = shade.get_room_name()
        self.channel = shade.get_channel_name()
        self.position = 0
        self.last_position = self.position
        self.is_moving = False
        self.state_last_updated = datetime.now()
        self.next_state_upate = datetime.now()
        '''This is needed because, when a move is triggered by HA, sometimes the next status update
        still reports 'not moving' because shitty warema hasn't caught up with reality yet
        and then the next update is delayed until for update_interval seconds'''
        self.force_update_until = datetime.now()
        self.update_interval = update_interval

    def update(self, force=False):
        if datetime.now() > self.next_state_upate or self.is_moving\
                or datetime.now() < self.force_update_until or force:
            self.last_position = self.position
            self.position, self.is_moving, self.state_last_updated = \
                self.shade.get_shade_state(True)
            if self.state_last_updated:
                self.next_state_upate = \
                    self.state_last_updated \
                    + timedelta(seconds=self.update_interval)
            _LOGGER.debug('Update performed for {}'.format(self.name))
        else:
            _LOGGER.debug('Update skipped for {}. Next update {}'
                          .format(self.name, self.next_state_upate))

    @property
    def device_class(self):
        return DEVICE_CLASS_SHADE

    @property
    def supported_features(self):
        return SUPPORT_OPEN|SUPPORT_CLOSE|SUPPORT_SET_POSITION

    @property
    def unique_id(self):
        return 'warema_shade' + self.name

    @property
    def name(self):
        return "{}:{}".format(self.room, self.channel)

    @property
    def current_cover_position(self):
        return 100 - self.position

    @property
    def is_opening(self):
        if self.is_moving and self.last_position > self.position:
            return True
        else:
            return False

    @property
    def is_closing(self):
        if self.is_moving and self.last_position < self.position:
            return True
        else:
            return False

    @property
    def is_closed(self):
        if not self.is_moving and self.position == 100:
            return True
        else:
            return False

    def open_cover(self, **kwargs):
        self.force_update_until = datetime.now() + timedelta(seconds=15)
        self.shade.set_shade_position(0)

    def close_cover(self, **kwargs):
        self.force_update_until = datetime.now() + timedelta(seconds=15)
        self.shade.set_shade_position(100)

    def set_cover_position(self, **kwargs):
        self.force_update_until = datetime.now() + timedelta(seconds=15)
        self.shade.set_shade_position(100 - kwargs[ATTR_POSITION])

