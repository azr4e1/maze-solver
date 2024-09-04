from tkinter import Tk, Canvas, N, S, W, E


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


class Window:
    def __init__(self, title, width, height):
        self._root = Tk()
        self._root.title(title)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        self._canvas = Canvas(
            self._root, background="white", width=width, height=height)
        self._canvas.grid(row=0, column=0, sticky=(N, S, W, E))
        self._is_running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()
        print("window closed")

    def close(self):
        self._is_running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self._canvas, fill_color)
