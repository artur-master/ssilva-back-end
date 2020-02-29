import os
run_create_database = "python manage.py migrate --fake-initial"

run_permissions = "python manage.py loaddata fixtures/permissions.json"
run_roles = "python manage.py loaddata fixtures/roles.json"

run_django_users_test = "python manage.py loaddata fixtures/django_users_test.json"
run_users_test = "python manage.py loaddata fixtures/users_test.json"

run_contacts_info_types = "python manage.py loaddata fixtures/contact_info_types.json"
run_regiones = "python manage.py loaddata fixtures/regiones.json"
run_provincias = "python manage.py loaddata fixtures/provincias.json"
run_comunas = "python manage.py loaddata fixtures/comunas.json"

run_inmobiliarias_test = "python manage.py loaddata fixtures/inmobiliarias_test.json"
run_constructoras_test = "python manage.py loaddata fixtures/constructoras_test.json"
run_inmobiliaria_contact_info_test = "python manage.py loaddata fixtures/inmobiliaria_contact_info.json"
run_users_inmobiliaria_test = "python manage.py loaddata fixtures/users_inmobiliaria_test.json"

run_inmueble_inmueble_types = "python manage.py loaddata fixtures/inmueble_inmueble_types.json"
run_inmueble_types_test = "python manage.py loaddata fixtures/inmueble_types_test.json"
run_inmueble_states = "python manage.py loaddata fixtures/inmueble_states.json"
run_orientations_test = "python manage.py loaddata fixtures/orientations_test.json"
run_tipologias_test = "python manage.py loaddata fixtures/tipologias_test.json"

run_notification_types = "python manage.py loaddata fixtures/notification_types.json"

run_proyecto_approval_states = "python manage.py loaddata fixtures/proyecto_approval_states.json"

run_plan_medios_states = "python manage.py loaddata fixtures/plan_medios_states.json"
run_borrador_promesa_states = "python manage.py loaddata fixtures/borrador_promesa_states.json"
run_ingreso_comisiones_states = "python manage.py loaddata fixtures/ingreso_comisiones_states.json"

run_proyecto_log_types = "python manage.py loaddata fixtures/proyecto_log_types.json"
run_proyecto_etapas_states = "python manage.py loaddata fixtures/proyecto_etapas_states.json"

run_instituciones_financieras = "python manage.py loaddata fixtures/instituciones_financieras.json"
run_aseguradoras = "python manage.py loaddata fixtures/aseguradoras.json"

run_user_proyecto_types = "python manage.py loaddata fixtures/user_proyecto_types.json"
run_user_inmobiliaria_types = "python manage.py loaddata fixtures/user_inmobiliaria_types.json"

run_users_proyecto_test = "python manage.py loaddata fixtures/users_proyecto_test.json"
run_proyecto_aseguradora = "python manage.py loaddata fixtures/proyecto_aseguradora.json"
run_proyectos_test = "python manage.py loaddata fixtures/proyectos_test.json"
run_proyecto_contact_info_test = "python manage.py loaddata fixtures/proyecto_contact_info.json"

run_api_update = "python manage.py loaddata fixtures/api_update.json"
run_ufs = "python manage.py loaddata fixtures/ufs.json"
run_constants_numerics = "python manage.py loaddata fixtures/constants_numerics.json"

run_contact_method_types = "python manage.py loaddata fixtures/contact_method_types.json"
run_finding_types = "python manage.py loaddata fixtures/finding_types.json"
run_cotizacion_types = "python manage.py loaddata fixtures/cotizacion_types.json"
run_cotizacion_states = "python manage.py loaddata fixtures/cotizacion_states.json"

run_counter_history = "python manage.py loaddata fixtures/counter_history.json"
run_counter_folio = "python manage.py loaddata fixtures/counter_folio.json"

run_etapas_test = "python manage.py loaddata fixtures/etapas_test.json"
run_inmuebles_test = "python manage.py loaddata fixtures/inmuebles_test.json"

run_reserva_states = "python manage.py loaddata fixtures/reserva_states.json"

run_venta_log_types = "python manage.py loaddata fixtures/venta_log_types.json"
run_paytypes = "python manage.py loaddata fixtures/paytypes.json"

# Ejecutar Comandos para inicializar base de datos con migraciones
os.system(run_create_database)

# Ejecutar Fixtures (data inicial)
os.system(run_permissions)
os.system(run_roles)
os.system(run_django_users_test)
os.system(run_users_test)
os.system(run_regiones)
os.system(run_provincias)
os.system(run_comunas)

os.system(run_notification_types)

os.system(run_contacts_info_types)

os.system(run_user_inmobiliaria_types)
os.system(run_inmobiliarias_test)
os.system(run_constructoras_test)
os.system(run_inmobiliaria_contact_info_test)
os.system(run_users_inmobiliaria_test)

os.system(run_inmueble_inmueble_types)
os.system(run_inmueble_types_test)
os.system(run_inmueble_states)
os.system(run_orientations_test)
os.system(run_tipologias_test)

os.system(run_proyecto_approval_states)

os.system(run_plan_medios_states)
os.system(run_borrador_promesa_states)
os.system(run_ingreso_comisiones_states)

os.system(run_proyecto_log_types)
os.system(run_proyecto_etapas_states)

os.system(run_instituciones_financieras)
os.system(run_aseguradoras)

os.system(run_user_proyecto_types)
os.system(run_proyecto_aseguradora)
os.system(run_proyectos_test)
os.system(run_users_proyecto_test)
os.system(run_proyecto_contact_info_test)

os.system(run_api_update)
os.system(run_ufs)
os.system(run_constants_numerics)

os.system(run_contact_method_types)
os.system(run_finding_types)
os.system(run_cotizacion_types)
os.system(run_cotizacion_states)

os.system(run_counter_history)
os.system(run_counter_folio)

# os.system(run_etapas_test)
# os.system(run_inmuebles_test)

os.system(run_reserva_states)
os.system(run_venta_log_types)
os.system(run_paytypes)
