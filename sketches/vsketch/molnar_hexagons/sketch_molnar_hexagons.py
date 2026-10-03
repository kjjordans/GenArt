import math
import random

import vsketch


def hexagon_points(radius: float) -> list[tuple[float, float]]:
    """Vertices of a pointy-top regular hexagon centred on the origin."""
    points = []
    for k in range(6):
        angle = math.radians(60 * k - 30)
        points.append((radius * math.cos(angle), radius * math.sin(angle)))
    return points


class MolnarHexagonsSketch(vsketch.SketchClass):
    """Molnár-style nested hexagons on an offset (honeycomb) grid."""

    # --- Page & grid (all lengths in cm) ---
    margin = vsketch.Param(2.0)  # blank border around the whole grid
    n_cols = vsketch.Param(6)  # hexagons across
    n_rows = vsketch.Param(6)  # hexagons down
    padding = vsketch.Param(0.5)  # gap between neighbouring hexagons
    row_offset = vsketch.Param(
        0.5, min_value=0.0, max_value=1.0
    )  # odd-row shift, fraction of pitch

    # --- Concentric hexagons ---
    nests = vsketch.Param(3, min_value=1)  # hexagons per cell
    nest_scale = vsketch.Param(0.75, min_value=0.05, max_value=1.0)  # inner size x previous

    # --- Jitter: maximum per-hexagon variation, reached at the focus point ---
    jitter_pos = vsketch.Param(0.06, min_value=0.0, max_value=1.0)
    jitter_angle = vsketch.Param(1.5)  # max rotation in degrees
    jitter_scale = vsketch.Param(1.0)  # whole-nest size factor: 1 = none

    # --- Focus: the point the disorder is centred on ---
    focus_x = vsketch.Param(0.5, min_value=0.0, max_value=1.0)  # 0 = left edge, 1 = right
    focus_y = vsketch.Param(0.5, min_value=0.0, max_value=1.0)  # 0 = top edge, 1 = bottom
    spread = vsketch.Param(0.7, min_value=0.05)  # bell width, as a fraction of grid reach

    # --- Layers & omission ---
    layers = vsketch.Param(1, min_value=1)  # hexagons are assigned a random layer
    omit = vsketch.Param(0.0, min_value=0.0, max_value=1.0)  # chance a hexagon is skipped

    seed = vsketch.Param(42)  # RNG seed: same seed always reproduces the same drawing

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=True)
        vsk.scale("cm")

        page_w = vsk.width * 2.54 / 96  # convert page px -> cm

        usable_w = page_w - 2 * self.margin
        cell_w = (usable_w - (self.n_cols - 1) * self.padding) / self.n_cols
        pitch = cell_w + self.padding
        radius = cell_w / 2  # circumradius; a pointy-top hexagon is cell_w tall

        # grid extents (odd rows stick out by the row_offset) and the focus point
        grid_w = (self.n_cols - 1) * pitch + cell_w + self.row_offset * pitch
        grid_h = (self.n_rows - 1) * pitch + cell_w
        x0, y0 = self.margin, self.margin
        ref = (x0 + self.focus_x * grid_w, y0 + self.focus_y * grid_h)

        # approximate farthest cell: the corners of the grid block
        corner_cells = [
            (x0 + cell_w / 2, y0 + cell_w / 2),
            (x0 + grid_w - cell_w / 2, y0 + cell_w / 2),
            (x0 + cell_w / 2, y0 + grid_h - cell_w / 2),
            (x0 + grid_w - cell_w / 2, y0 + grid_h - cell_w / 2),
        ]
        max_dist = max(math.dist(ref, c) for c in corner_cells)
        sigma = max(self.spread * max_dist, 1e-6)

        rng = random.Random(self.seed)
        offset = self.jitter_pos * pitch
        amplitude = abs(self.jitter_scale - 1.0)
        base_hex = hexagon_points(radius)

        for row in range(self.n_rows):
            for col in range(self.n_cols):
                # odd rows shift sideways so the grid interlocks (honeycomb)
                cx = self.margin + col * pitch + (row % 2) * self.row_offset * pitch + cell_w / 2
                cy = self.margin + row * pitch + cell_w / 2

                # bell weight: 1 at the focus, falling off with distance
                w = math.exp(-((math.dist((cx, cy), ref) / sigma) ** 2))

                # one size factor per cell, shared by every ring
                block_scale = 1.0 + rng.uniform(-amplitude * w, amplitude * w)

                for i in range(self.nests):
                    # draw all randoms before the omit roll, so changing `omit`
                    # only removes hexagons without moving the others
                    dx = rng.uniform(-offset * w, offset * w)
                    dy = rng.uniform(-offset * w, offset * w)
                    angle = rng.uniform(-self.jitter_angle * w, self.jitter_angle * w)
                    layer = rng.randint(1, self.layers)

                    if rng.random() < self.omit:
                        continue

                    # each ring gets its own layer and transform (off-register look)
                    vsk.stroke(layer)
                    with vsk.pushMatrix():
                        vsk.translate(cx + dx, cy + dy)
                        vsk.rotate(angle, degrees=True)
                        vsk.scale(block_scale * self.nest_scale**i)
                        vsk.polygon(base_hex, close=True)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    MolnarHexagonsSketch.display()
