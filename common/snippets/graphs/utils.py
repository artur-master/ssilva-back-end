
# Funciones de utilidad para la creacion de grafos customs


def add_node(label, description):
    node = dict()
    node['Label'] = label
    node['Description'] = description

    return node


def set_color(node, color):
    node['Color'] = color
