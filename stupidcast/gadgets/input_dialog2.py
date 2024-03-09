
from asyncio import Future, ensure_future

from prompt_toolkit.widgets import Frame, Dialog, Label, Button, RadioList, TextArea, ValidationToolbar
from prompt_toolkit.layout import Float, HSplit, Dimension
from prompt_toolkit.application import get_app

from stupidcast.config import config


class TextInputDialog:
    def __init__(self, title="", label_text="", completer=None):
        self.future = Future()

        def accept_text(buf):
            get_app().layout.focus(ok_button)
            buf.complete_state = None
            return True

        def accept():
            self.future.set_result(self.text_area.text)

        def cancel():
            self.future.set_result(None)

        self.text_area = TextArea(
            completer=completer,
            multiline=False,
            width=Dimension(preferred=40),
            accept_handler=accept_text,
        )

        ok_button = Button(text="OK", handler=accept)
        cancel_button = Button(text="Cancel", handler=cancel)

        self.dialog = Dialog(
            title=title,
            body=HSplit([Label(text=label_text), self.text_area]),
            buttons=[ok_button, cancel_button],
            width=Dimension(preferred=80),
            modal=True,
        )

    def __pt_container__(self):
        return self.dialog

async def show_dialog_as_float(dialog):
    "Coroutine."
    float_ = Float(content=dialog)
    config.root_float.floats.insert(0, float_)

    app = get_app()

    focused_before = app.layout.current_window
    app.layout.focus(dialog)
    result = await dialog.future
    app.layout.focus(focused_before)

    if float_ in root_container.floats:
        root_container.floats.remove(float_)

    return result

