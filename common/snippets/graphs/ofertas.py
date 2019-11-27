from common import constants
from .utils import add_node, set_color

## Creacion de grafo para oferta



## Creacion de nodos
def return_nodes(oferta, node_ac_co, node_i_ai, node_ac_pc,
                 node_f_rg, node_l_p_a, node_l_p):
    nodes = list()

    if oferta.OfertaState == constants.OFERTA_STATE[0]:
        set_color(node_ac_co, 'green')
        nodes.append(node_ac_co)

        if oferta.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[0]:
            set_color(node_i_ai, 'yellow')
        elif oferta.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[1]:
            set_color(node_i_ai, 'orange')
        elif oferta.AprobacionInmobiliariaState == constants.APROBACION_INMOBILIARIA_STATE[2]:
            set_color(node_i_ai, 'green')
        else:
            set_color(node_i_ai, 'red')

        nodes.append(node_i_ai)

        if oferta.PreAprobacionCreditoState == constants.PRE_APROBACION_CREDITO_STATE[0]:
            set_color(node_ac_pc, 'white')
        elif oferta.PreAprobacionCreditoState == constants.PRE_APROBACION_CREDITO_STATE[1]:
            set_color(node_ac_pc, 'white')
        elif oferta.PreAprobacionCreditoState == constants.PRE_APROBACION_CREDITO_STATE[2]:
            set_color(node_ac_pc, 'green')
        else:
            set_color(node_ac_pc, 'red')

        nodes.append(node_ac_pc)

        if oferta.RecepcionGarantiaState == constants.RECEPCION_GARANTIA_STATE[0]:
            set_color(node_f_rg, 'white')
        else:
            set_color(node_f_rg, 'green')

        nodes.append(node_f_rg)

        set_color(node_l_p_a, 'white')
        nodes.append(node_l_p_a)

        set_color(node_l_p, 'white')
        nodes.append(node_l_p)

    elif oferta.OfertaState == constants.OFERTA_STATE[1]:
        set_color(node_ac_co, 'green')
        nodes.append(node_ac_co)

        set_color(node_i_ai, 'green')
        nodes.append(node_i_ai)

        set_color(node_ac_pc, 'green')
        nodes.append(node_ac_pc)

        set_color(node_f_rg, 'green')
        nodes.append(node_f_rg)

        set_color(node_l_p_a, 'orange')
        nodes.append(node_l_p_a)

        set_color(node_l_p, 'white')
        nodes.append(node_l_p)

    elif oferta.OfertaState == constants.OFERTA_STATE[2]:
        set_color(node_ac_co, 'green')
        nodes.append(node_ac_co)

        set_color(node_i_ai, 'green')
        nodes.append(node_i_ai)

        set_color(node_ac_pc, 'green')
        nodes.append(node_ac_pc)

        set_color(node_f_rg, 'green')
        nodes.append(node_f_rg)

        set_color(node_l_p, 'red')
        nodes.append(node_l_p)

        set_color(node_l_p_a, 'white')
        nodes.append(node_l_p_a)

    elif oferta.OfertaState == constants.OFERTA_STATE[3]:
        set_color(node_ac_co, 'green')
        nodes.append(node_ac_co)

        set_color(node_i_ai, 'green')
        nodes.append(node_i_ai)

        set_color(node_ac_pc, 'green')
        nodes.append(node_ac_pc)

        set_color(node_f_rg, 'green')
        nodes.append(node_f_rg)

        set_color(node_l_p, 'green')
        nodes.append(node_l_p)

        set_color(node_l_p_a, 'green')
        nodes.append(node_l_p_a)

    else:
        set_color(node_ac_co, 'green')
        nodes.append(node_ac_co)

        set_color(node_i_ai, 'green')
        nodes.append(node_i_ai)

        set_color(node_ac_pc, 'green')
        nodes.append(node_ac_pc)

        set_color(node_f_rg, 'green')
        nodes.append(node_f_rg)

        set_color(node_l_p, 'green')
        nodes.append(node_l_p)

        set_color(node_l_p_a, 'red')
        nodes.append(node_l_p_a)

    return nodes


def create_relation(node_ac_co, node_i_ai, node_ac_pc,
                    node_f_rg, node_l_p_a, node_l_p):

    relation = "{0}-{1}-{2}-{3}-{4}-{5}".format(node_ac_co['Label'], node_i_ai['Label'],
                                                node_ac_pc['Label'], node_f_rg['Label'],
                                                node_l_p_a['Label'], node_l_p['Label'])

    return relation


# Creacion de grafo 
def return_graph(oferta):
    graph = dict()
    result = list()

    # Nodos
    node_ac_co = add_node('AC', 'Oferta')
    node_i_ai = add_node('IN', 'Aprobación inmobiliaria')
    node_ac_pc = add_node('AC', 'Preaprobación crédito')
    node_f_rg = add_node('FI', 'Recepción de garantía')
    node_l_p_a = add_node('LG', 'Pendiente legal')
    #node_l_p = add_node('LG', 'Promesa/Oferta cancelada ')
    node_l_p = add_node('LG', 'Promesa')

    nodes = return_nodes(oferta, node_ac_co, node_i_ai, node_ac_pc,
                         node_f_rg, node_l_p_a, node_l_p)

    relation = create_relation(node_ac_co, node_i_ai, node_ac_pc,
                               node_f_rg, node_l_p_a, node_l_p)

    result.append(relation)

    graph['Node'] = nodes
    graph['Result'] = result

    return graph
