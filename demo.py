# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "martle>=0.2.0",
# ]
# ///
import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from martle import Color, Martle
    return Color, Martle, mo


@app.cell
def _(mo):
    mo.md(r"""
    # 🐢 Async Turtle Graphics in Marimo
    """)
    return


@app.cell
def _(Color):
    async def spiral(t):
        colors = list(Color)
        for i in range(70):
            if i % 10 == 0:
                t.set_color(colors[(i // 10) % len(colors)])
            await t.forward(i * 2.8)
            t.right(91)

    return (spiral,)


@app.cell
def _(Color):
    async def star(t):
        colors = list(Color)
        for i in range(5):
            t.set_color(colors[i % len(colors)])
            await t.forward(200)
            t.right(144)

    return (star,)


@app.cell
def _(Color):
    async def branch(tt, length, depth):
        if depth == 0 or length < 3:
            await tt.forward(length)
            return
        await tt.forward(length / 3)
        tt.left(60)
        await branch(tt, length / 3, depth - 1)
        tt.right(120)
        await branch(tt, length / 3, depth - 1)
        tt.left(60)
        await tt.forward(length / 3)

    async def snowflake(t):
        colors = list(Color)
        for i in range(3):
            t.set_color(colors[i % len(colors)])
            await branch(t, 210, 3)
            t.right(120)

    return (snowflake,)


@app.cell
def _(Color):
    async def square_spiral(t):
        colors = list(Color)
        for i in range(52):
            if i % 4 == 0:
                t.set_color(colors[(i // 4) % len(colors)])
            await t.forward(10 + i * 3.8)
            t.right(89)

    return (square_spiral,)


@app.cell
def _():
    async def koch(tt, length, depth):
        if depth == 0:
            await tt.forward(length)
            return
        await koch(tt, length / 3, depth - 1)
        tt.left(60)
        await koch(tt, length / 3, depth - 1)
        tt.right(120)
        await koch(tt, length / 3, depth - 1)
        tt.left(60)
        await koch(tt, length / 3, depth - 1)

    async def koch_curve(t):
        t.goto(t.width * 0.1, t.height * 0.6)
        t.setheading(0)
        await koch(t, t.width * 0.8, 3)

    return (koch_curve,)


@app.cell
def _(koch_curve, mo, snowflake, spiral, square_spiral, star):
    shapes = {
        "spiral": spiral,
        "star": star,
        "snowflake": snowflake,
        "square spiral": square_spiral,
        "koch curve": koch_curve,
    }
    pattern = mo.ui.dropdown(
        options=list(shapes.keys()),
        value=list(shapes.keys())[0],
        label="Pattern",
    )
    speed = mo.ui.slider(1, 30, value=12, label="Speed (steps/sec)")
    draw_btn = mo.ui.run_button(label="▶ Draw")
    mo.hstack([pattern, speed, draw_btn], gap=2)
    return draw_btn, pattern, shapes, speed


@app.cell
async def _(Martle, draw_btn, mo, pattern, shapes, speed):
    # cell is async: marimo runs it on its asyncio event loop
    draw_btn  # reactive: re-run this cell whenever the button is clicked

    # Draw.
    turtle = Martle(delay=1.0 / speed.value)
    await shapes[pattern.value](turtle)

    # Final frame: hide the turtle marker
    mo.output.replace(mo.Html(turtle.draw(show_turtle=False)))
    return


if __name__ == "__main__":
    app.run()
