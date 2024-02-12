"""Custom integration to integrate announce-bot with Home Assistant.

For more details about this integration, please refer to
https://github.com/mrtnebrle/announce-bot
"""
from __future__ import annotations

# import logging
# from token import OP

# from homeassistant.config_entries import ConfigEntry
# from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
# from homeassistant.core import HomeAssistant
from homeassistant.const import EVENT_HOMEASSISTANT_START
# from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .announce_bot import AnnounceBot

# from .api import AnnounceBotApiClient
from .const import DOMAIN, SENSORS, OPENAI_KEY, LOGGER
# from .coordinator import AnnounceBotDataUpdateCoordinator
import voluptuous as vol
import threading

# _LOGGER = logging.getLogger(__name__)

# PLATFORMS: list[Platform] = [
#     Platform.SENSOR,
#     Platform.BINARY_SENSOR,
#     Platform.SWITCH,
# ]

REQ_LOCK = threading.Lock()
CONFIG_SCHEMA = vol.Schema(
	{
		DOMAIN: vol.Schema({
			vol.Required(OPENAI_KEY): cv.string,
			vol.Required(SENSORS): cv.ensure_list
		})
	},
	extra=vol.ALLOW_EXTRA,
)

def setup(hass, config):
	conf = config[DOMAIN]
	openai_key = conf.get(OPENAI_KEY)
	sensors = conf.get(SENSORS)

	announce_bot = AnnounceBot(hass, openai_key, sensors)

	# rf = rcswitch.RCSwitch(comport, speed=comspeed)
	# rf.libWaitForAck(True, timeout=1)

	def cleanup(event):
		LOGGER.info("cleanup")
		# rf.cleanup()

	def prepare(event):
		LOGGER.info("prepare")
		# rf.prepare()
		# rf.startReceivingThread()
		# hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, cleanup)

	hass.bus.listen_once(EVENT_HOMEASSISTANT_START, prepare)
	hass.data.setdefault(DOMAIN, {})
	# hass.data[DOMAIN] = rf

	return True

# # https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
# async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Set up this integration using UI."""
#     hass.data.setdefault(DOMAIN, {})
#     hass.data[DOMAIN][entry.entry_id] = coordinator = AnnounceBotDataUpdateCoordinator(
#         hass=hass,
#         client=AnnounceBotApiClient(
#             username=entry.data[CONF_USERNAME],
#             password=entry.data[CONF_PASSWORD],
#             session=async_get_clientsession(hass),
#         ),
#     )
#     # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
#     await coordinator.async_config_entry_first_refresh()

#     await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
#     entry.async_on_unload(entry.add_update_listener(async_reload_entry))

#     return True


# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
#     """Handle removal of an entry."""
#     if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
#         hass.data[DOMAIN].pop(entry.entry_id)
#     return unloaded


# async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
#     """Reload config entry."""
#     await async_unload_entry(hass, entry)
#     await async_setup_entry(hass, entry)