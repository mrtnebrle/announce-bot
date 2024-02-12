"""Announce Bot Implementation."""
from homeassistant.core import HomeAssistant

from homeassistant.helpers.event import track_state_change

from .const import LOGGER

class AnnounceBot:
    """Implementation."""

    def __init__(
        self,
        hass: HomeAssistant,
        sensors: dict) -> None:
        """Initialize."""
        track_state_change(hass, sensors, self.state_changed)

    def state_changed(entity_id, old_state, new_state):
        """When state changes."""
        if old_state is None or new_state is None:
            return

        LOGGER.info("state changed")
