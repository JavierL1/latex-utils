import os
from latex.utils import Writter, Commands


if __name__ == "__main__":
    w = Writter()
    c = Commands()
    path = (
        'C:\\Users\\Javier\\Documents\\pstricks-automation\\drawings'
    )
    filename = 'basic_ann.tex'
    filepath = os.path.join(path, filename)

    def a_name(sub, sup):
        return f'a{sub}{sup}'

    def a_label(sub, sup):
        if isinstance(sub, int):
            sub = sub + 1
        if isinstance(sup, int):
            sup = sup + 1
        return f'$a_{{{sub}}}^{{{sup}}}$'

    net = [
        {
            'top': '$l_1$',
            'bot': 'Capa de Entrada',
            'display': [1, 0, 1]
        },
        {
            'top': '$l_2$',
            'bot': 'Capa Oculta',
            'display': [1, 1, 0, 1, 1]
        },
        {
            'top': '$l_3$',
            'bot': 'Capa de Salida',
            'display': [1, 0, 1, 0, 1]
        }
    ]

    bot_left = (0, 0)
    top_right = (10, 12)
    v_offset = 2
    h_offset = 2
    x_rect_offset = 0.2
    y_rect_offset = 0.8
    node_radius = 0.5
    inter_node = 1.5
    inter_layer = 3
    full_width = top_right[0] - bot_left[0]
    full_height = top_right[1] - bot_left[1]

    left = bot_left[0] + h_offset
    bot = bot_left[1] + v_offset
    right = top_right[0] - h_offset
    top = top_right[1] - v_offset

    def get_n_nodes(layer):
        if 'length' in layer:
            return layer['length']
        else:
            return len(layer['display'])

    def get_layer_height(layer):
        n_nodes = get_n_nodes(layer)
        return (n_nodes - 1) * inter_node

    def get_visibility(layer, n_index):
        if 'display' in layer:
            return 1 == layer['display'][n_index]
        else:
            return 1

    def get_vertical_center(net):
        heights = [
            get_layer_height(layer)
            for layer in net
        ]
        return max(heights) / 2

    vertical_center = get_vertical_center(net)
    colors = [
        {
            'name': 'mandarin_red',
            'rgb': (229, 80, 57)
        },
        {
            'name': 'azraq_blue',
            'rgb': (74, 105, 189)
        },
        {
            'name': 'dupain',
            'rgb': (96, 163, 188)
        }
    ]

    for color in colors:
        c.definecolor(color['name'], color['rgb'])

    with c.pspicture(bl=bot_left, tr=top_right):
        for l_index, layer in enumerate(net):
            c.psset(['linecolor={0}'.format(colors[l_index]['name'])])
            x = left + l_index * inter_layer
            n_nodes = get_n_nodes(layer)
            vertical_delta = vertical_center - get_layer_height(layer) / 2
            top_rect = top - vertical_delta + y_rect_offset
            bot_rect = (
                top - vertical_delta - y_rect_offset
                - (n_nodes - 1) * inter_node
            )
            left_rect = x - node_radius - x_rect_offset
            right_rect = x + node_radius + x_rect_offset
            c.pspolygon(
                [
                    'fillstyle=solid',
                    'fillcolor={0}!30'.format(colors[l_index]['name']),
                    'linearc=4pt',
                    'linewidth=1pt'
                ],
                [
                    (left_rect, top_rect),
                    (left_rect, bot_rect),
                    (right_rect, bot_rect),
                    (right_rect, top_rect)
                ]
            )
            c.uput(
                (x, top_rect),
                layer['top'],
                refangle=90
            )
            c.uput(
                (x, bot_rect),
                layer['bot'],
                refangle=270
            )
            for n_index in range(n_nodes):
                y = top - vertical_delta - n_index * inter_node
                is_visible = get_visibility(layer, n_index)
                if is_visible:
                    if n_index == n_nodes - 2:
                        c.cnodeput(
                            ['radius=0.6cm'],
                            (x, y),
                            a_name(n_index, l_index),
                            a_label(f'S_{{l_{l_index+1}}}-1', l_index)
                        )
                    elif n_index == n_nodes - 1:
                        c.cnodeput(
                            ['radius=0.6cm'],
                            (x, y),
                            a_name(n_index, l_index),
                            a_label(f'S_{{l_{l_index+1}}}', l_index)
                        )
                    else:
                        c.cnodeput(
                            ['radius=0.6cm'],
                            (x, y),
                            a_name(n_index, l_index),
                            a_label(n_index, l_index)
                        )
                else:
                    c.psdots(
                        ['dotsize=3pt'],
                        [
                            (x, y + 0.3),
                            (x, y),
                            (x, y - 0.3)
                        ]
                    )
        for l_index, layer in enumerate(net[:-1]):
            start_nodes = get_n_nodes(layer)
            for start_index in range(start_nodes):
                end_nodes = get_n_nodes(net[l_index+1])
                for end_index in range(end_nodes):
                    start_name = a_name(start_index, l_index)
                    end_name = a_name(end_index, l_index + 1)
                    c.ncline(
                        ['linecolor=black!70'],
                        start_name,
                        end_name
                    )
    w.add_to_body(c.get_buffer())
    w.write_body(filepath)
