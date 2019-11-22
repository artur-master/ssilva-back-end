from common.models import Comuna, ContactInfoType
from ventas.models.clientes import ClienteContactInfo

# Funciones realizadas por Rafael Torres

def save_cliente_return(validated_data, cliente, current_user):
    contacts_info_cliente_data = validated_data.pop('ContactInfo')

    if validated_data.get('ComunaID'):
        comuna = Comuna.objects.get(
            ComunaID=validated_data.pop('ComunaID'))
    else:
        comuna = None

    cliente.ComunaID = comuna
    cliente.Creator = current_user
    cliente.LastModifier = current_user

    for k in validated_data:
        if k in ['ComunaID', 'ContactInfo']:
            continue
        setattr(cliente, k, validated_data[k])

    cliente.save()

    contacts_cliente = ClienteContactInfo.objects.filter(
        UserID=cliente)

    if contacts_cliente.exists():
        contacts_cliente.delete()

    contact_list = list()
    for contact_info_data in contacts_info_cliente_data:
        contact_info_type = ContactInfoType.objects.get(
            ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
        client_contact = ClienteContactInfo()
        client_contact.UserID = cliente
        client_contact.ContactInfoTypeID = contact_info_type
        client_contact.Value = contact_info_data['Value']
        contact_list.append(client_contact)

    if contact_list:
        ClienteContactInfo.objects.bulk_create(contact_list)

    return cliente


def save_cliente(validated_data, cliente, current_user):
    contacts_info_cliente_data = validated_data.get('ContactInfo', [])

    comuna = None
    if validated_data.get('ComunaID'):
        comuna = Comuna.objects.get(
            ComunaID=validated_data.get('ComunaID'))

    if 'ComunaID' in validated_data:
        cliente.ComunaID = comuna

    cliente.LastModifier = current_user
    cliente.Creator = current_user

    for k in validated_data:
        if k in ['ComunaID', 'ContactInfo']:
            continue
        setattr(cliente, k, validated_data[k])

    cliente.save()

    if 'ContactInfo' in validated_data:
        contacts_cliente = ClienteContactInfo.objects.filter(
            UserID=cliente)

        if contacts_cliente.exists():
            contacts_cliente.delete()

    contact_list = list()
    for contact_info_data in contacts_info_cliente_data:
        contact_info_type = ContactInfoType.objects.get(
            ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
        client_contact = ClienteContactInfo()
        client_contact.UserID = cliente
        client_contact.ContactInfoTypeID = contact_info_type
        client_contact.Value = contact_info_data['Value']
        contact_list.append(client_contact)

    if contact_list:
        ClienteContactInfo.objects.bulk_create(contact_list)


def save_cliente_comuna(validated_data, cliente, comuna, current_user):
    contacts_info_cliente_data = validated_data.pop('ContactInfo')

    cliente.ComunaID = comuna
    cliente.Creator = current_user
    cliente.LastModifier = current_user

    for k in validated_data:
        if k in ['ComunaID', 'ContactInfo']:
            continue
        setattr(cliente, k, validated_data[k])

    cliente.save()

    contacts_cliente = ClienteContactInfo.objects.filter(
        UserID=cliente)

    if contacts_cliente.exists():
        contacts_cliente.delete()

    contact_list = list()
    for contact_info_data in contacts_info_cliente_data:
        contact_info_type = ContactInfoType.objects.get(
            ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
        client_contact = ClienteContactInfo()
        client_contact.UserID = cliente
        client_contact.ContactInfoTypeID = contact_info_type
        client_contact.Value = contact_info_data['Value']
        contact_list.append(client_contact)

    if contact_list:
        ClienteContactInfo.objects.bulk_create(contact_list)


def save_cliente_user_exists(validated_data, cliente, comuna, current_user, user):
    contacts_info_cliente_data = validated_data.pop('ContactInfo')

    cliente.ComunaID = comuna
    cliente.Creator = current_user
    cliente.LastModifier = current_user
    cliente.user_ptr = user

    for k in validated_data:
        if k in ['ComunaID', 'ContactInfo']:
            continue
        setattr(cliente, k, validated_data[k])

    # Crea un cliente con usuario existente
    cliente.__dict__.update(user.__dict__)
    cliente.save()

    contacts_cliente = ClienteContactInfo.objects.filter(
        UserID=cliente)

    if contacts_cliente.exists():
        contacts_cliente.delete()

    contact_list = list()
    for contact_info_data in contacts_info_cliente_data:
        contact_info_type = ContactInfoType.objects.get(
            ContactInfoTypeID=contact_info_data['ContactInfoTypeID'])
        client_contact = ClienteContactInfo()
        client_contact.UserID = cliente
        client_contact.ContactInfoTypeID = contact_info_type
        client_contact.Value = contact_info_data['Value']
        contact_list.append(client_contact)

    if contact_list:
        ClienteContactInfo.objects.bulk_create(contact_list)
