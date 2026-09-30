import math

import vsketch

"""
Lissajous / Harmonograph Curves — Generative Art Primer
========================================================

A Lissajous curve is parametric harmonic motion:
    x(t) = A · sin(a·t + δ)
    y(t) = B · sin(b·t)

    a / b    = frequency ratio  →  pattern complexity & symmetry
    δ        = phase shift      →  which shape the ratio takes
    A, B     = amplitudes       →  stretch on each axis

Integer ratios (1:1, 1:2, 2:3, 3:4, 4:5) produce closed,
repeating curves. Irrational ratios never repeat.

A Harmonograph extends this with damping and multiple pendulums:
    x(t) = sum of sin(aᵢ·t + φᵢ) · e^(-dᵢ·t)
    y(t) = sum of sin(bⱼ·t + φⱼ) · e^(-dⱼ·t)

    d        = damping (friction)  →  spiral-inward decay
    more terms = richer, "mechanical" feel

Creative knobs:
    - frequency ratio (musical intervals: 1:2 octave, 3:2 fifth)
    - phase difference (rotates the whole figure)
    - damping (adds motion / decay / echo)
    - # of pendulums (1 per axis → clean, 2+ → complex)
    - time range or threshold stop (open loop vs closed)
    - colour mapped to time, speed, or position
"""

class HarmonographSketch(vsketch.SketchClass):
    # Sketch parameters:
    # radius = vsketch.Param(2.0)
    freq_1 = vsketch.Param(3.0)
    freq_2 = vsketch.Param(2.0)
    freq_3 = vsketch.Param(5.0)
    freq_4 = vsketch.Param(4.0)
    phase_1 = vsketch.Param(0.0, step=1)  # degrees
    phase_2 = vsketch.Param(0.0, step=1)  # degrees
    phase_3 = vsketch.Param(0.0, step=1)  # degrees
    phase_4 = vsketch.Param(0.0, step=1)  # degrees
    amplitude_a = vsketch.Param(5.0)
    amplitude_b = vsketch.Param(5.0)    
    damping = vsketch.Param(0.01)
    samples = vsketch.Param(1000)
    dt = vsketch.Param(0.1)

    def harmonograph_point(self, t: float) -> tuple[float, float]:
        x = (
            self.amplitude_a * math.sin(self.freq_1 * t + math.radians(self.phase_1)) * math.exp(-self.damping * t)
            + self.amplitude_a * math.sin(self.freq_2 * t + math.radians(self.phase_2)) * math.exp(-self.damping * t)
        )
        y = (
            self.amplitude_b * math.sin(self.freq_3 * t + math.radians(self.phase_3)) * math.exp(-self.damping * t)
            + self.amplitude_b * math.sin(self.freq_4 * t + math.radians(self.phase_4)) * math.exp(-self.damping * t)
        )
        return x, y

    def generate_harmonograph(self) -> list[tuple[float, float]]:
        points = []
        for i in range(self.samples):
            t = i * self.dt  # Adjust the time step as needed
            point = self.harmonograph_point(t)
            points.append(point)
        return points

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        translate_x = vsk.width / 2
        translate_y = vsk.height / 2
        vsk.translate(translate_x, translate_y)

        points = self.generate_harmonograph()
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            vsk.line(x1, y1, x2, y2)


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify linesort")


if __name__ == "__main__":
    HarmonographSketch.display()
