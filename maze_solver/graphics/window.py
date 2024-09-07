from tkinter import Tk, Canvas, N, S, W, E
from tkinter import ttk

BACKGROUND = "white"


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def draw(self, canvas: Canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x,
                           self.p2.y, fill=fill_color, width=2)


class MainWindow:
    def __init__(self, root, width, height):
        self._root = root
        self._canvas = Canvas(
            self._root, background=BACKGROUND, width=width, height=height)
        self._is_running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self._canvas, fill_color)

    def grid(self, *args, **kwargs):
        self._canvas.grid(*args, **kwargs)

    def clear(self):
        self._canvas.delete('all')
