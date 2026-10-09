import math
import random

import vsketch


def exit_point(
    origin: tuple[float, float],
    direction: tuple[float, float],
    polygon: list[tuple[float, float]],
    skip_edge: int,
) -> tuple[tuple[float, float], int] | None:
    """First point where a ray from ``origin`` leaves a convex polygon.

    The ray starts on the polygon boundary, so the edge holding ``origin`` is
    skipped to avoid a self-hit at distance zero.

    Args:
        origin: Ray start, on the polygon boundary.
        direction: Ray direction as (dx, dy); must point into the polygon.
        polygon: Panel vertices as (x, y), in order.
        skip_edge: Index of the edge that contains ``origin``.

    Returns:
        The exit point and the index of the edge it lies on, or None if the ray
        is parallel to every other edge.
    """
    ox, oy = origin
    dx, dy = direction
    best = None  # (distance, edge index, position along that edge)
    for i in range(len(polygon)):
        if i == skip_edge:
            continue
        ax, ay = polygon[i]
        bx, by = polygon[(i + 1) % len(polygon)]
        ex, ey = bx - ax, by - ay
        denom = dx * ey - dy * ex
        if abs(denom) < 1e-12:  # ray parallel to this edge
            continue
        fx, fy = ax - ox, ay - oy
        s = (fx * ey - fy * ex) / denom
        u = (fx * dy - fy * dx) / denom
        if s > 1e-9 and -1e-9 <= u <= 1.0 + 1e-9 and (best is None or s < best[0]):
            best = (s, i, u)

    if best is None:
        return None
    _, edge, u = best
    u = min(1.0, max(0.0, u))  # clamp to the edge after the tolerance test
    ax, ay = polygon[edge]
    bx, by = polygon[(edge + 1) % len(polygon)]
    return (ax + u * (bx - ax), ay + u * (by - ay)), edge


def subdivide_panel(
    polygon: list[tuple[float, float]],
    rng: random.Random,
    depth: int,
    split_min: float,
    max_tilt: float,
    min_size: float,
    stop_chance: float,
) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    """Recursively slice a convex panel, returning the cut segments.

    Each slice starts partway along the panel's longest edge and runs into the
    panel at an angle, leaving that edge up to ``max_tilt`` degrees from
    perpendicular. A panel may stop early (``stop_chance``) or once its longest
    edge is shorter than ``min_size``, so the subdivision stays uneven.

    Cutting a convex polygon with a straight chord always yields two convex
    polygons, so the inward-normal test below stays valid at every depth.

    Args:
        polygon: Panel vertices as (x, y), in order.
        rng: Seeded random source.
        depth: Remaining recursion levels.
        split_min: Closest the cut may start to a corner, as a fraction of the
            chosen edge.
        max_tilt: Largest tilt from a perpendicular cut, in degrees.
        min_size: Stop once the longest edge is shorter than this length.
        stop_chance: Probability that a panel stops early, 0..1.

    Returns:
        The cut segments, each as ((x1, y1), (x2, y2)).
    """
    count = len(polygon)
    longest_index, longest = max(
        ((i, math.dist(polygon[i], polygon[(i + 1) % count])) for i in range(count)),
        key=lambda edge: edge[1],
    )
    if depth <= 0 or longest < min_size or rng.random() < stop_chance:
        return []

    # anchor the cut on the longest edge
    a = polygon[longest_index]
    b = polygon[(longest_index + 1) % count]
    t = rng.uniform(split_min, 1.0 - split_min)
    origin = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    # inward normal of that edge: a zero tilt cuts straight across
    tx, ty = b[0] - a[0], b[1] - a[1]
    normal = (-ty / longest, tx / longest)
    centre = (sum(p[0] for p in polygon) / count, sum(p[1] for p in polygon) / count)
    if normal[0] * (centre[0] - origin[0]) + normal[1] * (centre[1] - origin[1]) < 0:
        normal = (-normal[0], -normal[1])

    # tilt the cut direction away from that normal
    tilt = math.radians(rng.uniform(-max_tilt, max_tilt))
    direction = (
        normal[0] * math.cos(tilt) - normal[1] * math.sin(tilt),
        normal[0] * math.sin(tilt) + normal[1] * math.cos(tilt),
    )

    hit = exit_point(origin, direction, polygon, longest_index)
    if hit is None:
        return []
    leaving, exit_edge = hit

    # walk the boundary both ways from the cut to build the two new panels
    first_arc = []
    k = (longest_index + 1) % count
    while True:
        first_arc.append(polygon[k])
        if k == exit_edge:
            break
        k = (k + 1) % count
    first = [origin, *first_arc, leaving]

    second_arc = []
    k = (exit_edge + 1) % count
    while True:
        second_arc.append(polygon[k])
        if k == longest_index:
            break
        k = (k + 1) % count
    second = [leaving, *second_arc, origin]

    return (
        [(origin, leaving)]
        + subdivide_panel(first, rng, depth - 1, split_min, max_tilt, min_size, stop_chance)
        + subdivide_panel(second, rng, depth - 1, split_min, max_tilt, min_size, stop_chance)
    )


class RecursiveSubdivisionSketch(vsketch.SketchClass):
    """Recursive subdivision into angled slices, with uneven stopping."""

    # --- Page & stopping rule (all lengths in cm) ---
    margin = vsketch.Param(2.0)  # blank border around the panel field
    max_depth = vsketch.Param(6, min_value=1)  # how many times a panel may split
    min_size = vsketch.Param(1.5)  # stop splitting below this longest-edge length

    # --- Slice placement ---
    split_min = vsketch.Param(0.35, min_value=0.05, max_value=0.5)  # most off-centre start
    max_tilt = vsketch.Param(25.0, min_value=0.0, max_value=80.0)  # degrees from perpendicular

    # --- Uneven stopping ---
    stop_chance = vsketch.Param(0.2, min_value=0.0, max_value=1.0)  # chance a panel stops early

    # --- Layers ---
    layers = vsketch.Param(1, min_value=1)  # each cut is assigned a random layer

    seed = vsketch.Param(42)  # RNG seed: same seed always reproduces the same drawing

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=True)
        vsk.scale("cm")

        page_w = vsk.width * 2.54 / 96  # convert page px -> cm
        page_h = vsk.height * 2.54 / 96

        root = [
            (self.margin, self.margin),
            (page_w - self.margin, self.margin),
            (page_w - self.margin, page_h - self.margin),
            (self.margin, page_h - self.margin),
        ]
        rng = random.Random(self.seed)

        segments = subdivide_panel(
            root,
            rng,
            self.max_depth,
            self.split_min,
            self.max_tilt,
            self.min_size,
            self.stop_chance,
        )

        # the frame holds the composition and fixes the centred bounding box
        vsk.polygon(root, close=True)
        for (x1, y1), (x2, y2) in segments:
            vsk.stroke(rng.randint(1, self.layers))
            vsk.line(x1, y1, x2, y2)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    RecursiveSubdivisionSketch.display()
