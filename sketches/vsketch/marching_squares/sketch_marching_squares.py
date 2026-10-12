import vsketch


class MarchingSquaresSketch(vsketch.SketchClass):
    n_xcells = vsketch.Param(20, step=1)
    margin = vsketch.Param(1.0)






    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")
        width_cm = vsk.width * 2.54 / 96  # convert page px -> cm
        height_cm = vsk.height * 2.54 / 96  # convert page px -> cm

        cell_size = (width_cm - 2 * self.margin) / self.n_xcells
        n_ycells = int((height_cm - 2 * self.margin) / cell_size)

        for column in range(self.n_xcells+1):
            for row in range(n_ycells+1):
                x = self.margin + column * cell_size
                y = self.margin + row * cell_size
                vsk.circle(x, y, 0.1)




    

        


    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    MarchingSquaresSketch.display()
