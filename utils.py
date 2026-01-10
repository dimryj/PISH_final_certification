import re 

def is_valid_email(email):
    """
        Проверка email.

        Parameters
        --------
        email : str
            Строка с email-адресом для проверки
            Ограничения:
                - Должен содержать символ @
                - Должен содержать домен с точкой
                - Допустимые символы: буквы, цифры, точки, подчеркивания, проценты, плюс, дефис

        Returns
        -----------
        bool :
            True, если email корректен
            False, если email не соответствует формату

        Examples
        --------
        >>> is_valid_email('test@example.ru')
        True
        >>> is_valid_email('invalid_email')
        False
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

def clean_string(text):
    """
    Очистка строки от лишних пробелов и форматирование.

    Parameters
    ----------
    text : str
        Исходная строка для обработки
        Ограничения:
            - Принимает любую строку
            - Пустая строка возвращается как пустая

    Returns
    -------
    str
        Отформатированная строка:
            - Все множественные пробелы заменены на одиночные
            - Удалены пробелы в начале и конце строки

    Examples
    --------
    >>> clean_string('   Hello   World   ')
    'Hello World'
    >>> clean_string('This   is   a   test')
    'This is a test'
    """
    return re.sub(r"\s+", " ", text.strip())