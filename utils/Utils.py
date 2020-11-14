def difference_between_lists(list1: list, list2: list) -> list:
    """
    :param list1: Primeira lista
    :param list2: Segunda lista
    :type list1: list
    :type list2: list
    :return: Vai retornar uma lista, com os itens que não se repetiram nas listas
    :rtype: list
    """
    return list(set(list1) - set(list2)) + list(set(list2) - set(list1))

def datetime_format(date1, date2=None) -> str:
    """
    :param date1: objeto datetime que vai ser subtraido pelo date2
    :param date2: Parâmetro opcional, se não for passado nada, vai pegar o datetime utc atual
    :type date1: datetime utc
    :type date2: datetime utc
    :return: vai retornar a string formatada, da diferença da date2 pela date1
    :rtype: str
    """
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
    """
        variável que vai controlar quantos dados já foram mostrados
        para evitar que a string saia muito grande, como:
        2 anos, 5 meses, 1 dia, 2 horas, 3 minutos e 2 segundos.
        com a variável limitando, vai sair assim:
        2 anos, 5 meses e 1 dia.
    """
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

