from common import constants
from .utils import add_node, set_color


# Creacion de grafo para proyecto

def return_nodes(reserva, node_v_cr, node_v_pi_r, node_ac_pc,
                 node_ac_ofe):
    nodes = list()

    if (reserva.ReservaStateID.Name == constants.RESERVA_STATE[0] or
            reserva.ReservaStateID.Name == constants.RESERVA_STATE[3]):

        set_color(node_v_cr, 'green')
        nodes.append(node_v_cr)

        set_color(node_v_pi_r, 'red')
        nodes.append(node_v_pi_r)

        set_color(node_ac_pc, 'white')
        nodes.append(node_ac_pc)

        set_color(node_ac_ofe, 'white')
        nodes.append(node_ac_ofe)

    elif reserva.ReservaStateID.Name == constants.RESERVA_STATE[1]:
        set_color(node_v_cr, 'green')
        nodes.append(node_v_cr)

        set_color(node_v_pi_r, 'green')
        nodes.append(node_v_pi_r)

        set_color(node_ac_pc, 'red')
        nodes.append(node_ac_pc)

        set_color(node_ac_ofe, 'white')
        nodes.append(node_ac_ofe)

    elif reserva.ReservaStateID.Name == constants.RESERVA_STATE[2]:
        set_color(node_v_cr, 'green')
        nodes.append(node_v_cr)

        set_color(node_v_pi_r, 'green')
        nodes.append(node_v_pi_r)

        set_color(node_ac_pc, 'green')
        nodes.append(node_ac_pc)

        set_color(node_ac_ofe, 'green')
        nodes.append(node_ac_ofe)

    return nodes


def create_relation(node_v_cr, node_v_pi_r, node_ac_pc,
                    node_ac_ofe):
    relation = "{0}-{1}-{2}-{3}".format(node_v_cr['Label'], node_v_pi_r['Label'],
                                        node_ac_pc['Label'], node_ac_ofe['Label'])

    return relation


def return_graph(reserva):
    graph = dict()
    result = list()

    # Nodos
    node_v_cr = add_node('V, JP', 'Crear reserva')
    node_v_pi_r = add_node('V', 'Pendiente información/Rechazada ')
    node_ac_pc = add_node('AC', 'Pendiente control')
    node_ac_ofe = add_node('AC', 'Oferta')

    nodes = return_nodes(reserva, node_v_cr, node_v_pi_r, node_ac_pc,
                         node_ac_ofe)

    relation = create_relation(node_v_cr, node_v_pi_r, node_ac_pc,
                               node_ac_ofe)

    result.append(relation)

    graph['Node'] = nodes
    graph['Result'] = result

    return graph
