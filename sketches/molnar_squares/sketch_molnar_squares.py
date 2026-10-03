import random

import vsketch


class MolnarSquaresSketch(vsketch.SketchClass):
    # Sketch parameters:
    margin = vsketch.Param(2.0)
    n_cols = vsketch.Param(6)
    n_rows = vsketch.Param(6)
    padding = vsketch.Param(0.5)
    jitter_pos = vsketch.Param(0.1, min_value=0.0, max_value=1.0)  # fraction of the cell pitch
    jitter_angle = vsketch.Param(1.0)
    jitter_scale = vsketch.Param(1.0)
    seed = vsketch.Param(42)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=True)
        vsk.scale("cm")

        page_w = vsk.width * 2.54 / 96  # convert page px -> cm

        usable_w = page_w - 2 * self.margin
        cell_w = (usable_w - (self.n_cols - 1) * self.padding) / self.n_cols
        pitch = cell_w + self.padding

        rng = random.Random(self.seed)
        offset = self.jitter_pos * pitch
        amplitude = abs(self.jitter_scale - 1.0)

        for row in range(self.n_rows):
            for col in range(self.n_cols):
                cx = self.margin + col * pitch + cell_w / 2
                cy = self.margin + row * pitch + cell_w / 2

                dx = rng.uniform(-offset, offset)
                dy = rng.uniform(-offset, offset)

                angle = rng.uniform(-self.jitter_angle, self.jitter_angle)

                scale = 1.0 + rng.uniform(-amplitude, amplitude)

                with vsk.pushMatrix():
                    vsk.translate(cx + dx, cy + dy)
                    vsk.rotate(angle, degrees=True)
                    vsk.scale(scale)
                    vsk.rect(-cell_w / 2, -cell_w / 2, cell_w, cell_w)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    MolnarSquaresSketch.display()
