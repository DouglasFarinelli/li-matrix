# -*- coding: utf-8 -*-


class InterpreterError(Exception):
    pass


class Interpreter(object):
    """Simple Command Interpreter."""

    def __init__(self):
        self.current_matrix = None

    def do_I(self, x_axis, y_axis):
        """Example: I X N. X and N must be an integer."""
        self.current_matrix = Matrix(int(x_axis), int(y_axis))

    def execute_command(self, command):
        try:
            args = command.strip().split()
            cmd, args = args[0], args[1:]
            method = getattr(self, 'do_%s' % cmd)
        except (IndexError, AttributeError):
            raise InterpreterError('Command %s not found.' % command)

        try:
            method(*args)
        except TypeError:
            raise InterpreterError(
                'Invalid arguments, help: %s' % getattr(method, '__doc__', '')
            )


class Matrix(object):
    """Simple Graphic Matrix."""

    def __init__(self, x_axis, y_axis, default_pixel=None):
        """
        :param x_axis:
            The number of rows (`int`).
        :param y_axis:
            The number of columns (`int`).
        :param default_pixel:
            Pixel default boot.
        """
        self.x_axis, self.y_axis = x_axis, y_axis
        self.default_pixel = str(default_pixel or 0)
        self.data = self.init_data(x_axis, y_axis, self.default_pixel)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx_row):
        return self.data[idx_row]

    @classmethod
    def init_data(cls, x_axis, y_axis, default_color):
        return [
            [default_color for _ in range(x_axis)] for _ in range(y_axis)
        ]
