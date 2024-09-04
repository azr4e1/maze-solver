import unittest
from maze_solver.graphics import Maze, Point


class MazeTest(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_zero(self):
        num_cols = 0
        num_rows = 0
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )

    def test_maze_create_cells_zero_row(self):
        num_cols = 12
        num_rows = 0
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_maze_create_cells_zero_cols(self):
        num_cols = 0
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, None)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )

    def test_maze_create_blanks(self):
        num_cols = 10
        num_rows = 10
        m1 = Maze(Point(0, 0), num_rows, num_cols, 10, 10, None)
        m1._break_entrance_and_exit()

        self.assertFalse(m1._cells[0][0].lwall)
        self.assertFalse(m1._cells[m1._cols-1][m1._rows-1].rwall)


if __name__ == "__main__":
    unittest.main()
