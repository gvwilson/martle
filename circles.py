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


@app.cell
def _(mo):
    circles_world = [None]

    def _stop_circles(_):
        if circles_world[0] is not None:
            circles_world[0]._stop = True

    circles_btn = mo.ui.run_button(label="Draw")
    circles_stop = mo.ui.run_button(label="Stop", on_change=_stop_circles)
    circles_spd = mo.ui.slider(1, 30, value=12, label="Speed")
    mo.hstack([mo.md("### Two Circles"), circles_spd, circles_btn, circles_stop], gap=2)
    return circles_btn, circles_spd, circles_stop, circles_world


@app.cell
async def _(World, Color, mo, circles_btn, circles_spd, circles_stop, circles_world):
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
    circles_world[0] = _world
    _t1 = _world.turtle()
    _t2 = _world.turtle()
    _t1.goto(63, 240)  # circle centre ≈ (120, 240)
    _t2.goto(303, 240)  # circle centre ≈ (360, 240)
    await _world.run(fast_circle(_t1), slow_circle(_t2))
    circles_world[0] = None
    return


if __name__ == "__main__":
    app.run()
