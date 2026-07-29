from typing import Tuple, List, Dict
import pandas as pd
from data_pipeline.tools.atomic_validators import (
    validar_cpf,
    validar_cep,
    validar_email,
    validar_data,
    validar_status,
)

def validar_clientes_row(row: Dict) -> Tuple[bool, List[str]]:
    """
    Valida uma linha do DataFrame de clientes.
    Retorna uma tupla (é_válido, lista_de_erros).
    """
    erros = []


    # Campos obrigatórios
    if not row.get("id_cliente"):
        erros.append("id_cliente ausente ou inválido.")

    nome = row.get("nome")
    if not nome or not isinstance(nome, str):
        erros.append("nome ausente ou inválido.")

    # Validações de campo com atomic validators
    cpf = str(row.get("cpf"))
    if not validar_cpf(cpf):
        erros.append(f"CPF inválido: {cpf}")

    email = str(row.get("email"))
    if not validar_email(email):
        erros.append(f"Email inválido: {email}")

    data_nascimento = str(row.get("data_nascimento"))
    if not validar_data(data_nascimento):
        erros.append(f"Data de nascimento inválida: {data_nascimento}")

    status = str(row.get("status"))
    if not validar_status(status):
        erros.append(f"Status inválido: {status}")

    return (len(erros) == 0, erros)

def validar_endereco_row(row: Dict, clientes_validos_ids: set) -> Tuple[bool, List[str]]:
    """
    Valida um endereço individual e verifica integridade referencial com CLIENTES.
    """
    erros = []

    # Validação da FK
    id_cliente = row.get("id_cliente")
    if not id_cliente:
        erros.append("id_cliente ausente.")
    elif id_cliente not in clientes_validos_ids:
        erros.append(f"id_cliente {id_cliente} não existe entre os clientes válidos.")

    # Campos específicos de endereço
    cep = str(row.get("cep"))
    if not validar_cep(cep):
        erros.append(f"CEP inválido: {cep}")

    cidade = row.get("cidade")
    if not cidade or not isinstance(cidade, str):
        erros.append("cidade ausente ou inválida.")

    estado = row.get("estado")
    if not estado or not isinstance(estado, str):
        erros.append("estado ausente ou inválido.")

    return (len(erros) == 0, erros)

def validar_entidades(
    df_clientes: pd.DataFrame, df_enderecos: pd.DataFrame
) -> Dict[str, pd.DataFrame]:
    """
    Executa validação completa dos datasets CLIENTES e ENDEREÇOS.
    Retorna:
        - clientes_validos
        - clientes_invalidos
        - enderecos_validos
        - enderecos_invalidos
    """

    clientes_validos_list = []
    clientes_invalidos_list = []

    for _, row in df_clientes.iterrows():
        row_dict = row.to_dict()
        is_valid, erros = validar_clientes_row(row_dict)
        row_dict["erros"] = erros

        if is_valid:
            clientes_validos_list.append(row_dict)
        else:
            clientes_invalidos_list.append(row_dict)


    clientes_ids_validos = {row["id_cliente"] for row in clientes_validos_list}


    enderecos_validos_list = []
    enderecos_invalidos_list = []

    for _, row in df_enderecos.iterrows():
        row_dict = row.to_dict()
        is_valid, erros = validar_endereco_row(row_dict, clientes_ids_validos)
        row_dict["erros"] = erros

        if is_valid:
            enderecos_validos_list.append(row_dict)
        else:
            enderecos_invalidos_list.append(row_dict)

    # ----------------------------

    return {
        "clientes_validos": pd.DataFrame(clientes_validos_list),
        "clientes_invalidos": pd.DataFrame(clientes_invalidos_list),
        "enderecos_validos": pd.DataFrame(enderecos_validos_list),
        "enderecos_invalidos": pd.DataFrame(enderecos_invalidos_list),
    }