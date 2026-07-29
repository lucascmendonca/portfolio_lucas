import pytest
from data_pipeline.tools.atomic_validators import (
    validar_cpf,
    validar_cep,
    validar_email,
    validar_data,
    validar_status,
)

# TESTE CPF

def test_validar_cpf():
    assert validar_cpf("123.456.789-10") is True
    assert validar_cpf("000.000.000-00") is True
    assert validar_cpf("12345678910") is False
    assert validar_cpf("123.456.78910") is False
    assert validar_cpf("") is False

# TESTE CEP

def test_validar_cep():
    assert validar_cep("12345-678") is True
    assert validar_cep("00000-000") is True
    assert validar_cep("12345678") is False
    assert validar_cep("1234-567") is False
    assert validar_cep("") is False

# TESTE EMAIL

def test_validar_email():
    assert validar_email("teste@example.com") is True
    assert validar_email("lucas.cardoso@empresa.com.br") is True
    assert validar_email("email@dominio") is False
    assert validar_email("@gmail.com") is False
    assert validar_email("teste@@gmail.com") is False
    assert validar_email("") is False

# TESTE DATA

def test_validar_data():
    assert validar_data("2024-02-28") is True
    assert validar_data("1990-12-01") is True
    assert validar_data("2024-13-01") is False
    assert validar_data("2024-02-30") is False
    assert validar_data("2024/02/28") is False
    assert validar_data("") is False

# TESTE STATUS

def test_validar_status():
    assert validar_status("ativo") is True
    assert validar_status("inativo") is True
    assert validar_status("suspenso") is True

    # Testes com variação de formato
    assert validar_status(" Ativo ") is True
    assert validar_status("INATIVO") is True

    # Valores inválidos
    assert validar_status("pendente") is False
    assert validar_status("bloqueado") is False
    assert validar_status("") is False
