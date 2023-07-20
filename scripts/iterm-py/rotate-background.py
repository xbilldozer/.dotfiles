#!/usr/bin/env python3.7
import glob
import asyncio
import iterm2
import random

_wallpapers = []


def load_wallpapers():
    if len(_wallpapers):
        return _wallpapers
    path = '/Users/altonwi/src/wallpapers/**/*.'
    extensions = ['bmp', 'jpeg', 'jpg', 'png']
    for ext in extensions:
        _wallpapers.extend(glob.glob(f'{path}{ext}', recursive=True))
    return _wallpapers


async def change_background(app):
    session = app.current_terminal_window.current_tab.current_session
    profile = await session.async_get_profile()
    wallpaper = random.choice(_wallpapers)
    print(f'setting to {wallpaper}')
    await profile.async_set_background_image_location(wallpaper)


async def poll_change_background(app):
    while True:
        await change_background(app)
        await asyncio.sleep(30 * 60)


async def main(connection):
    tasks = []
    app = await iterm2.async_get_app(connection)
    load_wallpapers()
    global task
    task = asyncio.create_task(change_background(app))
    tasks.append(task)

    async def keystroke_handler(keystroke, app):
        """This function is called every time a key is pressed."""
        if keystroke.keycode != iterm2.Keycode.F9:
            return
        if keystroke.modifiers == [iterm2.Modifier.FUNCTION]:
            for task in tasks:
                task.cancel()
                print('task canceled')

            task = asyncio.create_task(change_background(app))
            tasks.append(task)

    # Monitor the keyboard
    async with iterm2.KeystrokeMonitor(connection) as mon:
        while True:
            keystroke = await mon.async_get()
            await keystroke_handler(keystroke, app)

iterm2.run_forever(main)
