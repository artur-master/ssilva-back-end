from django.db import connection
from rest_framework.exceptions import ValidationError

from empresas_and_proyectos.models.inmuebles import Orientation


# Funcion realizada por Rafael Torres

def insert_properties_orientaations(
        properties, orientations_dict, relation_table):
    orientaciones = Orientation.objects.all()
    insertions = list()
    for inmueble in properties:
        if orientations_dict.get(inmueble.InmuebleID):
            property_o = orientations_dict.get(inmueble.InmuebleID)
            aux_orientations = property_o.split('-')
            for orientation_name in aux_orientations:
                if orientation_name == "Nor":
                    orientation_name = "Norte"
                elif orientation_name == "No aplica":
                    continue
                try:
                    orientacion = orientaciones.get(Name=orientation_name)
                    insertions.append((inmueble.pk, orientacion.pk))
                except:
                    raise ValidationError("Unknown orientacion named %s" % orientation_name)

    if insertions:
        temp_query = "INSERT INTO public.\"{0}\" ".format(relation_table)
        temp_query += " (inmueble_id, orientation_id) VALUES "
        for (property_id, orientation_id) in insertions:
            aux_q = "({0}, {1}),".format(property_id, orientation_id)
            temp_query += aux_q
        temp_query = temp_query[:len(temp_query) - 1] + ";"
        with connection.cursor() as cursor:
            cursor.execute(temp_query)