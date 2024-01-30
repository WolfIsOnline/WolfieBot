"""Voice Manager"""
from elevenlabs import set_api_key, generate, save
from moviepy.editor import ImageClip, AudioFileClip

import wolfiebot
from wolfiebot.logger import Logger

log = Logger(__name__, wolfiebot.LOG_LEVEL)


class VoiceManager:
    """Manages Voices"""

    BASE_PATH = "./wolfiebot/content"
    AUDIO_PATH = f"{BASE_PATH}/reply.wav"
    IMAGE_PATH = f"{BASE_PATH}/wolfie.jpg"
    OUTPUT_PATH = f"{BASE_PATH}/reply.mp4"
    VOICE = "maya"
    MODEL = "eleven_multilingual_v2"

    def __init__(self, text: str):
        self.text = text
        self.audio = None
        set_api_key(wolfiebot.ELEVENLABS_API_KEY)

    def generate_reply(self):
        if self.text is None or self.text == "":
            log.error(
                'generate_reply():  invalid string. text can\'t be equal "%s"',
                self.text,
            )
            return

        log.debug("generate_reply(): generating speech...")
        self.audio = generate(text=self.text, voice=self.VOICE, model=self.MODEL)
        log.debug(
            'generate_reply(): audio has been generated with "%s" voice using model "%s"',
            self.VOICE,
            self.MODEL,
        )

    def save_audio(self):
        if self.audio is None:
            return
        save(self.audio, self.AUDIO_PATH)
        log.debug("save_audio(): saved audio to %s", self.AUDIO_PATH)

    def convert_to_video(self):
        audio = AudioFileClip(self.AUDIO_PATH)

        image = ImageClip(self.IMAGE_PATH)
        # pylint: disable=no-member
        image = image.resize((150, 150))
        image = image.set_duration(audio.duration)

        video = image.set_audio(audio)
        video.write_videofile(
            self.OUTPUT_PATH,
            codec="libx264",
            audio_codec="aac",
            fps=24,
            verbose=False,
            logger=None,
        )
