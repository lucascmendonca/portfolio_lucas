import os
import pandas as pd
from dotenv import load_dotenv

from data_pipeline.scripts.extract import extracao_excel_github
from data_pipeline.tools.entity_validators import validar_entidades
from data_pipeline.scripts.raw_writer import salvar_raw
from data_pipeline.configs.config import *



# Função principal do pipeline RAW

def executar_pipeline_raw(env="local", output_dir="./local_output"):
    print("Iniciando pipeline RAW...")

    # Garantir que diretorio de saída existe
    os.makedirs(output_dir, exist_ok=True)

    # Carregar variáveis de ambiente (.env)
    load_dotenv()
    BUCKET_NAME = os.getenv("S3_BUCKET_NAME", None)

    
    # Extrair dados do GitHub
    
    print("Extraindo dados do arquivo Excel no GitHub...")
    dados = extracao_excel_github(GITHUB_EXCEL_URL)

    if dados is None or not isinstance(dados, dict):
        raise ValueError("Erro ao extrair dados do GitHub")

    df_clientes = pd.DataFrame(dados.get("clientes", []))
    df_enderecos = pd.DataFrame(dados.get("enderecos", []))

    print(f"Clientes carregados: {len(df_clientes)}")
    print(f"Endereços carregados: {len(df_enderecos)}")

    
    # Validações
    
    print("Executando validação completa dos dados...")

    resultado = validar_entidades(df_clientes, df_enderecos)

    df_cli_validos = resultado["clientes_validos"]
    df_cli_invalidos = resultado["clientes_invalidos"]
    df_end_validos = resultado["enderecos_validos"]
    df_end_invalidos = resultado["enderecos_invalidos"]

    print(f"Clientes válidos: {len(df_cli_validos)}")
    print(f"Clientes inválidos: {len(df_cli_invalidos)}")
    print(f"Endereços válidos: {len(df_end_validos)}")
    print(f"Endereços inválidos: {len(df_end_invalidos)}")

    
    # Salvar RAW
    
    print("Salvando arquivos no RAW...")

    # Clientes válidos
    salvar_raw(
        df=df_cli_validos,
        nome_dataset="clientes",
        valido=True,
        environment=env,
        bucket=str(BUCKET_NAME),
        output_dir=output_dir,
    )

    # Clientes inválidos
    if len(df_cli_invalidos) > 0:
        salvar_raw(
            df=df_cli_invalidos,
            nome_dataset="clientes",
            valido=False,
            environment=env,
            bucket=str(BUCKET_NAME),
            output_dir=output_dir,
        )

    # Endereços válidos
    salvar_raw(
        df=df_end_validos,
        nome_dataset="enderecos",
        valido=True,
        environment=env,
        bucket=str(BUCKET_NAME),
        output_dir=output_dir,
    )

    # Endereços inválidos
    if len(df_end_invalidos) > 0:
        salvar_raw(
            df=df_end_invalidos,
            nome_dataset="enderecos",
            valido=False,
            environment=env,
            bucket=str(BUCKET_NAME),
            output_dir=output_dir,
        )

    print("Pipeline RAW finalizado com sucesso.")


# Execução direta
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Executa o pipeline RAW.")
    parser.add_argument("--env", type=str, default="local", help="Ambiente de execucao: local ou aws.")
    parser.add_argument("--output-dir", type=str, default="./local_output", help="Diretorio de saída.")
    args = parser.parse_args()

    executar_pipeline_raw(env=args.env, output_dir=args.output_dir)