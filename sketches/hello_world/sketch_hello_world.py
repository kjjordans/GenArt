
import vsketch


class HelloWorldSketch(vsketch.SketchClass):
    # Sketch parameters:
    radius: vsketch.Param[float] = vsketch.Param(2.0)

    def draw(self, vsk: vsketch.Vsketch) -> None:
        vsk.size("a4", landscape=False)
        vsk.scale("cm")

        x = vsk.width / 2
        y = vsk.height / 2

        vsk.circle(x, y, self.radius, mode="radius")
        vsk.line(x-3, y, x+3, y)
        vsk.line(x, y-3, x, y+3)
        


        

    def finalize(self, vsk: vsketch.Vsketch) -> None:
        vsk.vpype("linemerge linesimplify reloop linesort")


if __name__ == "__main__":
    HelloWorldSketch.display()
