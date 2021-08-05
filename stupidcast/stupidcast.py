#!/usr/bin/env python3

import asyncio
import threading

import pychromecast
from prompt_toolkit import Application
from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.widgets import Frame, Dialog, Label, Button, RadioList
from prompt_toolkit.layout.containers import VSplit, Window, WindowAlign, FloatContainer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import Float, HSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import get_app
from prompt_toolkit.formatted_text import HTML

from prettytable import PrettyTable

from .config import config
from .gadgets import radio_list, alert, input_dialog

# get_app().layout.focus(w)


kb = KeyBindings()

@kb.add('0')
def _volume_up(event):
    if config.cast: config.cast.volume_up()

@kb.add('9')
def _volume_down(event):
    if config.cast: config.cast.volume_down()

@kb.add('c-t')
def _(event):
    input_dialog(title="My Title", text="Something here") 

"""
@kb.add('t')
def _(event):
    def handler():
        print("HERE")

    dialog = Dialog(
            title='something',
            body=Label('someting'),
            buttons=[Button(text="something here", handler=handler)],
            )

    f = Float(dialog)
    #f = Float(Window(content=FormattedTextControl("Something")))
    config.root_float.floats.append(f)
    get_app().layout.focus(dialog)
"""

@kb.add('c-q')
@kb.add('c-c')
@kb.add('q')
def exit_(event):
    """
    Pressing Ctrl-Q will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.
    """
    event.app.exit()

"""
buffer1 = Buffer()  # Editable buffer.
root_container = VSplit([
    Window(content=BufferControl(buffer=buffer1)),
    Window(width=1, char='|'),
    Window(content=FormattedTextControl(text='Hello world')),
])
"""

config.window_castinfo = Window(content=FormattedTextControl(""))
config.frame_castinfo = Frame(body=config.window_castinfo)
config.root_float = FloatContainer(content=config.frame_castinfo, floats=[])

#root_container = Window(content=FormattedTextControl(text="Scanning for chromecasts..."), align=WindowAlign.CENTER)
#root_frame = Frame(body=root_container, title="Something")

layout = Layout(config.root_float)

def select_cast():
    chromecasts, browser = pychromecast.get_chromecasts()

    index = radiolist_dialog(
        title="Chromecast",
        text="Which chromecast do you want to connect to?",
        values=[(chromecasts.index(device), f"{device.device.friendly_name} ({device.device.model_name})") for device in chromecasts]
    ).run()

    config.cast = chromecasts[index]
    config.chromecasts = chromecasts

async def _update_cast_status():
    while True:
        await asyncio.sleep(0.5)

        if config.cast is None:
            continue

        config.frame_castinfo.title = config.cast.device.friendly_name
        config.window_castinfo.content = FormattedTextControl(CHROMECAST_STATUS.format(
            friendly_name=config.cast.device.friendly_name,
            app_display_name=config.cast.app_display_name,
            model_name=config.cast.model_name,
            media_title=config.cast.media_controller.status.title if config.cast.media_controller.status else None,
            media_artist=config.cast.media_controller.status.artist if config.cast.media_controller.status else None,
            ))

        get_app().invalidate()


async def _ensure_cast():
    # This can only run in separate thread for some reason
    def _get_chromecasts_thread():
        config.chromecasts, config.browser = pychromecast.get_chromecasts()

    def callback(index):
        config.cast = config.chromecasts[index]
        config.cast.wait()
        #config.chromecasts = chromecasts

    #radio_list("title", "some text", [["1", "One"], ["2", "Two"]], callback=mycb)
    alert("Chromecast", "Searching for chromecasts on your network... Please be patient.", button_text=None)
    await asyncio.sleep(0.2)

    #chromecasts, browser = pychromecast.get_chromecasts()
    t = threading.Thread(target=_get_chromecasts_thread)
    t.start()
    t.join()
    config.root_float.floats.pop()

    if config.chromecasts == []:
        return alert("Chromecast", "Couldn't find any devices!", callback=lambda: exit(1))

    radio_list(
        title="Chromecast",
        text="Which chromecast do you want to connect to?",
        values=[(config.chromecasts.index(device), f"{device.device.friendly_name} ({device.device.model_name})") for device in config.chromecasts],
        callback=callback
    )


def main():
    #print("Searching for chromecasts...")
    #select_cast()
    app = Application(layout=layout, full_screen=True, key_bindings=kb)
    app.create_background_task(_update_cast_status())
    app.create_background_task(_ensure_cast())
    app.run()


CHROMECAST_STATUS = HTML(r"""
<b><u>Chromecast Info</u></b>
<b>Name</b>:  {friendly_name}
<b>Model</b>: {model_name}
<b>App</b>:   {app_display_name}

<b><u>Media Info</u></b>
<b>Title</b>:  {media_title}
<b>Artist</b>: {media_artist}
""")

if __name__ == '__main__':
    main()

