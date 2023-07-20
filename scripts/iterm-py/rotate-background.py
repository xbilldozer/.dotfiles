#!/usr/bin/env python3.7
import asyncio
import glob
import iterm2
import random
import subprocess
import os

_last_wallpaper = ''
_path = f'/usr/local/bin/:{os.environ.get("PATH")}'
_tasks = []
_wallpapers = []
_wp_path = '/Users/altonwi/src/personal/wallpapers/**/*.'
MAPPINGS = ['apple', 'md770']
MODIFIERS = {
    'md770': [iterm2.Modifier.CONTROL, iterm2.Modifier.OPTION],
    'apple': [iterm2.Modifier.FUNCTION]
}
KEYCODES = {
    'info': {
        'apple': {
            'key': iterm2.Keycode.ANSI_I,
            'modifier': [iterm2.Modifier.CONTROL,
                         iterm2.Modifier.OPTION]},
        'md770': {
            'key': iterm2.Keycode.ANSI_I,
            'modifier': [iterm2.Modifier.CONTROL,
                         iterm2.Modifier.OPTION]}},
    'next': {
        'apple': {
            'key': iterm2.Keycode.F9,
            'modifier': [iterm2.Modifier.FUNCTION]},
        'md770': {
            'key': iterm2.Keycode.ANSI_N,
            'modifier': [iterm2.Modifier.CONTROL,
                         iterm2.Modifier.OPTION]}},
    'reload': {
        'apple': {
            'key': iterm2.Keycode.F5,
            'modifier': [iterm2.Modifier.FUNCTION]},
        'md770': {
            'key': iterm2.Keycode.ANSI_W,
            'modifier': [iterm2.Modifier.CONTROL,
                         iterm2.Modifier.OPTION]}},
    'stop': {
        'apple': {
            'key': iterm2.Keycode.F7,
            'modifier': [iterm2.Modifier.FUNCTION]},
        'md770': {
            'key': iterm2.Keycode.ANSI_S,
            'modifier': [iterm2.Modifier.CONTROL,
                         iterm2.Modifier.OPTION]}},
    'toggle': {
        'apple': {
            'key': iterm2.Keycode.F8,
            'modifier': [iterm2.Modifier.FUNCTION]},
        'md770': {
            'key': iterm2.Keycode.ANSI_GRAVE,
            'modifier': [iterm2.Modifier.CONTROL,
                         iterm2.Modifier.OPTION]}}
}
WALLPAPER_EXTENTIONS = ['bmp', 'jpeg', 'jpg', 'png']
WALLPAPER_TIMEOUT_SEC = 30 * 60


def load_wallpapers():
    global _wallpapers
    _wallpapers = []
    for ext in WALLPAPER_EXTENTIONS:
        _wallpapers.extend(glob.glob(f'{_wp_path}{ext}', recursive=True))
    print(f'loaded {len(_wallpapers)} backgrounds')


def cancel_tasks():
    for task in _tasks:
        task.cancel()
        print('task canceled')
    _tasks.clear()


def pick_wallpaper():
    while True:
        # Do not allow us to select the same wallpaper
        wallpaper = random.choice(_wallpapers)
        if not wallpaper == _last_wallpaper:
            break
    return wallpaper


def stroke_it(keystroke, task, mapping):
    return (keystroke.keycode == KEYCODES[task][mapping]['key'] and
            keystroke.modifiers == KEYCODES[task][mapping]['modifier'])


async def change_background(app, wallpaper=None):
    global _last_wallpaper
    session = app.current_terminal_window.current_tab.current_session
    profile = await session.async_get_profile()
    if wallpaper is None:
        wallpaper = pick_wallpaper()
        _last_wallpaper = wallpaper
    print(f'setting background to {wallpaper}')
    await profile.async_set_background_image_location(wallpaper)
    subprocess.call(['tmux', 'display-message', wallpaper],
                    env={'PATH': _path})


async def poll_change_background(app, restore=False):
    await change_background(app, _last_wallpaper if restore else None)
    while True:
        await asyncio.sleep(WALLPAPER_TIMEOUT_SEC)
        await change_background(app)


async def main(connection):
    app = await iterm2.async_get_app(connection)
    load_wallpapers()
    global task
    task = asyncio.create_task(poll_change_background(app))
    _tasks.append(task)

    async def keystroke_handler(keystroke, app):
        """This function is called every time a key is pressed."""
        for m in MAPPINGS:
            if stroke_it(keystroke, 'toggle', m):
                # Toggle the background on and off for work calls
                if not len(_tasks):
                    task = asyncio.create_task(
                            poll_change_background(app, True))
                    _tasks.append(task)
                else:
                    cancel_tasks()
                    await change_background(app, '')
            elif stroke_it(keystroke, 'stop', m):
                cancel_tasks()
            elif stroke_it(keystroke, 'reload', m):
                load_wallpapers()
            elif stroke_it(keystroke, 'next', m):
                # Skip to the next background
                cancel_tasks()
                task = asyncio.create_task(poll_change_background(app))
                _tasks.append(task)
            elif stroke_it(keystroke, 'info', m):
                message = (f'stopped: {not _tasks};'
                           f' loaded: {len(_wallpapers)};'
                           f' t/o: {WALLPAPER_TIMEOUT_SEC}'
                           f' loc: {_last_wallpaper}').lower()
                subprocess.call(['tmux', 'display-message', message],
                                env={'PATH': _path})

    # Monitor the keyboard
    async with iterm2.KeystrokeMonitor(connection) as mon:
        while True:
            keystroke = await mon.async_get()
            await keystroke_handler(keystroke, app)

iterm2.run_forever(main)

