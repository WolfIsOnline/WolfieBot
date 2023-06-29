import logging
import hikari
import wolfiebot
import lightbulb

from elevenlabs import set_api_key, voices, generate, save
from moviepy.editor import *

log = logging.getLogger(__name__)
plugin = lightbulb.Plugin("ai.voice")
set_api_key(wolfiebot.ELEVENLABS_API_KEY)


def generate_reply(reply: str):
    base_path = "./WolfieBot/wolfiebot/ai"
    audio_path = f"{base_path}/reply.mp3"
    image_path = f"{base_path}/wolfie-pfp.png"
    output_path = f"{base_path}/reply.mp4"
    
    log.info("generating audio")
    voices()
    audio = generate(text=reply, api_key=wolfiebot.ELEVENLABS_API_KEY, voice="wolfie", model="eleven_multilingual_v1")
    save(audio, audio_path)
    
    audio = AudioFileClip(audio_path)

    log.info("converting audio to mp4")
    image = ImageClip(image_path)
    image = image.resize((150, 150))
    image = image.set_duration(audio.duration)

    video = image.set_audio(audio)
    video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24, verbose=False, logger=None)
    
def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)

