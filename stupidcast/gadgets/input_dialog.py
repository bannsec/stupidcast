
from prompt_toolkit.widgets import Frame, Dialog, Label, Button, RadioList, TextArea, ValidationToolbar
from prompt_toolkit.layout import Float, HSplit, Dimension
from prompt_toolkit.application import get_app

from stupidcast.config import config

def input_dialog(title, text, callback=None, ok_text="OK", cancel_text="Cancel", password=False, completer=None, validator=None):

    def accept(buf):
        get_app().layout.focus(ok_button)
        return True  # Keep text.

    def ok_handler():
        config.root_float.floats.pop()
        get_app().invalidate()
        #get_app().exit(result=textfield.text)

    def cancel_handler():
        config.root_float.floats.pop()
        get_app().invalidate()

    ok_button = Button(text=ok_text, handler=ok_handler)
    cancel_button = Button(text=cancel_text, handler=cancel_handler)

    textfield = TextArea(
        multiline=False,
        password=password,
        completer=completer,
        validator=validator,
        accept_handler=accept,
        width=Dimension(min=80),
    )

    dialog = Dialog(
        title=title,
        body=HSplit(
            [
                Label(text=text, dont_extend_height=True),
                textfield,
                ValidationToolbar(),
            ],
            padding=Dimension(preferred=1, max=1),
        ),
        buttons=[ok_button, cancel_button],
        with_background=True,
    )

    f = Float(dialog)
    config.root_float.floats.append(f)
    get_app().layout.focus(dialog)
    get_app().invalidate()



"""
    def handler():
        config.root_float.floats.pop()
        get_app().invalidate()
        if callable(callback):
            callback()

    dialog = Dialog(
            title=title,
            body=Label(text=text, dont_extend_height=True),
            buttons=[Button(text=button_text, handler=handler)] if button_text else None,
            with_background=True,
        )


"""
