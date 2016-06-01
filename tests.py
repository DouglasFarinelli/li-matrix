# -*- coding: utf-8 -*-

import unittest
from matrix import Interpreter, InterpreterError


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


if __name__ == '__main__':
    unittest.main()
