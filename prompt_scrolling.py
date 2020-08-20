import sys
from operator import add, mul
from pathlib import Path
from shutil import get_terminal_size
from typing import Sequence, Tuple, Union, Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.data_structures import Point
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout import ScrollOffsets
from prompt_toolkit.widgets.base import Frame

# get terminal size from: event.app.renderer.output.get_size() -> Size
# 

bindings = KeyBindings()
@bindings.add("c-c")
def _(event):
    event.app.exit()

scroll_position = 0
@bindings.add("left")
def _(event):
    "Move the tape left"
    global scroll_position
    scroll_position -= 1

@bindings.add("right")
def _(event):
    "Move the tape right"
    global scroll_position
    scroll_position += 1
    print(event.app.renderer.output.get_size())

text = ''.join(f"{x: >5}   " for x in range(21))
ftc = FormattedTextControl(text=text)
win = Window(
    content=ftc,
    width=None,
    height=1,
    dont_extend_height=True,
    dont_extend_width=True,
    wrap_lines=False,
    always_hide_cursor=True,
    cursorline=False,
    cursorcolumn=False,
    align=WindowAlign.LEFT,
)
lay = Layout(
    container=win,
)

def make_scroller() -> Callable[[], Point]:
    global win
    if win.render_info:
        print(win.render_info)
        print(dir(win.render_info))
        sys.exit(0)
    def scroller() -> Point:
        global scroll_position
        if scroll_position < 0:
            scroll_position = 0
        elif scroll_position > len(text):
            scroll_position = len(text)

        return Point(scroll_position, 0)
    
    return scroller

ftc.get_cursor_position = make_scroller()

app = Application(
    layout=lay,
    key_bindings=bindings,
)

if __name__ == "__main__":
    app.run()