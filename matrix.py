# -*- coding: utf-8 -*-


class InterpreterError(Exception):
    pass


class Interpreter(object):
    """Simple Command Interpreter."""

    def __init__(self):
        self.current_matrix = None

    def execute_command(self, command):
        try:
            args = command.strip().split()
            cmd, args = args[0], args[1:]
            method = getattr(self, 'do_%s' % cmd)
        except (IndexError, AttributeError):
            return None

        if cmd != 'I' and self.current_matrix is None:
            raise InterpreterError('No matrix instance. '
                                   'Start with the command I X Y.')

        method(*args)

    #: commands

    def do_I(self, x_axis, y_axis):
        """Example: I X N. X and N must be an integer."""
        self.current_matrix = Matrix(int(x_axis), int(y_axis))

    def do_L(self, x_axis, y_axis, color):
        """Example: L X Y C. X and N must be an integer. C must be a pixel value."""
        self.current_matrix.set(int(x_axis) - 1, int(y_axis) - 1, color)

    def do_V(self, x_axis, start_y, end_y, color):
        """Example: V X Y1 Y2 C."""
        self.current_matrix.draw_vertical_segment(
            x_axis=int(x_axis) - 1, start_y=int(start_y) - 1, end_y=int(end_y), value=color
        )

    def do_H(self, start_x, end_x, y_axis, color):
        """Example: H X1 X2 Y C."""
        self.current_matrix.draw_horizontal_segment(
            start_x=int(start_x) - 1, end_x=int(end_x), y_axis=int(y_axis) - 1, value=color
        )

    def do_F(self, x_axis, y_axis, color):
        """Example: F 3 3 J."""
        self.current_matrix.fill_region(x_axis=int(x_axis) - 1, y_axis=int(y_axis) - 1, value=color)

    def do_S(self, filename):
        """Example: S name"""
        self.current_matrix.save(filename)


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
        self.default_pixel = str(default_pixel or 'O')
        self.data = self.init_data(x_axis, y_axis, self.default_pixel)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx_row):
        return self.data[idx_row]

    def __str__(self):
        return '\n'.join(''.join(str(pixel) for pixel in row) for row in self)

    @classmethod
    def init_data(cls, x_axis, y_axis, default_color):
        return [
            [default_color for _ in range(x_axis)] for _ in range(y_axis)
        ]

    def get(self, x_axis, y_axis):
        return self[y_axis][x_axis]

    def set(self, x_axis, y_axis, value):
        """Defines a pixel X to Y.

        :param x_axis:
            The column number (int).
        :param y_axis:
            The row number (int).
        :param value:
            The pixel value.
        """
        self[y_axis][x_axis] = str(value)

    def fill_region(self, x_axis, y_axis, value):
        region = self.get(x_axis, y_axis)

        def recursive_fill(matrix, x_axis, y_axis, value, region):
            left, right = x_axis - 1, x_axis + 1
            top, bottom = y_axis + 1, y_axis - 1

            coordinates = [
                (left, y_axis), (right, y_axis), (top, x_axis), (bottom, x_axis)
            ]

            for y, x in coordinates:
                try:
                    if matrix.get(x, y) == region:
                        matrix.set(x, y, value)
                        recursive_fill(matrix, x, y, value, region)
                except IndexError:
                    pass

        return recursive_fill(self, x_axis, y_axis, value, region)


    def draw_vertical_segment(self, x_axis, start_y, end_y, value):
        """Draw vertical segment.

        :param x_axis:
            The column number (int).
        :param start_y:
            Start segment (int).
        :param end_y:
            End segment (int).
        :param value:
            The pixel value.
        """
        for y_axis in range(start_y, end_y):
            self.set(x_axis=x_axis, y_axis=y_axis, value=value)

    def draw_horizontal_segment(self, start_x, end_x, y_axis, value):
        """Draw vertical segment.

        :param y_axis:
            The column number (int).
        :param start_x:
            Start segment (int).
        :param end_x:
            End segment (int).
        :param value:
            The pixel value.
        """
        for x_axis in range(start_x, end_x):
            self.set(x_axis=x_axis, y_axis=y_axis, value=value)

    def save(self, filename):
        """Save the matrix as file."""
        with open(filename, 'w') as matrix_file:
            matrix_file.write(str(self))
