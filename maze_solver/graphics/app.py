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
        super(MainWindow, self).__init__(self._root,
                                         width/3)

        super().grid(row=0, column=0, columnspan=4, sticky=(N, S, W, E))
        super(MainWindow, self).grid(row=0, column=4, sticky=E)
        # self._add_scrolling()
        self.maze: Maze = None
        self._canvas.bind('<Configure>', lambda e: self._resize_maze())

        self._root.bind('<Return>', lambda x: self.create_maze())

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

    def _calculate_maze_position(self, maze_rows: int, maze_cols: int):
        canvas_height = self._canvas.winfo_height()
        canvas_width = self._canvas.winfo_width()
        cell_height = canvas_height / (maze_rows + 2)
        cell_width = canvas_width / (maze_cols + 2)

        cell_size = min(cell_height, cell_width)

        height_pos = (canvas_height - cell_size * maze_rows) / 2
        width_pos = (canvas_width - cell_size * maze_cols) / 2

        pos = Point(width_pos, height_pos)

        return pos, cell_size

    def _resize_maze(self):
        if self.maze is None:
            return
        self.maze.interrupt()
        pos, size = self._calculate_maze_position(
            self.maze._rows, self.maze._cols)
        self.maze.resize(size, pos)
        self.maze.clear(clear_solution=False)
