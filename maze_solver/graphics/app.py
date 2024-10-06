from tkinter import Tk, N, S, E, W, HORIZONTAL, VERTICAL
from tkinter import ttk
from .window import MainWindow, Point
from .controls import Control
from .maze import Maze

MAZE_POS = Point(10, 10)


class App(MainWindow, Control):
    def __init__(self, title, width, height):
        self._root = Tk()
        self._root.title(title)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)
        super().__init__(self._root, width, height)
        super(MainWindow, self).__init__(self._root, width/3, MAZE_POS)

        super().grid(row=0, column=0, columnspan=4, sticky=(N, S, W, E))
        super(MainWindow, self).grid(row=0, column=4, sticky=E)
        # self._add_scrolling()
        self.maze: Maze = None

        self._root.bind('<Return>', lambda x: self.create_maze())
        # self._canvas.bind('<Button-4>', self._scroll_vertically_mousewheel(-1))
        # self._canvas.bind('<Button-5>', self._scroll_vertically_mousewheel(1))
        # self._canvas.bind('<Shift-Button-4>',
        #                   self._scroll_horizontally_mousewheel(-1))
        # self._canvas.bind('<Shift-Button-5>',
        #                   self._scroll_horizontally_mousewheel(1))

    def wait_for_close(self):
        self._is_running = True
        while self._is_running:
            self.redraw()
        print("window closed")

    def close(self):
        self.interrupt_maze()
        self._is_running = False

    def _add_scrolling(self):
        cell_size = self.maze_cell_size.get()
        height = 2 * MAZE_POS.y + self.maze_rows.get() * cell_size
        width = 4 * MAZE_POS.x + self.maze_cols.get() * cell_size

        h = ttk.Scrollbar(self._root, orient=HORIZONTAL)
        v = ttk.Scrollbar(self._root, orient=VERTICAL)

        self._canvas.config(scrollregion=(0, 0, width, height))
        self._canvas['yscrollcommand'] = v.set
        self._canvas['xscrollcommand'] = h.set

        h['command'] = self._canvas.xview
        v['command'] = self._canvas.yview

        h.grid(column=0, row=1, sticky=(W, E))
        v.grid(column=1, row=0, sticky=(N, S))

    def _update_scrollsize(self):
        cell_size = self.maze_cell_size.get()
        height = 2 * MAZE_POS.y + self.maze_rows.get() * cell_size
        width = 4 * MAZE_POS.x + self.maze_cols.get() * cell_size
        self._canvas.config(scrollregion=(0, 0, width, height))
        self.redraw()

    def _scroll_vertically_mousewheel(self, direction):
        def inner(event):
            self._canvas.yview_scroll(direction, "units")

        return inner

    def _scroll_horizontally_mousewheel(self, direction):
        def inner(event):
            self._canvas.xview_scroll(direction, "units")

        return inner
