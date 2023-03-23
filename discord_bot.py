import discord


class TimerBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord!')
        self.bot_ready = True

    async def join_voice_channel(self, guild_id, voice_channel_id):
        guild = self.get_guild(guild_id)
        voice_channel = guild.get_channel(voice_channel_id)
        await voice_channel.connect()

    async def play_audio(self, guild_id, voice_channel_id, file_path):
        guild = self.get_guild(guild_id)
        voice_client = guild.voice_client

        # 音声ファイルを再生する
        source = discord.FFmpegPCMAudio(file_path)
        voice_client.play(source)
