import asyncio
from pydub import AudioSegment
from pydub.playback import play
from discord_bot import TimerBot

RUNNING = 1
IDLE = 2
FIRST = 3
SECOND = 4
USE_DISCORD = 1

class Timer:
    def __init__(self, seconds,minutes,use_discord,audio_queue,client = None,voice_channel_id = None,guild_id = None):
        self.seconds = 3+seconds + (minutes * 60)-7
        self.seconds2 = (seconds + (minutes * 60))*3
        self.remaining = self.seconds
        self.number = FIRST
        self.state = IDLE
        self.use_discord = use_discord
        self.audio_queue = audio_queue
        self.client = client
        self.voice_channel_id = voice_channel_id
        self.guild_id = guild_id

    async def start(self):
        self.state = RUNNING
        while self.remaining > 0:
            print(f"Remaining: {self.remaining}                    ", end="\r")
            await asyncio.sleep(1)
            if self.state == RUNNING:
                self.remaining -= 1
        if self.state == RUNNING:
            if self.number == FIRST:
                if self.use_discord == USE_DISCORD:
                    #音声再生
                    print("first Time's up! for Discord", end="\r")
                    await self.client.play_audio(self.guild_id, self.voice_channel_id, "sound/toan.mp3")
                else:
                    print("first Time's up!", end="\r")
                    await self.play_audio("sound/toan.mp3") 
                self.remaining = self.seconds2
                self.number = SECOND 
                await self.start()
            elif self.number == SECOND:
                if self.use_discord:
                    print("second Time's up! for Discord true", end="\r")
                    await self.client.play_audio(self.guild_id, self.voice_channel_id, "sound/toan_extension.mp3")
                else:
                    #音声再生
                    print("second Time's up!", end="\r")
                    await self.play_audio("sound/toan_extension.mp3") 
                self.remaining = self.seconds
                self.number = FIRST
                self.state = IDLE

    def reset(self):
        self.remaining = self.seconds
        self.number = FIRST


    async def play_audio(self, file_path):
        print("playback tona.mp3!",end="\r")
        audio = AudioSegment.from_file(file_path)
        play(audio)