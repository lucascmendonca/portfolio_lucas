import pandas as pd
import pytest

from data_pipeline.tools.entity_validators import validar_entidades

@pytest.fixture
def df_clientes_validos():
    return pd.DataFrame([
        {
            "id_cliente": 1,
            "nome": "Lucas",
            "cpf": "123.456.789-09",
            "email": "lucas@example.com",
            "data_nascimento": "1990-05-01",
            "status": "ativo"
        }
    ])


@pytest.fixture
def df_clientes_invalidos():
    return pd.DataFrame([
        {
            "id_cliente": None,
            "nome": "",
            "cpf": "00000000000",
            "email": "email-invalido",
            "data_nascimento": "31-31-2999",
            "status": "banana"
        }
    ])


@pytest.fixture
def df_enderecos_validos():
    return pd.DataFrame([
        {
            "id_endereco": 10,
            "id_cliente": 1,
            "cep": "12345-678",
            "cidade": "São Paulo",
            "estado": "SP"
        }
    ])


@pytest.fixture
def df_enderecos_invalidos():
    return pd.DataFrame([
        {
            "id_endereco": 11,
            "id_cliente": 999,  # FK inválida
            "cep": "ABCDE",
            "cidade": "",
            "estado": None
        }
    ])

# TESTES

def test_validacao_clientes_validos(df_clientes_validos, df_enderecos_validos):
    result = validar_entidades(df_clientes_validos, df_enderecos_validos)

    assert len(result["clientes_validos"]) == 1
    assert len(result["clientes_invalidos"]) == 0


def test_validacao_clientes_invalidos(df_clientes_invalidos, df_enderecos_validos):
    result = validar_entidades(df_clientes_invalidos, df_enderecos_validos)

    assert len(result["clientes_validos"]) == 0
    assert len(result["clientes_invalidos"]) == 1
    assert "erros" in result["clientes_invalidos"].columns


def test_validacao_enderecos_validos(df_clientes_validos, df_enderecos_validos):
    result = validar_entidades(df_clientes_validos, df_enderecos_validos)

    assert len(result["enderecos_validos"]) == 1
    assert len(result["enderecos_invalidos"]) == 0


def test_validacao_enderecos_invalidos(df_clientes_validos, df_enderecos_invalidos):
    result = validar_entidades(df_clientes_validos, df_enderecos_invalidos)

    assert len(result["enderecos_validos"]) == 0
    assert len(result["enderecos_invalidos"]) == 1
    assert "erros" in result["enderecos_invalidos"].columns


def test_integridade_referencial(df_clientes_validos, df_enderecos_invalidos):
    """Endereço não pode ter id_cliente inexistente."""
    result = validar_entidades(df_clientes_validos, df_enderecos_invalidos)

    erros = result["enderecos_invalidos"].iloc[0]["erros"]
    assert any("não existe" in e for e in erros)


def test_retorno_formato_final(df_clientes_validos, df_enderecos_validos):
    """Testa se a função retorna exatamente os 4 DataFrames."""
    result = validar_entidades(df_clientes_validos, df_enderecos_validos)

    expected_keys = {
        "clientes_validos",
        "clientes_invalidos",
        "enderecos_validos",
        "enderecos_invalidos"
    }

    assert expected_keys == set(result.keys())
