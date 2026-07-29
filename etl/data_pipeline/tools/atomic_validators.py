import re
from datetime import datetime


def validar_cpf(cpf: str) -> bool:
    """
    Valida formato de CPF: XXX.XXX.XXX-XX
    """
    if not cpf:
        return False
    
    padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
    return bool(re.match(padrao, cpf))

def validar_cep(cep: str) -> bool:
    """
    Valida formato de CEP: XXXXX-XXX
    """
    if not cep:
        return False

    padrao = r"^\d{5}-\d{3}$"
    return bool(re.match(padrao, cep))


def validar_email(email: str) -> bool:
    """
    Valida e-mail no formato padrão.
    """
    if not email:
        return False

    padrao = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(padrao, email))

def validar_data(data_str: str) -> bool:
    """
    Verifica se a data está no formato YYYY-MM-DD
    e se representa uma data válida.
    """
    if not data_str:
        return False

    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except:
        return False


def validar_status(status: str) -> bool:
    """
    Verifica se o status está entre os valores aceitos.
    """
    if not status:
        return False

    status = status.strip().lower()
    valores_validos = {"ativo", "inativo", "suspenso"}

    return status in valores_validos