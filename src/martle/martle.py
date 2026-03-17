"""Turtle class."""

import asyncio
import math
from enum import Enum

import marimo as mo

# Canvas dimensions
WIDTH = 480
HEIGHT = 480

# Seconds to sleep between frames (controls animation speed)
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
    """Standard palette colors available to Martle turtles."""
    CRIMSON     = "#e63946"
    SANDY       = "#f4a261"
    TEAL        = "#2ec4b6"
    SKY         = "#a8dadc"
    GOLD        = "#e9c46a"
    CORNFLOWER  = "#8ecae6"
    SAGE        = "#b5e48c"


class Martle:
    """
    Async turtle graphics for Marimo.

    Each movement method is a coroutine.  Callers `await` it, so the
    event loop gets a chance to flush the updated SVG to the browser
    after every single line segment.

    The pen color is not changed automatically.  Call ``set_color``
    with a ``Color`` enum value or a hex string before drawing.
    """

    def __init__(self, width: int = WIDTH, height: int = HEIGHT, delay: float = DEFAULT_DELAY):
        self.width = width
        self.height = height
        self.x = width / 2
        self.y = height / 2
        self.angle = INITIAL_ANGLE
        self.pen = True
        self.segments: list = []
        self.color: str = Color.CRIMSON.value
        self._delay = delay

    # ── pen control ──────────────────────────────────────────────────────
    def penup(self):   self.pen = False
    def pendown(self): self.pen = True
    def goto(self, x, y): self.x, self.y = x, y
    def setheading(self, a): self.angle = a

    def set_color(self, color: "Color | str") -> None:
        """Set the pen color to a Color enum value or a hex string."""
        self.color = color.value if isinstance(color, Color) else color

    # ── SVG rendering ─────────────────────────────────────────────────────
    def draw(self, show_turtle: bool = True) -> str:
        lines = ""
        for (x1, y1), (x2, y2), color in self.segments:
            lines += (
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" '
                f'x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{color}" stroke-width="{STROKE_WIDTH}" '
                f'stroke-linecap="round"/>'
            )
        marker = ""
        if show_turtle:
            r = math.radians(self.angle)
            # Equilateral triangle: three vertices equally spaced at 120° (2π/3 rad)
            pts = " ".join(
                f"{self.x + TURTLE_RADIUS*math.cos(r+a):.1f},{self.y + TURTLE_RADIUS*math.sin(r+a):.1f}"
                for a in [0, 2*math.pi/3, -2*math.pi/3]
            )
            marker = f'<polygon points="{pts}" fill="{TURTLE_COLOR}" opacity="{TURTLE_OPACITY}"/>'
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'style="background:{BACKGROUND_COLOR};border-radius:{BORDER_RADIUS}px;display:block">'
            f'{lines}{marker}</svg>'
        )

    # ── private: push one SVG frame ──────────────────────────────────────
    async def _frame(self):
        mo.output.replace(mo.Html(self.draw()))
        await asyncio.sleep(self._delay)   # ← yield to event loop here

    # ── movement coroutines ──────────────────────────────────────────────
    async def forward(self, dist: float):
        r = math.radians(self.angle)
        nx = self.x + dist * math.cos(r)
        ny = self.y + dist * math.sin(r)
        if self.pen:
            self.segments.append(((self.x, self.y), (nx, ny), self.color))
            self.x, self.y = nx, ny
            await self._frame()
        else:
            self.x, self.y = nx, ny

    async def backward(self, dist: float):
        await self.forward(-dist)

    def right(self, deg: float): self.angle += deg

    def left(self,  deg: float): self.angle -= deg
