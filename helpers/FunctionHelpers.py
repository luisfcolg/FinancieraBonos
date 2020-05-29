import datetime
import random


def generateIsin(countryCode):
    '''
    Esta función será usada para calcular el ISIN en base al código de cada país
    :param countryCode: El código del país en base a la moneda
    :type countryCode: str
    :return: Devuelve el código ISIN
    :rtype: str
    '''
    isin = "" + countryCode[0] + countryCode[1]
    digits = []

    for i in range(9):
        rnd = random.randint(0, 9)
        isin += str(rnd)
        digits.append(rnd)

    digit = 0
    for i in range(9):
        digit += digits[i]

    isin += str(digit % 10)

    return isin


def compareDates(before, after):
    '''
    Esta función sera usada para comparar dos fechas
    :param before: La fecha supuestamente anterior
    :type before: str
    :param after: La fecha supuestamente posterior
    :type after: str
    :returns: Devuelve un booleano del resultado. Será verdadero si before es menor o igual a after
    :rtype: bool
    '''
    x = datetime.datetime(int(before.split("-")[0]), int(before.split("-")[1]), int(before.split("-")[2]))
    y = datetime.datetime(int(after.split("-")[0]), int(after.split("-")[1]), int(after.split("-")[2]))

    return x < y