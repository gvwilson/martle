"""Turtle and World classes."""

import asyncio
import math
import time
from enum import Enum

import marimo as mo

# Default canvas dimensions
WIDTH = 480
HEIGHT = 480

# Render rate: seconds between frames
DEFAULT_DELAY = 0.05

# Initial heading: -90° points upward in SVG coordinate space
INITIAL_ANGLE = -90.0

# SVG line thickness for drawn segments
STROKE_WIDTH = 1.8

# Size of the equilateral triangle that represents the turtle cursor
TURTLE_RADIUS = 9

# Turtle cursor appearance
TURTLE_COLOR = "#00ff88"
TURTLE_OPACITY = 0.9

# Canvas background and border
BACKGROUND_COLOR = "#1a1a2e"
BORDER_RADIUS = 8


class Color(str, Enum):
    """Standard colors available to Martle turtles."""

    CORNFLOWER = "#8ecae6"
    CRIMSON = "#e63946"
    GOLD = "#e9c46a"
    SAGE = "#b5e48c"
    SANDY = "#f4a261"
    SKY = "#a8dadc"
    TEAL = "#2ec4b6"


class World:
    """
    Canvas that owns rendering and hosts one or more turtles.

    Create turtles with ``world.turtle()``, then run drawing coroutines
    concurrently with ``await world.run(coro1, coro2, ...)``.  A background
    render loop composites all turtles into one SVG at a fixed rate
    (``delay`` seconds) so rendering cost is independent of turtle count.
    """

    def __init__(
        self, width: int = WIDTH, height: int = HEIGHT, delay: float = DEFAULT_DELAY
    ):
        self.width = width
        self.height = height
        self._delay = delay
        self._turtles: list["Martle"] = []
        self._dirty = False
        self._last_render: float = 0.0  # time.monotonic() of last render
        self._stop = False

    def turtle(self) -> "Martle":
        """Create a new turtle that belongs to this world."""
        t = Martle(self)
        self._turtles.append(t)
        return t

    async def run(self, *coroutines) -> None:
        """
        Run coroutines concurrently, compositing all turtles each frame.

        A single coroutine is awaited directly so that ``mo.output.replace``
        calls inside it remain on the cell's execution chain.  Multiple
        coroutines are run via ``asyncio.gather``; Python copies the current
        contextvars context into each task, so output calls still reach the
        correct cell.
        """
        self._last_render = 0.0  # ensure first dirty frame renders immediately
        try:
            if len(coroutines) == 1:
                await coroutines[0]
            else:
                await asyncio.gather(*coroutines, return_exceptions=True)
        finally:
            # Final frame: hide turtle cursors
            mo.output.replace(mo.Html(self._draw(show_turtle=False)))

    def _maybe_render(self) -> None:
        """Render if dirty and enough time has elapsed since the last frame."""
        now = time.monotonic()
        if self._dirty and (now - self._last_render) >= self._delay:
            mo.output.replace(mo.Html(self._draw()))
            self._dirty = False
            self._last_render = now

    def _draw(self, show_turtle: bool = True) -> str:
        """Composite all turtles' segments and cursors into one SVG."""
        lines = ""
        for t in self._turtles:
            for (x1, y1), (x2, y2), color in t.segments:
                lines += (
                    f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                    f'x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="{color}" stroke-width="{STROKE_WIDTH}" '
                    f'stroke-linecap="round"/>'
                )
        if show_turtle:
            for t in self._turtles:
                r = math.radians(t.angle)
                # Equilateral triangle: three vertices equally spaced at 120° (2π/3 rad)
                pts = " ".join(
                    f"{t.x + TURTLE_RADIUS * math.cos(r + a):.1f},"
                    f"{t.y + TURTLE_RADIUS * math.sin(r + a):.1f}"
                    for a in [0, 2 * math.pi / 3, -2 * math.pi / 3]
                )
                lines += (
                    f'<polygon points="{pts}" fill="{TURTLE_COLOR}"'
                    f' opacity="{TURTLE_OPACITY}"/>'
                )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}"'
            f' height="{self.height}" style="background:{BACKGROUND_COLOR};'
            f'border-radius:{BORDER_RADIUS}px;display:block">'
            f"{lines}</svg>"
        )


class Martle:
    """
    Async turtle that draws into a World.

    Create via ``World.turtle()`` rather than directly.  Each movement
    method is a coroutine that yields to the event loop after moving so
    that other turtles and the World's render loop can run.
    """

    def __init__(self, world: World):
        self._world = world
        self.x = world.width / 2
        self.y = world.height / 2
        self.angle = INITIAL_ANGLE
        self.pen = True
        self.segments: list = []
        self.color: str = Color.CRIMSON.value

    @property
    def width(self) -> int:
        return self._world.width

    @property
    def height(self) -> int:
        return self._world.height

    def pen_up(self):
        self.pen = False

    def pen_down(self):
        self.pen = True

    def goto(self, x, y):
        self.x, self.y = x, y

    def set_heading(self, a):
        self.angle = a

    def set_color(self, color: "Color | str") -> None:
        self.color = color.value if isinstance(color, Color) else color

    async def forward(self, dist: float):
        if self._world._stop:
            return
        r = math.radians(self.angle)
        nx = self.x + dist * math.cos(r)
        ny = self.y + dist * math.sin(r)
        if self.pen:
            self.segments.append(((self.x, self.y), (nx, ny), self.color))
            self.x, self.y = nx, ny
            self._world._dirty = True
            await asyncio.sleep(self._world._delay)  # pace steps and yield to other turtles
            self._world._maybe_render()
        else:
            self.x, self.y = nx, ny

    async def backward(self, dist: float):
        await self.forward(-dist)

    def right(self, deg: float):
        self.angle += deg

    def left(self, deg: float):
        self.angle -= deg
