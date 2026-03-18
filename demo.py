# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
#     "martle>=0.4.0",
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

    Each turtle method is an `async def` coroutine that `await`s a short
    `asyncio.sleep()` after drawing, yielding control back to the event
    loop so Marimo can push the updated SVG to the browser in real time.

    No threads, no locks — just cooperative multitasking.
    """)
    return


# ── Spiral ────────────────────────────────────────────────────────────────────


@app.cell
def _(Color, mo):
    spiral_token = [None]  # spiral_token[0] holds the active World, if any

    def _stop_spiral(_):
        if spiral_token[0] is not None:
            spiral_token[0]._stop = True

    async def spiral(t):
        colors = list(Color)
        for i in range(70):
            if i % 10 == 0:
                t.set_color(colors[(i // 10) % len(colors)])
            await t.forward(i * 2.8)
            t.right(91)

    spiral_btn = mo.ui.run_button(label="Draw")
    spiral_stop = mo.ui.run_button(label="Stop", on_change=_stop_spiral)
    spiral_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Spiral"), spiral_spd, spiral_btn, spiral_stop], gap=2)
    return spiral, spiral_btn, spiral_spd, spiral_stop, spiral_token


@app.cell
async def _(World, mo, spiral, spiral_btn, spiral_spd, spiral_stop, spiral_token):
    mo.stop(not spiral_btn.value)
    _world = World(delay=1.0 / spiral_spd.value)
    spiral_token[0] = _world
    _t = _world.turtle()
    await _world.run(spiral(_t))
    spiral_token[0] = None
    return


# ── Star ──────────────────────────────────────────────────────────────────────


@app.cell
def _(Color, mo):
    star_token = [None]

    def _stop_star(_):
        if star_token[0] is not None:
            star_token[0]._stop = True

    async def star(t):
        colors = list(Color)
        for i in range(5):
            t.set_color(colors[i % len(colors)])
            await t.forward(200)
            t.right(144)

    star_btn = mo.ui.run_button(label="Draw")
    star_stop = mo.ui.run_button(label="Stop", on_change=_stop_star)
    star_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Star"), star_spd, star_btn, star_stop], gap=2)
    return star, star_btn, star_spd, star_stop, star_token


@app.cell
async def _(World, mo, star, star_btn, star_spd, star_stop, star_token):
    mo.stop(not star_btn.value)
    _world = World(delay=1.0 / star_spd.value)
    star_token[0] = _world
    _t = _world.turtle()
    await _world.run(star(_t))
    star_token[0] = None
    return


# ── Snowflake ─────────────────────────────────────────────────────────────────


@app.cell
def _(Color, mo):
    snowflake_token = [None]

    def _stop_snowflake(_):
        if snowflake_token[0] is not None:
            snowflake_token[0]._stop = True

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

    snowflake_btn = mo.ui.run_button(label="Draw")
    snowflake_stop = mo.ui.run_button(label="Stop", on_change=_stop_snowflake)
    snowflake_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Snowflake"), snowflake_spd, snowflake_btn, snowflake_stop], gap=2)
    return snowflake, snowflake_btn, snowflake_spd, snowflake_stop, snowflake_token


@app.cell
async def _(World, mo, snowflake, snowflake_btn, snowflake_spd, snowflake_stop, snowflake_token):
    mo.stop(not snowflake_btn.value)
    _world = World(delay=1.0 / snowflake_spd.value)
    snowflake_token[0] = _world
    _t = _world.turtle()
    await _world.run(snowflake(_t))
    snowflake_token[0] = None
    return


# ── Square Spiral ─────────────────────────────────────────────────────────────


@app.cell
def _(Color, mo):
    sq_token = [None]

    def _stop_sq(_):
        if sq_token[0] is not None:
            sq_token[0]._stop = True

    async def square_spiral(t):
        colors = list(Color)
        for i in range(52):
            if i % 4 == 0:
                t.set_color(colors[(i // 4) % len(colors)])
            await t.forward(10 + i * 3.8)
            t.right(89)

    square_spiral_btn = mo.ui.run_button(label="Draw")
    sq_stop = mo.ui.run_button(label="Stop", on_change=_stop_sq)
    sq_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Square Spiral"), sq_spd, square_spiral_btn, sq_stop], gap=2)
    return square_spiral, square_spiral_btn, sq_spd, sq_stop, sq_token


@app.cell
async def _(World, mo, square_spiral, square_spiral_btn, sq_spd, sq_stop, sq_token):
    mo.stop(not square_spiral_btn.value)
    _world = World(delay=1.0 / sq_spd.value)
    sq_token[0] = _world
    _t = _world.turtle()
    await _world.run(square_spiral(_t))
    sq_token[0] = None
    return


# ── Koch Curve ────────────────────────────────────────────────────────────────


@app.cell
def _(mo):
    koch_token = [None]

    def _stop_koch(_):
        if koch_token[0] is not None:
            koch_token[0]._stop = True

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
        t.set_heading(0)
        await koch(t, t.width * 0.8, 3)

    koch_btn = mo.ui.run_button(label="Draw")
    koch_stop = mo.ui.run_button(label="Stop", on_change=_stop_koch)
    koch_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Koch Curve"), koch_spd, koch_btn, koch_stop], gap=2)
    return koch_curve, koch_btn, koch_spd, koch_stop, koch_token


@app.cell
async def _(World, mo, koch_curve, koch_btn, koch_spd, koch_stop, koch_token):
    mo.stop(not koch_btn.value)
    _world = World(delay=1.0 / koch_spd.value)
    koch_token[0] = _world
    _t = _world.turtle()
    await _world.run(koch_curve(_t))
    koch_token[0] = None
    return


# ── Two Circles ───────────────────────────────────────────────────────────────
# Both turtles trace circles of equal radius (r = d / (2 sin(a/2)) ≈ 57 px).
# The slow turtle uses half the step size and twice the step count, so it
# takes twice as long to complete the same circle.
# t1 (fast): forward(1),   right(1)   × 360 steps → r ≈ 57 px
# t2 (slow): forward(0.5), right(0.5) × 720 steps → r ≈ 57 px, 2× slower


@app.cell
def _(mo):
    circles_token = [None]

    def _stop_circles(_):
        if circles_token[0] is not None:
            circles_token[0]._stop = True

    circles_btn = mo.ui.run_button(label="Draw")
    circles_stop = mo.ui.run_button(label="Stop", on_change=_stop_circles)
    circles_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Two Circles"), circles_spd, circles_btn, circles_stop], gap=2)
    return circles_btn, circles_spd, circles_stop, circles_token


@app.cell
async def _(World, Color, mo, circles_btn, circles_spd, circles_stop, circles_token):
    mo.stop(not circles_btn.value)

    async def fast_circle(t):
        t.set_color(Color.TEAL)
        for _ in range(360):
            await t.forward(1)
            t.right(1)

    async def slow_circle(t):
        t.set_color(Color.SANDY)
        for _ in range(720):
            await t.forward(0.5)
            t.right(0.5)

    _world = World(delay=1.0 / circles_spd.value)
    circles_token[0] = _world
    _t1 = _world.turtle()
    _t2 = _world.turtle()
    _t1.goto(63, 240)   # circle centre ≈ (120, 240)
    _t2.goto(303, 240)  # circle centre ≈ (360, 240)
    await _world.run(fast_circle(_t1), slow_circle(_t2))
    circles_token[0] = None
    return


if __name__ == "__main__":
    app.run()
