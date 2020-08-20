from operator import add, mul
from pathlib import Path
from shutil import get_terminal_size
from typing import Sequence, Tuple, Union

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

# We have an input tape with all the opcodes and input in a file
# We read it in, and turn it into a list of integers
tape = list(
    map(
        int,
        Path("day2_input.txt").read_text().split(","),
    )
)
# We also want a pointer that keeps track of which opcode we're executing
pointer: int = 0

# Part of the problem statement described modifying the tape
tape[1] = 12
tape[2] = 2

def render_tape_range(begin=0, end=None) -> str:
    if end is None:
        end = len(tape)
    
    return ''.join(f"{x: >5}   " for x in tape[begin:end])

def op(opcode: int, val1: int, val2: int, output: int) -> None:
    if not isinstance(opcode, int) or opcode not in [1,2,99]:
        raise NotImplementedError("Bad opcode!")
    if opcode == 99:
        raise StopIteration("STOP")
    
    if opcode == 1:
        tape[output] = add(val1, val2)
    else:
        tape[output] = mul(val1, val2)

def current_instruction() -> Tuple[int, int, int, int]:
    return tuple(tape[pointer, pointer + 4])

def behind_tape() -> Sequence[int]:
    return tape[:pointer]

def ahead_tape() -> Sequence[int]:
    return tape[pointer + 4:]

bindings = KeyBindings()
@bindings.add("c-c")
def _(event):
    event.app.exit()

scroll_offset = 0
@bindings.add("left")
def _(event):
    "Move the tape left"
    global scroll_offset
    scroll_offset += 1

@bindings.add("right")
def _(event):
    "Move the tape right"
    global scroll_offset
    scroll_offset -= 1

app = Application(
    layout=Layout(
        HSplit([
            FloatContainer(
                content=Window(content=FormattedTextControl(text=""), height=1),
                floats=[
                    Float(
                        content=Window(char="┌"),
                        top=0,
                        left=36,
                        width=1,
                        height=1,
                    ),
                    Float(
                        content=Window(char="─"),
                        width=7,
                        height=1,
                        top=0,
                        left=37,
                    ),
                    Float(
                        content=Window(char="┐"),
                        width=1,
                        height=1,
                        top=0,
                        left=44,
                    )
                ],
            ),
            FloatContainer(
                content=HSplit([
                    Window(content=FormattedTextControl(text=""), height=1),
                    Window(
                        content=FormattedTextControl(text=render_tape_range()),
                        height=1,
                        align=WindowAlign.LEFT,
                    ),
                    Window(content=FormattedTextControl(text=""), height=1),
                ]),
                floats=[
                    Float(
                        content=Frame(
                            body=Window(content=FormattedTextControl(text="")),
                        ),
                        height=3,
                        width=32,
                        left=7,
                        transparent=True,
                    ),
                    Float(
                        content=Window(content=FormattedTextControl(text="↓")),
                        width=1,
                        height=1,
                        left=44,
                        top=0,
                    )
                ]
            )
        ],
        )
    ),
    key_bindings=bindings,
)

app = Application(
    layout=Layout(
        Window(
            content=FormattedTextControl(
                text="         ".join(map(str, range(20))),
                get_cursor_position=lambda : Point(2,0),
            ),
            width=None,
            height=1,
            z_index=None,
            dont_extend_width=True,
            dont_extend_height=True,
            ignore_content_width=False,
            ignore_content_height=False,
            left_margins=None,
            right_margins=None,
            scroll_offsets=None,
            allow_scroll_beyond_bottom=False,
            wrap_lines=False,
            get_vertical_scroll=None,
            get_horizontal_scroll=lambda win, a=scroll_offset: a,
            always_hide_cursor=False,
            cursorline=False,
            cursorcolumn=True,
            colorcolumns=None,
            align=WindowAlign.LEFT,
            style="",
            char=None,
            get_line_prefix=None,
        )
    ),
    key_bindings=bindings,
)

if __name__ == "__main__":
    app.run()