"""Metaballs study: circles that move and bounce off the window edges.

Run from the project root with:
    .venv-py5\\Scripts\\python sketches\\py5\\metaballs\\metaballs.py
"""

import py5
import numpy as np

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
                    value += ball.r ** 2 / ((x - ball.x)**2 + (y - ball.y)**2)
                self.values[row, col] = value

    def display_values(self):
        """Display the grid values as brightness on the screen."""
        for row in range(self.rows):
            for col in range(self.cols):
                x, y = self.point_at(col, row)
                brightness = py5.remap(self.values[row, col], 0, 1, 0, 255) 
                
                py5.fill(brightness,100)
                py5.no_stroke()
                py5.rect_mode(py5.CENTER)
                py5.rect(x, y, self.spacing, self.spacing)



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




    
    # TODO: render grid.values (map values to brightness) so the array is visible
    # TODO: (after Grid works) metaball field -- for each grid point sum
    #       r / distance(point, ball), and fill points above a threshold to get blobs

py5.run_sketch()
