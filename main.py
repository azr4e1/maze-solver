from graphics import Window, Line, Point


def main():
    win = Window("Maze Solver", 800, 600)
    line1 = Line(Point(1, 2), Point(100, 4))
    line2 = Line(Point(2, 2), Point(100, 400))
    line3 = Line(Point(90, 2), Point(400, 100))
    line4 = Line(Point(800, 190), Point(200, 40))
    line5 = Line(Point(10, 200), Point(400, 100))

    win.draw_line(line1, "black")
    win.draw_line(line2, "black")
    win.draw_line(line3, "black")
    win.draw_line(line4, "black")
    win.draw_line(line5, "black")
    win.wait_for_close()


main()
