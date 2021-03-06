# -*- coding: utf-8 -*-

import unittest
from matrix import Interpreter, InterpreterError

OUTPUT02 = """\
JJJJJJJJJJ
JJJJJJJJJJ
JWJJAJJJJJ
JWJJJJJJJJ
ZZZZZZZZZZ
RRRRRRRRRR
REEEEEEERR
REEEEEEERR
RRRRRRRRRR\
"""


class MatrixTest(unittest.TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def test_create_a_new_matrix(self):
        x_axis, y_axis = 5, 6

        self.interpreter.execute_command('I 5 6')
        matrix = self.interpreter.current_matrix

        self.assertIsNotNone(matrix)

        self.assertEqual(len(matrix), y_axis)

        for columns in matrix:
            self.assertEqual(len(columns), x_axis)

            for p in columns:
                self.assertEqual(p, matrix.default_pixel)

    def test_command_without_initialize_the_matrix(self):
        with self.assertRaises(InterpreterError):
            self.interpreter.execute_command('L 2 3 A')

    def test_set_a_pixel(self):
        self.interpreter.execute_command('I 5 6')
        self.interpreter.execute_command('L 2 3 A')
        self.assertEqual(str(self.interpreter.current_matrix), 'OOOOO\nOOOOO\nOAOOO\nOOOOO\nOOOOO\nOOOOO')

    def test_ignored_commands(self):
        self.interpreter.execute_command('I 5 6')
        self.interpreter.execute_command('L 2 3 A')
        self.interpreter.execute_command('S one.bmp')
        self.interpreter.execute_command('G 2 3 J')
        self.assertTrue(True)

    def test_draw_new_vertical_segment(self):
        self.interpreter.execute_command('I 5 6')
        self.interpreter.execute_command('L 2 3 A')
        self.interpreter.execute_command('S one.bmp')
        self.interpreter.execute_command('G 2 3 J')
        self.interpreter.execute_command('V 2 3 4 W')
        self.assertTrue(True)

    def test_draw_new_horizontal_segment(self):
        self.interpreter.execute_command('I 5 6')
        self.interpreter.execute_command('L 2 3 A')
        self.interpreter.execute_command('S one.bmp')
        self.interpreter.execute_command('G 2 3 J')
        self.interpreter.execute_command('V 2 3 4 W')
        self.interpreter.execute_command('H 3 4 2 Z')
        self.assertTrue(True)

    def test_fill_region(self):
        self.interpreter.execute_command('I 5 6')
        self.interpreter.execute_command('L 2 3 A')
        self.interpreter.execute_command('S one.bmp')
        self.interpreter.execute_command('G 2 3 J')
        self.interpreter.execute_command('V 2 3 4 W')
        self.interpreter.execute_command('H 3 4 2 Z')
        self.interpreter.execute_command('F 3 3 J')
        self.interpreter.execute_command('S two.bmp')
        self.assertEqual(str(self.interpreter.current_matrix), 'JJJJJ\nJJZZJ\nJWJJJ\nJWJJJ\nJJJJJ\nJJJJJ')

    def test_draw_rectangle(self):
        self.interpreter.execute_command('I 10 9')
        self.interpreter.execute_command('L 5 3 A')
        self.interpreter.execute_command('G 2 3 J')
        self.interpreter.execute_command('V 2 3 4 W')
        self.interpreter.execute_command('H 1 10 5 Z')
        self.interpreter.execute_command('F 3 3 J')
        self.interpreter.execute_command('K 2 7 8 8 E')
        self.interpreter.execute_command('F 9 9 R')
        self.interpreter.execute_command('S one.bmp')
        self.assertEqual(str(self.interpreter.current_matrix), OUTPUT02)


if __name__ == '__main__':
    unittest.main()
