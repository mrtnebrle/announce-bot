"""Constants for announce-bot."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Announce Bot"
DOMAIN = "announce_bot"
VERSION = "0.0.0"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

OPENAI_KEY = "openai_key"
SENSORS = "sensors"
ELEVEN_API_KEY = "eleven_api_key"
ELEVENLABS_API_KEY = "elevenlabs_api_key"
ELEVENLABS_VOICE_ID = "elevenlabs_voice_id"
