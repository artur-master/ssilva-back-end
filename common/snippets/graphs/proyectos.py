from common import constants
from .utils import add_node, set_color


# Creacion de grafo para proyecto

def return_nodes(proyecto, node_jp_cp, node_l_bp, node_jp_if,
                 node_l_ap, node_gc_ap):
    nodes = list()

    if proyecto.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[0]:
        set_color(node_jp_cp, 'green')
        nodes.append(node_jp_cp)

        if proyecto.BorradorPromesaState.Name == constants.BORRADOR_PROMESA_STATE[0]:
            set_color(node_l_bp, 'red')
            set_color(node_jp_if, 'white')
        else:
            set_color(node_l_bp, 'green')
            set_color(node_jp_if, 'red')

        nodes.append(node_l_bp)
        nodes.append(node_jp_if)

        set_color(node_l_ap, 'white')
        nodes.append(node_l_ap)

        set_color(node_gc_ap, 'white')
        nodes.append(node_gc_ap)

    elif proyecto.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[1]:
        set_color(node_jp_cp, 'green')
        nodes.append(node_jp_cp)

        set_color(node_l_bp, 'green')
        nodes.append(node_l_bp)

        set_color(node_jp_if, 'green')
        nodes.append(node_jp_if)

        set_color(node_l_ap, 'red')
        nodes.append(node_l_ap)

        set_color(node_gc_ap, 'white')
        nodes.append(node_gc_ap)

    elif proyecto.ProyectoApprovalState.Name == constants.PROYECTO_APPROVAL_STATE[2]:
        set_color(node_jp_cp, 'green')
        nodes.append(node_jp_cp)

        set_color(node_l_bp, 'green')
        nodes.append(node_l_bp)

        set_color(node_jp_if, 'green')
        nodes.append(node_jp_if)

        set_color(node_l_ap, 'green')
        nodes.append(node_l_ap)

        set_color(node_gc_ap, 'red')
        nodes.append(node_gc_ap)

    return nodes


def create_relation(node_jp_cp, node_l_bp, node_jp_if,
                    node_l_ap, node_gc_ap):

    relation = "{0}-{1}-{2}-{3}-{4}".format(node_jp_cp['Label'], node_l_bp['Label'],
                                                        node_jp_if['Label'], node_l_ap['Label'],
                                                        node_gc_ap['Label'])

    return relation


def return_graph(proyecto):
    graph = dict()
    result = list()

    # Nodos
    node_jp_cp = add_node('JP', 'Crear proyecto')
    node_l_bp = add_node('L', 'Pendiente de Información')
    node_jp_if = add_node('JP', 'Revisión Proyecto')
    node_l_ap = add_node('L', 'Aprobación Inmuebles')
    node_gc_ap = add_node('GC', 'Aprobación Final')

    nodes = return_nodes(proyecto, node_jp_cp, node_l_bp, node_jp_if,
                         node_l_ap, node_gc_ap)

    relation = create_relation(node_jp_cp, node_l_bp, node_jp_if,
                               node_l_ap, node_gc_ap)

    result.append(relation)

    graph['Node'] = nodes
    graph['Result'] = result

    return graph
