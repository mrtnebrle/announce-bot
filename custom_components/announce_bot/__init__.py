"""Custom integration to integrate announce-bot with Home Assistant.

For more details about this integration, please refer to
https://github.com/mrtnebrle/announce-bot
"""
from __future__ import annotations

from homeassistant.const import EVENT_HOMEASSISTANT_START
import homeassistant.helpers.config_validation as cv

from .announce_bot import AnnounceBot

from .const import (
    DOMAIN,
    SENSORS,
    OPENAI_KEY,
    ELEVEN_API_KEY,
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    LOGGER
)

import voluptuous as vol
import threading

REQ_LOCK = threading.Lock()
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(OPENAI_KEY): cv.string,
            vol.Required(ELEVEN_API_KEY): cv.string,
            vol.Required(ELEVENLABS_API_KEY): cv.string,
            vol.Required(ELEVENLABS_VOICE_ID): cv.string,
            vol.Required(SENSORS): cv.ensure_list,
        })
    },
    extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
    """Set up Custom Component."""
    conf = config[DOMAIN]
    openai_key = conf.get(OPENAI_KEY)
    sensors = conf.get(SENSORS)

    def prepare(event):
        AnnounceBot(hass, sensors, openai_key)

    hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)
    hass.data.setdefault(DOMAIN, {})

    return True
