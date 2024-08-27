from graphics import Window, Line, Point


def main():
    win = Window("Maze Solver", 800, 600)
    line1 = Line(Point(1, 2), Point(10, 4))
    line2 = Line(Point(2, 2), Point(10, 4))
    line3 = Line(Point(9, 2), Point(9, 1))
    line4 = Line(Point(8, 19), Point(2, 4))
    line5 = Line(Point(10, 2), Point(4, 10))

    win.draw_line(line1, "black")
    win.draw_line(line2, "black")
    win.draw_line(line3, "black")
    win.draw_line(line4, "black")
    win.draw_line(line5, "black")
    win.wait_for_close()


main()
