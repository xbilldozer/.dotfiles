#!/usr/bin/env python3.7
import asyncio
from datetime import datetime
import glob
import iterm2
import random
import subprocess
import os

_last_switch = -1
_last_background = ''
_path = f'/usr/local/bin/:{os.environ.get("PATH")}'
_tasks = []
_backgrounds = []
_bg_path = os.path.join(os.environ.get('HOME'), 'src/wallpapers/**/*.')
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
BACKGROUND_EXTENTIONS = ['bmp', 'jpeg', 'jpg', 'png']
BACKGROUND_TIMEOUT_SEC = 30 * 60


def load_backgrounds():
    global _backgrounds
    _backgrounds = []
    for ext in BACKGROUND_EXTENTIONS:
        _backgrounds.extend(glob.glob(f'{_bg_path}{ext}', recursive=True))
    print(f'loaded {len(_backgrounds)} backgrounds')


def cancel_tasks():
    global _last_switch
    for task in _tasks:
        task.cancel()
        print('task canceled')
    _last_switch = -1
    _tasks.clear()


def pick_background():
    while True:
        # Do not allow us to select the same background
        background = random.choice(_backgrounds)
        if not background == _last_background:
            break
    return background


def stroke_it(keystroke, task, mapping):
    return (keystroke.keycode == KEYCODES[task][mapping]['key'] and
            keystroke.modifiers == KEYCODES[task][mapping]['modifier'])


async def change_background(app, background=None):
    global _last_background
    session = app.current_terminal_window.current_tab.current_session
    profile = await session.async_get_profile()
    if background is None:
        background = pick_background()
        _last_background = background
    print(f'setting background to {background}')
    await profile.async_set_background_image_location(background)
    subprocess.call(['tmux', 'display-message', background],
                    env={'PATH': _path})


async def poll_change_background(app, restore=False):
    global _last_switch
    await change_background(app, _last_background if restore else None)
    while True:
        _last_switch = datetime.now()
        await asyncio.sleep(BACKGROUND_TIMEOUT_SEC)
        await change_background(app)


async def main(connection):
    app = await iterm2.async_get_app(connection)
    load_backgrounds()
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
                # Stop cycling through backgrounds, leave current background
                cancel_tasks()
            elif stroke_it(keystroke, 'reload', m):
                # Rediscover backgrounds
                load_backgrounds()
            elif stroke_it(keystroke, 'next', m):
                # Skip to the next background
                cancel_tasks()
                task = asyncio.create_task(poll_change_background(app))
                _tasks.append(task)
            elif stroke_it(keystroke, 'info', m):
                # Display debug information
                next_sec = 'n/a'
                if not _last_switch == -1:
                    next_sec = BACKGROUND_TIMEOUT_SEC - (
                            datetime.now() - _last_switch).seconds
                information = [
                    f'stopped: {not _tasks}',
                    f'loaded: {len(_backgrounds)}',
                    f't/o: {BACKGROUND_TIMEOUT_SEC}',
                    f'next in: {next_sec}',
                    f'loc: {_last_background}'
                ]
                message = '; '.join(information).lower()
                subprocess.call(['tmux', 'display-message', message],
                                env={'PATH': _path})

    # Monitor the keyboard
    async with iterm2.KeystrokeMonitor(connection) as mon:
        while True:
            keystroke = await mon.async_get()
            await keystroke_handler(keystroke, app)

iterm2.run_forever(main)



