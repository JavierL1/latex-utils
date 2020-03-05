from contextlib import contextmanager


def write(decorated):
    def wrapper(self, *args, **kwargs):
        result = decorated(self, *args, **kwargs)
        if self.buffer == '':
            self.buffer = result
        else:
            self.buffer = f'{self.buffer}\n{result}'
        return result
    return wrapper


class Commands:
    def __init__(self, buffer=''):
        self.buffer = buffer

    def get_buffer(self):
        return self.buffer

    def set_buffer(self, buffer):
        self.buffer = buffer
        return buffer

    @write
    def colorlet(self, newcolor, source):
        return f'\\colorlet{{{newcolor}}}{{{source}}}'

    @write
    def psset(self, options):
        return '\\psset{{{0}}}'.format(', '.join(options))

    def str_coordinate(self, coordinate):
        return f'({str(coordinate[0])}, {str(coordinate[1])})'

    def str_coordinates(self, coordinates):
        return ''.join([
            self.str_coordinate(coor)
            for coor in coordinates
        ])

    @write
    def pspolygon(self, params, coordinates):
        return '\\pspolygon[{0}]{1}'.format(
            ', '.join(params),
            self.str_coordinates(coordinates)
        )

    @write
    def psdots(self, params, coordinates):
        return '\\psdots[{0}]{1}'.format(
            ', '.join(params),
            self.str_coordinates(coordinates)
        )

    @write
    def cnodeput(self, params, coordinate, name, label):
        _params = '[{}]'.format(', '.join(params))
        return (
            f'\\Cnodeput{_params}{self.str_coordinate(coordinate)}'
            f'{{{name}}}{{{label}}}'
        )

    @write
    def ncline(self, params, start, end):
        return '\\ncline[{0}]{{{1}}}{{{2}}}'.format(
            ', '.join(params),
            start,
            end
        )

    @contextmanager
    def pspicture(self, bl=None, tr=None):
        top = '\\begin{pspicture}'
        if tr and bl:
            top = f'{top}{self.str_coordinate(bl)}{self.str_coordinate(tr)}'
        elif tr:
            top = f'{top}{self.str_coordinate(tr)}'
        else:
            raise ValueError(
                'tr cooordinate must be defined to use bl coordinate'
            )
        self.buffer = f'{self.buffer}\n{top}'
        yield
        self.buffer = f'{self.buffer}\n\\end{{pspicture}}'

    @write
    def definecolor(self, name, rgb):
        return '\\definecolor{{{0}}}{{RGB}}{{{1}}}'.format(
            name,
            ', '.join([str(value) for value in rgb])
        )

    @write
    def uput(
        self, coordinate, label, labelsep=None, refangle=None, rotation=None
    ):
        labelsep = f'{{{labelsep}}}' if isinstance(labelsep, float) else ''
        refangle = f'[{refangle}]' if isinstance(refangle, int) else ''
        rotation = f'{{{rotation}}}' if isinstance(rotation, int) else ''
        return '\\uput{0}{1}{2}{3}{{{4}}}'.format(
            labelsep,
            refangle,
            rotation,
            self.str_coordinate(coordinate),
            label
        )
