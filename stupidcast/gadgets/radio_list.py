
from prompt_toolkit.widgets import Frame, Dialog, Label, Button, RadioList
from prompt_toolkit.layout import Float, HSplit
from prompt_toolkit.application import get_app

from stupidcast.config import config

def radio_list(title, text, values, callback=None, ok_text="OK", cancel_text="Cancel"):
    def ok_handler():
        config.root_float.floats.pop()
        get_app().layout.focus(config.window_castinfo)
        get_app().invalidate()
        callback(radio_list.current_value)

    def cancel_handler():
        get_app().layout.focus(config.window_castinfo)
        config.root_float.floats.pop()

    radio_list = RadioList(values)

    #container = message_dialog(title='something', text='something').layout.container
    dialog = Dialog(
            title=title,
            body=HSplit(
                [Label(text=text, dont_extend_height=True), radio_list],
                padding=1,
            ),
            buttons=[
                Button(text=ok_text, handler=ok_handler),
                Button(text=cancel_text, handler=cancel_handler),
            ],
            with_background=True,
        )


    f = Float(dialog)
    config.root_float.floats.append(f)
    get_app().layout.focus(dialog)
    get_app().invalidate()
