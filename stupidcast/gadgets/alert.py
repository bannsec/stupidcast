
from prompt_toolkit.widgets import Frame, Dialog, Label, Button, RadioList
from prompt_toolkit.layout import Float, HSplit
from prompt_toolkit.application import get_app

from stupidcast.config import config

def alert(title, text, callback=None, button_text="OK"):
    def handler():
        config.root_float.floats.pop()
        get_app().layout.focus(config.window_castinfo)
        get_app().invalidate()
        if callable(callback):
            callback()

    dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[Button(text=button_text, handler=handler)] if button_text else None,
            with_background=True,
        )


    f = Float(dialog)
    config.root_float.floats.append(f)

    if button_text:
        get_app().layout.focus(dialog)

    get_app().invalidate()
