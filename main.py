from graphics import Window, Line, Point, Cell
import time


def main():
    win = Window("Maze Solver", 800, 600)
    # line1 = Line(Point(1, 2), Point(100, 4))
    # line2 = Line(Point(2, 2), Point(100, 400))
    # line3 = Line(Point(90, 2), Point(400, 100))
    # line4 = Line(Point(800, 190), Point(200, 40))
    # line5 = Line(Point(10, 200), Point(400, 100))

    cell1 = Cell(win, Point(10, 20), Point(40, 50),
                 True, True, True, True)
    cell2 = Cell(win, Point(40, 50), Point(60, 70),
                 False, True, True, True)
    cell3 = Cell(win, Point(90, 30), Point(120, 50),
                 True, False, True, True)
    cell4 = Cell(win, Point(200, 10), Point(180, 30),
                 True, True, False, True)
    cell5 = Cell(win, Point(100, 100), Point(400, 400),
                 True, True, False, False)

    # win.draw_line(line1, "black")
    # win.draw_line(line2, "black")
    # win.draw_line(line3, "black")
    # win.draw_line(line4, "black")
    # win.draw_line(line5, "black")
    cell1.draw('red')
    cell2.draw('red')
    cell3.draw('red')
    cell4.draw('red')

    cell5.draw('black')
    cell1.draw_move(cell2, undo=True)

    win.wait_for_close()


main()
