"""Metaballs study: circles that move and bounce off the window edges.

Run from the project root with:
    .venv-py5\\Scripts\\python sketches\\py5\\metaballs\\metaballs.py
"""

import numpy as np
import py5

ROWS = 40
COLS = 80
SPACING = 10

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
        self.cols = cols + 1
        self.rows = rows + 1
        self.spacing = spacing
        self.values = np.zeros((rows + 1, cols + 1))  # 2D array of shape (rows, cols)

    def point_at(self, col: int, row: int) -> tuple[float, float]:
        """Return the (x, y) coordinates of the grid point at (col, row)."""
        x = col * self.spacing
        y = row * self.spacing
        return x, y

    def show(self):
        py5.stroke(255, 50)
        for i in range(self.cols):
            x = i * self.spacing
            py5.line(x, 0, x, py5.height)
        for j in range(self.rows):
            y = j * self.spacing
            py5.line(0, y, py5.width, y)

    def metaball_values(self, balls: list[Ball]):
        """Calculate the metaball values at each grid point based on the balls."""
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = self.point_at(col, row)
                value = 0
                for ball in balls:
                    value += ball.r**2 / ((x - ball.x) ** 2 + (y - ball.y) ** 2 + 1e-9)
                self.values[row, col] = value

    def display_values(self):
        """Display the grid values as brightness on the screen."""
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = self.point_at(col, row)
                brightness = py5.remap(self.values[row, col], 0, 1, 0, 255)

                py5.fill(brightness, 100)
                py5.no_stroke()
                py5.rect_mode(py5.CENTER)
                py5.rect(x, y, self.spacing, self.spacing)


def edge_crossing(
    x1: float, y1: float, x2: float, y2: float, v1: float, v2: float, level: float
) -> tuple[float, float] | None:
    """Return the crossing point on the edge (x1, y1)-(x2, y2) where the values
    v1 and v2 cross *level*, or None if both endpoints are on the same side."""
    if (v1 >= level) == (v2 >= level):
        return None

    t = (level - v1) / (v2 - v1)
    x_cross = x1 + t * (x2 - x1)
    y_cross = y1 + t * (y2 - y1)
    return x_cross, y_cross


def contours(grid: Grid, threshold: float):
    """Draw contours based on the grid values and a threshold."""
    lines = []
    for row in range(grid.rows - 1):
        for col in range(grid.cols - 1):
            # Values at the corners of the cell.
            tl = grid.values[row, col]
            tr = grid.values[row, col + 1]
            br = grid.values[row + 1, col + 1]
            bl = grid.values[row + 1, col]

            case = (
                int(tl >= threshold)
                | (int(tr >= threshold) << 1)
                | (int(br >= threshold) << 2)
                | (int(bl >= threshold) << 3)
            )
            if case in (0, 15):
                continue

            # Interpolate the crossing point on each edge that the threshold
            # passes through.
            x0, y0 = grid.point_at(col, row)
            x1, y1 = grid.point_at(col + 1, row + 1)

            crossings = []
            p_top = edge_crossing(x0, y0, x1, y0, tl, tr, threshold)
            p_right = edge_crossing(x1, y0, x1, y1, tr, br, threshold)
            p_bottom = edge_crossing(x0, y1, x1, y1, bl, br, threshold)
            p_left = edge_crossing(x0, y0, x0, y1, tl, bl, threshold)
            for p in (p_top, p_right, p_bottom, p_left):
                if p is not None:
                    crossings.append(p)

            if len(crossings) == 2:
                lines.append((crossings[0], crossings[1]))
            elif len(crossings) == 4:
                # Ambiguous saddle case: resolve connectivity using the cell
                # centre average.
                center_high = (tl + tr + br + bl) / 4 >= threshold

                if case == 5:
                    pairs = ((0, 1), (2, 3)) if center_high else ((0, 3), (1, 2))
                else:  # case == 10
                    pairs = ((0, 3), (1, 2)) if center_high else ((0, 1), (2, 3))

                for first, second in pairs:
                    lines.append((crossings[first], crossings[second]))
    return lines


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
    grid.show()

    for ball in balls:
        ball.update()
        ball.show()

    grid.metaball_values(balls)
    grid.display_values()

    lines = contours(grid, threshold=1)
    py5.stroke(255, 0, 0)
    for line in lines:
        (x1, y1), (x2, y2) = line
        py5.line(x1, y1, x2, y2)


py5.run_sketch()
