from os import listdir
from json import load
import re
from re import sub
from random import choice, randint
import string as string_lib


def random_color():
    return int(f'0x{randint(0, 255):01x}{randint(0, 255):02x}{randint(0, 255):02x}', 16)

def difference_between_lists(list1: list, list2: list) -> list:
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))

def datetime_format(date1, date2=None) -> str:
    from dateutil.relativedelta import relativedelta
    from datetime import datetime
    if date2 is None:
        date2 = datetime.utcnow()
    time = relativedelta(date2, date1)
    years = abs(time.years)
    months = abs(time.months)
    days = abs(time.days)
    hours = abs(time.hours)
    minutes = abs(time.minutes)
    seconds = abs(time.seconds)
    dados = 0
    dt_str = ''
    if (years == 0) and (months == 0) and (days <= 1):
        if days == 0:
            d_str = 'Hoje'
        elif days == 1:
            d_str = 'Ontem'
        else:
            d_str = ''
        if hours > 1:
            h_str = f'{hours} horas'
        elif hours == 1:
            h_str = f'{hours} hora'
        else:
            h_str = ''
        if minutes > 1:
            m_str = f'{minutes} minutos'
        elif minutes == 1:
            m_str = f'{minutes} minuto'
        else:
            m_str = ''
        if seconds > 1:
            s_str = f'{seconds} segundos'
        elif seconds == 1:
            s_str = f'{seconds} segundo'
        else:
            s_str = ''
        if h_str and m_str and s_str:
            dt_str = f'{d_str} há {h_str}, {m_str} e {s_str}.'
        elif h_str and m_str:
            dt_str = f'{d_str} há {h_str} e {m_str}.'
        elif h_str and s_str:
            dt_str = f'{d_str} há {h_str} e {s_str}.'
        elif m_str and s_str:
            dt_str = f'{d_str} há {m_str} e {s_str}.'
        elif h_str:
            dt_str = f'{d_str} há {h_str}.'
        elif m_str:
            dt_str = f'{d_str} há {m_str}.'
        elif s_str:
            dt_str = f'{d_str} há {s_str}.'
        elif (h_str == '') and (m_str == '') and (s_str == ''):
            dt_str = f'{d_str}.'
        return dt_str
    if years > 1:
        dt_str += f'{years} anos'
        dados += 1
    elif years == 1:
        dt_str += f'{years} ano'
        dados += 1
    if months > 1:
        if years >= 1:
            dt_str += ', '
        dt_str += f'{months} meses'
        dados += 1
    elif months == 1:
        if years >= 1:
            dt_str += ', '
        dt_str += f'{months} mês'
        dados += 1
    if days > 1:
        if (years >= 1) or (months >= 1):
            dt_str += ', '
        dt_str += f'{days} dias'
        dados += 1
    elif days == 1:
        if (years >= 1) or (months >= 1):
            dt_str += ', '
        dt_str += f'{days} dia'
        dados += 1
    if dados < 3:
        if hours > 1:
            if (years >= 1) or (months >= 1) or (days >= 1):
                dt_str += ', '
            dt_str += f'{hours} horas'
            dados += 1
        elif hours == 1:
            if (years >= 1) or (months >= 1) or (days >= 1):
                dt_str += ', '
            dt_str += f'{hours} hora'
            dados += 1
        if dados < 3:
            if minutes > 1:
                if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1):
                    dt_str += ', '
                dt_str += f'{minutes} minutos'
                dados += 1
            elif minutes == 1:
                if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1):
                    dt_str += ', '
                dt_str += f'{minutes} minuto'
                dados += 1
            if dados < 3:
                if seconds > 1:
                    if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1) or (minutes >= 1):
                        dt_str += ', '
                    dt_str += f'{seconds} segundos'
                elif seconds == 1:
                    if (years >= 1) or (months >= 1) or (days >= 1) or (hours >= 1) or (minutes >= 1):
                        dt_str += ', '
                    dt_str += f'{seconds} segundo'
    dt_str += '.'
    if dt_str.rfind(',') != -1:
        dt_str = dt_str[:dt_str.rfind(',')] + ' e' + dt_str[dt_str.rfind(',') + 1:]
    return dt_str

def is_number(string):
    try:
        if string.find(',') != -1:

            string = string.replace(',', '.')

        string = string.replace(' ', '')

        if string.isalpha():
            return False

        for char in string_lib.ascii_lowercase:
            if char in string.lower():
                return False
        float(string)
        return True
    except ValueError:
        return False



def prettify_number(number, br=True, truncate=False):

    if not is_number(str(number)):
        return number

    if truncate:
        number = sub(r'^(\d+\.\d{,2})\d*$', r'\1', str(number))

    number = str(number).split('.')
    decimal = number[-1] if len(number) > 1 else ''
    decimal = decimal if decimal.strip('0') else ''
    number = number[0]
    separator = '.' if br else ','
    decimal_separator = ''
    if decimal != '':
        decimal_separator = ',' if br else '.'
    number = f'{int(number):_}'.replace('_', separator)
    return f'{number}{decimal_separator}{decimal}'



with open('cogs/img/data/avatars.json', encoding='utf-8') as avatars:
    avatars = load(avatars)


