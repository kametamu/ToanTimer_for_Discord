import asyncio
import configparser
from pynput import keyboard
import discord
import threading
import time
from discord_bot import TimerBot

from timer import Timer, RUNNING, IDLE,FIRST,SECOND,USE_DISCORD

def on_press(key, queue, start_hotkey):
    try:
        k = key.char
    except AttributeError:
        k = key.name
    if k == start_hotkey:
        queue.put_nowait("start")

def hotkey_detection(queue, start_hotkey):
    with keyboard.Listener(on_press=lambda key: on_press(key, queue, start_hotkey)) as listener:
        listener.join()

async def main():
    client = None
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    timer_seconds = int(config.get('settings', 'timer_seconds'))
    timer_minutes = int(config.get('settings', 'timer_minutes'))
    start_hotkey = config.get('settings', 'start_hotkey')
    use_discord = int(config.get('settings', 'use_discord'))

    token = config.get('discord', 'token')
    voice_channel_id = int(config.get('discord', 'voice_channel'))
    guild_id = int(config.get('discord', 'guild_id'))

    audio_queue = asyncio.Queue()

    print(f"loading...")

    queue = asyncio.Queue()
    hotkey_thread = threading.Thread(target=hotkey_detection, args=(queue, start_hotkey))
    hotkey_thread.start()

    if use_discord == USE_DISCORD:
        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False

        client = TimerBot(intents=intents)
        client.bot_ready = False
        client_task = asyncio.create_task(client.start(token))

        while not client.bot_ready:
            await asyncio.sleep(0.1)

        await client.join_voice_channel(guild_id, voice_channel_id)

    timer_instance = Timer(timer_seconds,timer_minutes,use_discord,audio_queue,client,voice_channel_id,guild_id)
    print(f"Press '{start_hotkey}' to start.")

    main_loop_start_time = time.time()

    while True:
        try:
            key_event = await asyncio.wait_for(queue.get(), timeout=0.1)
        except asyncio.TimeoutError:
            continue
        if key_event == "start":
            if timer_instance.state == IDLE:
                print(f"Timer start               ", end="\r")
                timer_task = asyncio.create_task(timer_instance.start())
            else:
                print(f"Timer reset              ", end="\r")
                timer_instance.reset()

        # 他の処理をブロックしないために、少し待機します。
        await asyncio.sleep(0.1)

    hotkey_thread.join()
    await client_task
    await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
