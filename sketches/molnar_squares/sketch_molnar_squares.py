import vsketch


class MolnarSquaresSketch(vsketch.SketchClass):
    # Sketch parameters:
    margin = vsketch.Param(2.0)
    n_cols = vsketch.Param(6)
    padding = vsketch.Param(0.5)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False, center=False)
        vsk.scale("cm")

        page_w = vsk.width * 2.54 / 96  # convert page px -> cm

        usable_w = page_w - 2 * self.margin
        cell_w = (usable_w - (self.n_cols - 1) * self.padding) / self.n_cols
        pitch = cell_w + self.padding

        for row in range(self.n_cols):
            for col in range(self.n_cols):
                x = self.margin + col * pitch
                y = self.margin + row * pitch
                vsk.rect(x, y, cell_w, cell_w)

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    MolnarSquaresSketch.display()
