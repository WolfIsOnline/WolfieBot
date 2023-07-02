"""
Voice Module
"""
import logging
import lightbulb

from elevenlabs import set_api_key, voices, generate, save
from moviepy.editor import ImageClip, AudioFileClip

# pylint: disable=import-error
import wolfiebot


log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("ai.voice")
set_api_key(wolfiebot.ELEVENLABS_API_KEY)
BASE_PATH = "./WolfieBot/wolfiebot/content"
AUDIO_PATH = f"{BASE_PATH}/reply.mp3"
IMAGE_PATH = f"{BASE_PATH}/wolfie-pfp.png"
OUTPUT_PATH = f"{BASE_PATH}/reply.mp4"


def generate_reply(reply: str) -> None:
    """
    Generates an audio reply based on the provided text.

    Args:
        reply (str): The text to generate the audio reply from.

    Returns:
        None
    """

    voices()
    audio = generate(
        text=reply,
        api_key=wolfiebot.ELEVENLABS_API_KEY,
        voice="wolfie",
        model="eleven_multilingual_v1"
    )

    save(audio, AUDIO_PATH)
    audio = AudioFileClip(AUDIO_PATH)

    image = ImageClip(IMAGE_PATH)
    # pylint: disable=no-member
    image = image.resize((150, 150))
    image = image.set_duration(audio.duration)

    video = image.set_audio(audio)
    video.write_videofile(
        OUTPUT_PATH,
        codec='libx264',
        audio_codec='aac',
        fps=24,
        verbose=False,
        logger=None
    )
