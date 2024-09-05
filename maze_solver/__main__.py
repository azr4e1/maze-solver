from graphics import Window, Point, Maze


def main():
    win = Window("Maze Solver", 800, 600)

    maze = Maze(Point(10, 10), 10, 15, 50, 50, win, 1)
    maze.draw()

    win.wait_for_close()


main()
