# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "martle>=0.6.0",
# ]
# ///
import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from martle import Color, World

    return Color, World, mo


@app.cell
def _(mo):
    mo.md(r"""
    # 🐢 Async Turtle Graphics in Marimo

    Each demo below is an interactive widget with its own start, stop,
    and speed controls.  Drawing runs as an asyncio task in Marimo's event
    loop, so the kernel stays responsive and 'stop' works immediately.
    """)
    return


# Spiral
@app.cell
def _(Color, World, mo):
    _world = World()

    async def _spiral(world, turtle):
        colors = list(Color)
        for i in range(70):
            if i % 10 == 0:
                turtle.set_color(colors[(i // 10) % len(colors)])
            await turtle.forward(i * 2.8)
            turtle.right(91)

    _world.set_coroutine(_spiral)
    mo.ui.anywidget(_world)


# Star
@app.cell
def _(Color, World, mo):
    _world = World()

    async def _star(world, turtle):
        colors = list(Color)
        for i in range(5):
            turtle.set_color(colors[i % len(colors)])
            await turtle.forward(200)
            turtle.right(144)

    _world.set_coroutine(_star)
    mo.ui.anywidget(_world)


# Snowflake
@app.cell
def _(Color, World, mo):
    _world = World()

    async def _branch(turtle, length, depth):
        if depth == 0 or length < 3:
            await turtle.forward(length)
            return
        await turtle.forward(length / 3)
        turtle.left(60)
        await _branch(turtle, length / 3, depth - 1)
        turtle.right(120)
        await _branch(turtle, length / 3, depth - 1)
        turtle.left(60)
        await turtle.forward(length / 3)

    async def _snowflake(world, turtle):
        colors = list(Color)
        for i in range(3):
            turtle.set_color(colors[i % len(colors)])
            await _branch(turtle, 210, 3)
            turtle.right(120)

    _world.set_coroutine(_snowflake)
    mo.ui.anywidget(_world)


# Square Spiral
@app.cell
def _(Color, World, mo):
    _world = World()

    async def _square_spiral(world, turtle):
        colors = list(Color)
        for i in range(52):
            if i % 4 == 0:
                turtle.set_color(colors[(i // 4) % len(colors)])
            await turtle.forward(10 + i * 3.8)
            turtle.right(89)

    _world.set_coroutine(_square_spiral)
    mo.ui.anywidget(_world)


# Koch Curve
@app.cell
def _(Color, World, mo):
    _world = World()

    async def _koch(turtle, length, depth):
        if depth == 0:
            await turtle.forward(length)
            return
        await _koch(turtle, length / 3, depth - 1)
        turtle.left(60)
        await _koch(turtle, length / 3, depth - 1)
        turtle.right(120)
        await _koch(turtle, length / 3, depth - 1)
        turtle.left(60)
        await _koch(turtle, length / 3, depth - 1)

    async def _koch_curve(world, turtle):
        turtle.set_color(Color.SKY)
        turtle.goto(world.width * 0.1, world.height * 0.6)
        turtle.set_heading(0)
        await _koch(turtle, world.width * 0.8, 3)

    _world.set_coroutine(_koch_curve)
    mo.ui.anywidget(_world)


# Two Circles
@app.cell
def _(Color, World, mo):
    _world = World()

    async def _fast_circle(world, turtle):
        turtle.goto(63, 240)
        turtle.set_color(Color.TEAL)
        for _ in range(360):
            await turtle.forward(1)
            turtle.right(1)

    async def _slow_circle(world, turtle):
        turtle.goto(303, 240)
        turtle.set_color(Color.SANDY)
        for _ in range(720):
            await turtle.forward(0.5)
            turtle.right(0.5)

    _world.set_coroutine(_fast_circle, _slow_circle)
    mo.ui.anywidget(_world)


if __name__ == "__main__":
    app.run()
