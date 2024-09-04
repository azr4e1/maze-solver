from graphics.graphics import Window, Line, Point, Cell, Maze
import time


def main():
    win = Window("Maze Solver", 800, 600)

    maze = Maze(Point(10, 10), 10, 12, 50, 50, win)
    maze.draw()

    win.wait_for_close()


main()
