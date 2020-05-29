import datetime
import random
import logging


logging.basicConfig(level=logging.DEBUG, filename='../events.log')


def generateIsin(countryCode):
    '''
    Esta función será usada para calcular el ISIN en base al código de cada país
    :param countryCode: El código del país en base a la moneda
    :type countryCode: str
    :return: Devuelve el código ISIN
    :rtype: str
    '''

    logging.debug("Calculando ISIN")
    # Tomar el codigo del pais
    isin = "" + countryCode[0] + countryCode[1]
    digits = []
    # Calcular 9 numeros aleatorios
    for i in range(9):
        rnd = random.randint(0, 9)
        isin += str(rnd)
        digits.append(rnd)
    # Sumar numeros
    digit = 0
    for i in range(9):
        digit += digits[i]
    # Agregar el digito de la suma de los numeros
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

    logging.debug("Comparando fechas")
    # Convertir fechas
    x = datetime.datetime(int(before.split("-")[0]), int(before.split("-")[1]), int(before.split("-")[2]))
    y = datetime.datetime(int(after.split("-")[0]), int(after.split("-")[1]), int(after.split("-")[2]))
    # Comparar fechas
    return x < y