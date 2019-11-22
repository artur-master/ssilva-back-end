from common.snippets.checks.utils_check import convert_number_to_words
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from datetime import datetime


# Funciones para generacion de cheque nuevo


def print_city(pdf, city):
    pdf.drawString(596, 353, city)


def print_date(pdf, date, has_year):
    date = date[:10]
    date = datetime.strptime(date, "%Y-%m-%d")
    date_str = datetime.strftime(date, '%d%m%Y')

    pdf.drawString(663, 353, date_str[0])
    pdf.drawString(678, 353, date_str[1])
    pdf.drawString(701, 353, date_str[2])
    pdf.drawString(715, 353, date_str[3])

    if has_year:
        pdf.drawString(735, 353, date_str[4])
        pdf.drawString(751, 353, date_str[5])

    pdf.drawString(766, 353, date_str[6])
    pdf.drawString(781, 353, date_str[7])


def print_number(pdf, number):
    number_str = str(number)

    if len(number_str) == 1:
        pdf.drawString(779, 380, number_str[0] + ".-")
    elif len(number_str) == 2:
        pdf.drawString(779, 380, number_str[1] + ".-")
        pdf.drawString(765, 380, number_str[0])
    elif len(number_str) == 3:
        pdf.drawString(779, 380, number_str[2] + ".-")
        pdf.drawString(765, 380, number_str[1])
        pdf.drawString(751, 380, number_str[0])
    elif len(number_str) == 4:
        pdf.drawString(779, 380, number_str[3] + ".-")
        pdf.drawString(765, 380, number_str[2])
        pdf.drawString(751, 380, number_str[1])
        pdf.drawString(737, 380, number_str[0] + ".")
    elif len(number_str) == 5:
        pdf.drawString(779, 380, number_str[4] + ".-")
        pdf.drawString(765, 380, number_str[3])
        pdf.drawString(751, 380, number_str[2])
        pdf.drawString(737, 380, number_str[1] + ".")
        pdf.drawString(723, 380, number_str[0])
    elif len(number_str) == 6:
        pdf.drawString(779, 380, number_str[5] + ".-")
        pdf.drawString(765, 380, number_str[4])
        pdf.drawString(751, 380, number_str[3])
        pdf.drawString(737, 380, number_str[2] + ".")
        pdf.drawString(723, 380, number_str[1])
        pdf.drawString(709, 380, number_str[0])
    elif len(number_str) == 7:
        pdf.drawString(779, 380, number_str[6] + ".-")
        pdf.drawString(765, 380, number_str[5])
        pdf.drawString(751, 380, number_str[4])
        pdf.drawString(737, 380, number_str[3] + ".")
        pdf.drawString(723, 380, number_str[2])
        pdf.drawString(709, 380, number_str[1])
        pdf.drawString(695, 380, number_str[0] + ".")
    elif len(number_str) == 8:
        pdf.drawString(779, 380, number_str[7] + ".-")
        pdf.drawString(765, 380, number_str[6])
        pdf.drawString(751, 380, number_str[5])
        pdf.drawString(737, 380, number_str[4] + ".")
        pdf.drawString(723, 380, number_str[3])
        pdf.drawString(709, 380, number_str[2])
        pdf.drawString(695, 380, number_str[1] + ".")
        pdf.drawString(681, 380, number_str[0])
    else:
        pdf.drawString(779, 380, number_str[8] + ".-")
        pdf.drawString(765, 380, number_str[7])
        pdf.drawString(751, 380, number_str[6])
        pdf.drawString(737, 380, number_str[5] + ".")
        pdf.drawString(723, 380, number_str[4])
        pdf.drawString(709, 380, number_str[3])
        pdf.drawString(695, 380, number_str[2] + ".")
        pdf.drawString(681, 380, number_str[1])
        pdf.drawString(667, 380, number_str[0])


def print_beneficiary(pdf, beneficiary):
    pdf.drawString(407, 330, beneficiary.upper())


def print_number_words(pdf, words):
    phrase = words.split()
    number = len(phrase)

    if number == 1:
        pdf.drawString(407, 311, phrase[0])
    elif number == 2:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1])
    elif number == 3:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2])
    elif number == 4:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3])
    elif number == 5:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4])
    elif number == 6:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
    elif number == 7:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6])
    elif number == 8:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7])
    elif number == 9:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7] + " " + phrase[8])
    elif number == 10:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                      " " + phrase[9])
    elif number == 11:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                      " " + phrase[9] + " " + phrase[10])
    elif number == 12:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                      " " + phrase[9] + " " + phrase[10] + " " + phrase[11])
    elif number == 13:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                      " " + phrase[9] + " " + phrase[10] + " " + phrase[11] +
                      " " + phrase[12])
    else:
        pdf.drawString(
            407, 311, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                      " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        pdf.drawString(
            362, 295, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                      " " + phrase[9] + " " + phrase[10] + " " + phrase[11] +
                      " " + phrase[12] + " " + phrase[13])


def print_crossed(pdf):
    pdf.line(460, 460, 280, 280)
    pdf.line(450, 430, 314, 290)


def print_nominative(pdf):
    pdf.drawString(361, 329, "xxxxxxx")


def print_to_the_carrier(pdf):
    pdf.drawString(744, 318, "XXXXXX")


def generate_new_check(city, date, number, has_year, beneficiary, nominative, crossed, to_the_carrier):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Cheque_Nuevo.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setPageSize(landscape(letter))

    city = city + ","
    words = convert_number_to_words(number)
    print_number(pdf, number)
    print_city(pdf, city)
    print_date(pdf, date, has_year)
    print_beneficiary(pdf, beneficiary)
    print_number_words(pdf, words)

    if crossed:
        print_crossed(pdf)

    if nominative:
        print_nominative(pdf)

    if to_the_carrier:
        print_to_the_carrier(pdf)

    pdf.save()

    return response
