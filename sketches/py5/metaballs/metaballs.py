"""Metaballs study: circles that move and bounce off the window edges.

Run from the project root with:
    .venv-py5\\Scripts\\python sketches\\py5\\metaballs\\metaballs.py
"""

import py5

ROWS = 20
COLS = 20
SPACING = 20

WIDTH = COLS * SPACING
HEIGHT = ROWS * SPACING


class Ball:
    def __init__(self, x: float, y: float, r: float, dx: float, dy: float) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.dx = dx
        self.dy = dy

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.check_edges()


    def check_edges(self):
        if self.x - self.r < 0:
            self.x = self.r
            self.dx *= -1
        elif self.x + self.r > py5.width:
            self.x = py5.width - self.r
            self.dx *= -1
        if self.y - self.r < 0:
            self.y = self.r
            self.dy *= -1
        elif self.y + self.r > py5.height:
            self.y = py5.height - self.r
            self.dy *= -1
            

    def show(self):
        py5.stroke(255)
        py5.no_fill()
        py5.ellipse(self.x, self.y, self.r * 2, self.r * 2)


class Grid:
    def __init__(self, cols: int, rows: int, spacing: float) -> None:
        self.cols = cols
        self.rows = rows
        self.spacing = spacing
        # TODO: add self.values -- 2D array of shape (rows, cols), e.g. numpy zeros.
        # TODO: (optional) fill with a test pattern (checkerboard) first so the
        #       array is actually visible while you debug.

    # TODO: add point_at(col, row) -> (x, y) using self.spacing, so show() and
    #       the metaball field code share one coordinate formula.

    def show(self):
        # TODO: guard with a self.visible flag (return when hidden) once show()/hide() exist.
        py5.stroke(255, 50)
        for i in range(self.cols):
            x = i * self.spacing
            py5.line(x, 0, x, py5.height)
        for j in range(self.rows):
            y = j * self.spacing
            py5.line(0, y, py5.width, y)

    # TODO: add a self.visible flag + hide() method; show() should no-op when hidden.




def setup() -> None:
    py5.size(WIDTH, HEIGHT)
    global balls
    global grid
    balls = []

    grid = Grid(COLS, ROWS, SPACING)
    for ball in range(10):
        x = py5.random(py5.width)
        y = py5.random(py5.height)
        r = py5.random(20, 50)
        dx = py5.random(-2, 2)
        dy = py5.random(-2, 2)
        balls.append(Ball(x, y, r, dx, dy))

    
def draw() -> None:
    py5.background(0)

    for ball in balls:
        ball.update()
        ball.show()

    grid.show()  # TODO: move this before the ball loop so grid lines sit behind the balls
    # TODO: render grid.values (map values to brightness) so the array is visible
    # TODO: (after Grid works) metaball field -- for each grid point sum
    #       r / distance(point, ball), and fill points above a threshold to get blobs

py5.run_sketch()
