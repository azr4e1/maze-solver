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
        self.__root = Tk()
        self.__root.title(title)
        self.__root.rowconfigure(0, weight=1)
        self.__root.columnconfigure(0, weight=1)
        self.__canvas = Canvas(
            self.__root, background="white", width=width, height=height)
        self.__canvas.grid(row=0, column=0, sticky=(N, S, W, E))
        self.__is_running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.__is_running = True
        while self.__is_running:
            self.redraw()
        print("window closed")

    def close(self):
        self.__is_running = False

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.__canvas, fill_color)


class Cell:
    def __init__(self,
                 win: Window,
                 pos1: Point,
                 pos2: Point,
                 lwall: bool = True,
                 rwall: bool = True,
                 uwall: bool = True,
                 dwall: bool = True):
        self.__pos1 = pos1
        self.__pos2 = pos2
        self.__win = win
        self.lwall = lwall
        self.rwall = rwall
        self.uwall = uwall
        self.dwall = dwall

    def draw(self, color: str):
        if self.lwall:
            line = Line(self.__pos1, Point(self.__pos1.x, self.__pos2.y))
            self.__win.draw_line(line, color)
        if self.rwall:
            line = Line(Point(self.__pos2.x, self.__pos1.y), self.__pos2)
            self.__win.draw_line(line, color)
        if self.uwall:
            line = Line(self.__pos1, Point(self.__pos2.x, self.__pos1.y))
            self.__win.draw_line(line, color)
        if self.dwall:
            line = Line(Point(self.__pos1.x, self.__pos2.y), self.__pos2)
            self.__win.draw_line(line, color)

    def draw_move(self, to_cell, undo: bool = False):
        point1 = Point((self.__pos1.x + self.__pos2.x) / 2,
                       (self.__pos1.y + self.__pos2.y) / 2)
        point2 = Point((to_cell.__pos1.x + to_cell.__pos2.x) / 2,
                       (to_cell.__pos1.y + to_cell.__pos2.y) / 2)
        color = 'red' if undo else 'gray'
        self.__win.draw_line(Line(point1, point2), color)
