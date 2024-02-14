"""Announce Bot Implementation."""
import base64
import errno
import time

from homeassistant.core import HomeAssistant

from homeassistant.helpers.event import track_state_change
from homeassistant.helpers import entity_registry
from homeassistant.helpers import device_registry

from homeassistant.const import STATE_ON
from httpx import TimeoutException

from openai import OpenAI

from .const import LOGGER

class AnnounceBot:
    """Implementation."""

    scripts = []

    def __init__(
        self,
        hass: HomeAssistant,
        sensors: dict,
        openai_key: str) -> None:
        """Initialize."""

        self.hass = hass
        self.entity_registry = entity_registry.async_get(self.hass)
        self.device_registry = device_registry.async_get(self.hass)

        self.openai_client = OpenAI(api_key=openai_key)

        track_state_change(hass, sensors, self.state_changed)

    async def state_changed(self, entity_id, old_state, new_state):
        """When the state of one of the sensor changes and the state is on, proceed to explain the image."""

        if old_state is None or new_state is None:
            return

        if new_state.state == STATE_ON:
            entity = self.entity_registry.async_get(entity_id)
            if entity:
                device = self.device_registry.async_get(entity.device_id)
                if device:
                    image_path = await self.capture_snapshot(entity_id=device.id)
                    if image_path:
                        image_description = await self.analyze_snapshot(image_path=image_path)
                        LOGGER.info(image_description)

    async def analyze_snapshot(self, image_path: str) -> str:
        """Analyze snapshot."""
        image_b64encoded = None
        try:
            with open(image_path, "rb") as image_file:
                image_b64encoded = base64.b64encode(image_file.read()).decode("utf-8")
        except OSError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
                # File is being written to, wait a bit and retry
            time.sleep(0.1)

        if image_b64encoded:
            image_description = self.explain_image(base64_image=image_b64encoded)
            self.scripts = self.scripts + [{"role": "assistant", "content": image_description}]
            return image_description

    async def capture_snapshot(self, entity_id: str) -> str:
        """Capture snapshot from camera."""
        image_path = f"/config/.storage/snapshot_{entity_id}.jpg"
        LOGGER.debug("📸 Retrieving picture...")
        try:
            await self.hass.services.async_call("camera", "snapshot", {"device_id": entity_id, "filename": image_path}, blocking=True)
            return image_path
        except TimeoutException:
            LOGGER.warning("Timeout while waiting for camera snapshot service. Aborting...")
        return None

    def create_content(self, base64_image):
        """Create content for request."""

        return [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64, {base64_image}",
                    },
                ],
            },
        ]

    def explain_image(self, base64_image) -> str:
        """Explain image content."""

        response = self.openai_client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are Sir David Attenborough. Narrate the picture of what is being seen on the image as if it is a nature documentary.
                    Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                    """,
                },
            ]
            + self.scripts
            + self.create_content(base64_image),
            max_tokens=500,
        )
        return response.choices[0].message.content
