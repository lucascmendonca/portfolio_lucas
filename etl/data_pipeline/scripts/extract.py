import requests
import pandas as pd
from io import BytesIO
from loguru import logger
from data_pipeline.configs.config import GITHUB_EXCEL_URL


def extracao_excel_github(url: str = GITHUB_EXCEL_URL) -> dict:
    logger.info("Iniciando extração do Excel do GitHub")

    response = requests.get(url)
    response.raise_for_status()
    excel_bytes = BytesIO(response.content)

    dfs = {
            "clientes": pd.read_excel(excel_bytes, sheet_name="clientes", dtype=str),
            "enderecos": pd.read_excel(excel_bytes, sheet_name="enderecos", dtype=str)
        }

    logger.info("Extração concluída com sucesso")

    return dfs