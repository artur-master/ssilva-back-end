import locale
from common.snippets.checks.utils_check import convert_number_to_words
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from datetime import datetime


# Set local zone to america
locale.setlocale(locale.LC_TIME, '')
# locale.setlocale(locale.LC_ALL,'es_ES.UTF-8')

# Funciones para generacion de cheque antiguo

def print_number(pdf, number):
    number_str = str(number)

    if len(number_str) == 1:
        pdf.drawString(707, 391, number_str[0] + ".-")
    elif len(number_str) == 2:
        pdf.drawString(707, 391, number_str[0] + number_str[1] + ".-")
    elif len(number_str) == 3:
        pdf.drawString(707, 391, number_str[0] + number_str[1] +
                       number_str[2] + ".-")
    elif len(number_str) == 4:
        pdf.drawString(707, 391, number_str[0] + "." + number_str[1] +
                       number_str[2] + number_str[3] + ".-")
    elif len(number_str) == 5:
        pdf.drawString(707, 391, number_str[0] + number_str[1] + "." +
                       number_str[2] + number_str[3] + number_str[4] + ".-")
    elif len(number_str) == 6:
        pdf.drawString(707, 391, number_str[0] + number_str[1] +
                       number_str[2] + "." + number_str[3] + number_str[4] +
                       number_str[5] + ".-")
    elif len(number_str) == 7:
        pdf.drawString(707, 391, number_str[0] + "." + number_str[1] +
                       number_str[2] + number_str[3] + "." + number_str[4] +
                       number_str[5] + number_str[6] + ".-")
    elif len(number_str) == 8:
        pdf.drawString(707, 391, number_str[0] + number_str[1] + "." +
                       number_str[2] + number_str[3] + number_str[4] + "." +
                       number_str[5] + number_str[6] + number_str[7] + ".-")
    else:
        pdf.drawString(707, 391, number_str[0] + number_str[1] +
                       number_str[2] + "." + number_str[3] + number_str[4] +
                       number_str[5] + "." + number_str[6] + number_str[7] +
                       number_str[8] + ".-")


def print_date(pdf, date, has_year):
    # day = datetime.strftime(date, '%d')
    # month = datetime.strftime(date, '%B')
    # year = datetime.strftime(date, '%Y')
    #
    # if has_year:
    #     pdf.drawString(580, 350, day)
    #     pdf.drawString(660, 350, month)
    #     pdf.drawString(772, 350, year[2] + year[3])
    # else:
    #     date = day + " de " + month + " del " + year
    #     pdf.drawString(653, 350, date)
    date = date[:10]
    date = datetime.strptime(date, "%Y-%m-%d")
    day = datetime.strftime(date, '%d')
    month = datetime.strftime(date, '%B')
    year = datetime.strftime(date, '%Y')
    date = day + " de " + month + " del " + year

    pdf.drawString(653, 350, date)


def print_beneficiary(pdf, beneficiary):
    try:
        pdf.drawString(407, 332, beneficiary.upper())
    except:
        pass


def print_number_words(pdf, words):
    phrase = words.split()
    number = len(phrase)
    try:
        if number == 1:
            pdf.drawString(407, 315, phrase[0])
        elif number == 2:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1])
        elif number == 3:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2])
        elif number == 4:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3])
        elif number == 5:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4])
        elif number == 6:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
        elif number == 7:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6])
        elif number == 8:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7])
        elif number == 9:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7] + " " + phrase[8])
        elif number == 10:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                        " " + phrase[9])
        elif number == 11:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                        " " + phrase[9] + " " + phrase[10])
        elif number == 12:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                        " " + phrase[9] + " " + phrase[10] + " " + phrase[11])
        elif number == 13:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                        " " + phrase[9] + " " + phrase[10] + " " + phrase[11] +
                        " " + phrase[12])
        else:
            pdf.drawString(
                407, 315, phrase[0] + " " + phrase[1] + " " + phrase[2] +
                        " " + phrase[3] + " " + phrase[4] + " " + phrase[5])
            pdf.drawString(
                362, 299, phrase[6] + " " + phrase[7] + " " + phrase[8] +
                        " " + phrase[9] + " " + phrase[10] + " " + phrase[11] +
                        " " + phrase[12] + " " + phrase[13])
    except:
        pass


def print_crossed(pdf):
    pdf.line(396, 196, 396, 500)
    pdf.line(420, 196, 420, 500)


def print_nominative(pdf):
    pdf.drawString(362, 329, "xxxxxx")


def print_to_the_carrier(pdf):
    pdf.drawString(744, 320, "XXXXXX")

def print_account_number(pdf, account_number):
    pdf.drawString(744, 318, "XXXXXX")    
    
def generate_old_check(date, number, has_year, beneficiary, nominative, crossed, to_the_carrier, account_number):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Cheque_Antiguo.pdf"'

    pdf = canvas.Canvas(response)
    pdf.setPageSize(landscape(letter))

    words = convert_number_to_words(number)
    print_number(pdf, number)
    print_date(pdf, date, has_year)
    print_beneficiary(pdf, beneficiary)
    print_number_words(pdf, words)
    print_account_number(pdf, account_number)

    if crossed:
        print_crossed(pdf)

    if nominative:
        print_nominative(pdf)

    if to_the_carrier:
        print_to_the_carrier(pdf)

    pdf.save()

    return response
