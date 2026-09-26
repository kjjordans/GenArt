import math

import vsketch


def rose_point(
    amplitude: float, frequency: float, phase: float, theta: float
) -> tuple[float, float]:
    r = amplitude * math.cos(frequency * theta + phase)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return (x, y)


def rose_points(
    amplitude: float, frequency: float, phase: float, num_points: int
) -> list[tuple[float, float]]:
    points = []
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        point = rose_point(amplitude, frequency, phase, theta)
        points.append(point)
    return points


class RosetteSketch(vsketch.SketchClass):
    amplitude: vsketch.Param[float] = vsketch.Param(80.0)
    frequency: vsketch.Param[float] = vsketch.Param(5.0)
    phase: vsketch.Param[float] = vsketch.Param(0.0)
    num_points: vsketch.Param[int] = vsketch.Param(500)
    layers: vsketch.Param[int] = vsketch.Param(3)
    layer_scale: vsketch.Param[float] = vsketch.Param(0.7)
    layer_rotation: vsketch.Param[float] = vsketch.Param(15.0)


    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("mm")
        
        cx = vsk.width / 2
        cy = vsk.height / 2
        
        vsk.translate(cx, cy)
        for layer in range(self.layers):
            scale = self.layer_scale ** layer
            rotation = self.layer_rotation * layer

            points = rose_points(
                self.amplitude * scale, self.frequency, self.phase + math.radians(rotation), self.num_points
            )

            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % len(points)]
                vsk.line(x1, y1, x2, y2)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    RosetteSketch.display()
