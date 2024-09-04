from typing import Optional
import time
from random import choice

from .window import Line, Point, Window


FRAME_TIME = 0.05
CELL_COLOR = 'black'


class Cell:
    def __init__(self,
                 win: Window,
                 pos1: Point,
                 pos2: Point,
                 lwall: bool = True,
                 rwall: bool = True,
                 uwall: bool = True,
                 dwall: bool = True,
                 visited: bool = False):
        self._pos1 = pos1
        self._pos2 = pos2
        self._win = win
        self.lwall = lwall
        self.rwall = rwall
        self.uwall = uwall
        self.dwall = dwall
        self.visited = visited

    def draw(self, color: str):
        if self._win is None:
            return

        blank_color = self._win._canvas['background']

        lline = Line(self._pos1, Point(self._pos1.x, self._pos2.y))
        rline = Line(Point(self._pos2.x, self._pos1.y), self._pos2)
        uline = Line(self._pos1, Point(self._pos2.x, self._pos1.y))
        dline = Line(Point(self._pos1.x, self._pos2.y), self._pos2)

        for w, l in [(self.lwall, lline),
                     (self.rwall, rline),
                     (self.uwall, uline),
                     (self.dwall, dline)]:
            clr = color if w else blank_color
            self._win.draw_line(l, clr)

    def draw_move(self, to_cell, undo: bool = False):
        if self._win is None:
            return

        point1 = Point((self._pos1.x + self._pos2.x) / 2,
                       (self._pos1.y + self._pos2.y) / 2)
        point2 = Point((to_cell.__pos1.x + to_cell.__pos2.x) / 2,
                       (to_cell.__pos1.y + to_cell.__pos2.y) / 2)
        color = 'red' if undo else 'gray'
        self._win.draw_line(Line(point1, point2), color)


class Maze:
    def __init__(
            self,
            pos: Point,
            num_rows: int,
            num_cols: int,
            cell_size_x: int,
            cell_size_y: int,
            win: Window,
            seed: Optional[int] = None):
        self._posn = pos
        self._rows = num_rows
        self._cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []
        self._create_cells()

    def _create_cells(self):
        curr_x = self._posn.x
        for coln in range(self._cols):
            rows = []
            curr_y = self._posn.y
            for rown in range(self._rows):
                point1 = Point(curr_x, curr_y)

                # update curr_y
                curr_y += self._cell_size_y
                point2 = Point(curr_x + self._cell_size_x, curr_y)

                cell = Cell(self._win, point1, point2)
                rows.append(cell)
            self._cells.append(rows)
            curr_x += self._cell_size_x

    def draw(self):
        for i in range(self._cols):
            for j in range(self._rows):
                self._draw_cell(i, j)
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0, set())

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw(CELL_COLOR)
        self._animate()

    def _break_entrance_and_exit(self):
        self._cells[0][0].lwall = False
        self._draw_cell(0, 0)

        self._cells[self._cols-1][self._rows-1].rwall = False
        self._draw_cell(self._cols-1, self._rows-1)

    def _break_walls_r(self, i, j, visited):
        visited.add((i, j))
        while True:
            adjacents = list(filter(lambda x: (0 <= x[0] < self._cols)
                                    and (0 <= x[1] < self._rows)
                                    and (x not in visited),
                                    [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]))
            if len(adjacents) == 0:
                return

            next = choice(adjacents)
            self._break_walls_between_cells(i, j, next[0], next[1])
            self._break_walls_r(next[0], next[1], visited)

    def _break_walls_between_cells(self, cur_i, cur_j, next_i, next_j):
        if cur_i > next_i:
            self._cells[cur_i][cur_j].lwall = False
            self._cells[next_i][next_j].rwall = False
        elif cur_i < next_i:
            self._cells[cur_i][cur_j].rwall = False
            self._cells[next_i][next_j].lwall = False
        elif cur_j > next_j:
            self._cells[cur_i][cur_j].uwall = False
            self._cells[next_i][next_j].dwall = False
        else:
            self._cells[cur_i][cur_j].dwall = False
            self._cells[next_i][next_j].uwall = False
        self._draw_cell(cur_i, cur_j)
        self._draw_cell(next_i, next_j)

    def _animate(self):
        if self._win is None:
            return

        self._win.redraw()
        time.sleep(FRAME_TIME)
