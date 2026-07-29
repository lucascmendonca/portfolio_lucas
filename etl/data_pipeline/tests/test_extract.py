import pandas as pd
from data_pipeline.scripts.extract import extracao_excel_github
from data_pipeline.configs.config import GITHUB_EXCEL_URL

def test_extracao_excel_github():
    # Executa a extração
    dfs = extracao_excel_github(url=GITHUB_EXCEL_URL)

    # Verifica se retornou um dict
    assert isinstance(dfs, dict), "A função deve retornar um dicionário."

    # Verifica se contém as chaves esperadas
    assert "clientes" in dfs, "Dicionário deve conter 'clientes'."
    assert "enderecos" in dfs, "Dicionário deve conter 'enderecos'."

    # Verifica se são DataFrames
    assert isinstance(dfs["clientes"], pd.DataFrame), "'clientes' deve ser DataFrame."
    assert isinstance(dfs["enderecos"], pd.DataFrame), "'enderecos' deve ser DataFrame."

    # Verifica se não estão vazios
    assert not dfs["clientes"].empty, "DataFrame 'clientes' não pode estar vazio."
    assert not dfs["enderecos"].empty, "DataFrame 'enderecos' não pode estar vazio."
