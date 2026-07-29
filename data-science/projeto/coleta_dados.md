# Coleta de Dados

## Planejamento de Governança e Modelo de Dados

A coleta de dados constitui uma fase fundamental para o sucesso de projetos de banco de dados e machine learning. Nesta etapa, foram definidas estratégias para extração, armazenamento e gerenciamento dos dados utilizados no projeto.

A coleta será realizada a partir da base disponível no Kaggle, mas com decisões estratégicas sobre infraestrutura, pipeline de dados e governança, simulando um ambiente corporativo real.

### Estratégia de Governança de Dados

Foi elaborada uma estratégia de governança que define requisitos, procedimentos, funções e responsabilidades para todo o ciclo de vida dos dados.
Essa estrutura de gerenciamento estabelece controles de qualidade, segurança e rastreabilidade desde a coleta até a disponibilização final.

O planejamento contempla:

Definição de papéis e responsabilidades

Políticas de acesso e uso dos dados

Procedimentos de backup e recuperação

Mecanismos de auditoria e monitoramento contínuo

### Modelo de Dados e Armazenamento

Os dados serão armazenados no formato Parquet, por duas razões principais:

Baixo custo de consumo — estrutura colunar otimiza o armazenamento e reduz custos de consulta em nuvem.

Alta performance — leitura rápida e eficiente, ideal para processamento paralelo.

Após o processo de ETL, os dados estarão limpos e estruturados, prontos para consumo pelos modelos de machine learning.

### Infraestrutura e Pipeline de Dados

A infraestrutura será implementada na Amazon Web Services (AWS), utilizando serviços especializados para construir um pipeline robusto e escalável.
A arquitetura foi projetada considerando performance, custo e facilidade de manutenção, seguindo boas práticas de engenharia de dados.

### Arquitetura de Armazenamento e Processamento

AWS S3: armazenamento dos arquivos em formato Parquet, garantindo durabilidade e escalabilidade.

AWS Glue: desenvolvimento do pipeline ETL (extração, transformação e carga), totalmente gerenciado.

AWS Athena: consultas SQL diretamente sobre os dados armazenados, sem necessidade de infraestrutura adicional.

### Infraestrutura como Código e Controle de Versão

Para garantir replicabilidade e padronização, a infraestrutura será criada utilizando o conceito de Infraestrutura como Código (IaC).
Os scripts estarão disponíveis no repositório Git, permitindo que qualquer membro da equipe replique o ambiente em sua própria conta AWS.

Todo o código-fonte do pipeline de ETL e os scripts IaC serão versionados via Git, utilizando forks para desenvolvimento e pull requests para integração.

### Controle e Rastreabilidade

O projeto implementa um sistema completo de controle e rastreabilidade, assegurando a qualidade e governança de dados e processos.
A documentação será mantida no repositório Git, descrevendo os procedimentos para replicação da infraestrutura e execução do pipeline de dados.

### Sistema de Monitoramento

Foi implementado um sistema de TAGs, simulando identificadores de tarefas semelhantes aos utilizados em ferramentas como JIRA, para:

Controle granular de desenvolvimento

Integração Contínua e Entrega Contínua (CI/CD)

Rastreamento de alterações e execuções do pipeline

 ### Documentação e Repositório

A documentação técnica abrange desde a configuração inicial da infraestrutura até os procedimentos operacionais do pipeline de dados.

📂 Repositório GitHub: Tecnologia-em-Banco-de-Dados-PUC-Minas/eixo5_grupo3_20252

📈 Status do Projeto: Etapas 1 e 2 concluídas
🧩 Próxima Etapa (3): Pré-processamento de dados
Inclui:

Limpeza, transformação e junção dos dados

Registro das ações realizadas

Compartilhamento dos dados pré-processados

Atualização do modelo de dados (se necessário)

Este documento será continuamente atualizado conforme o progresso das próximas etapas do projeto.

### Referências

CNDL & SPC Brasil. Indicadores de inadimplência no Brasil. 2024. https://www.cndl.org.br

Kaggle. Credit Risk Dataset. https://www.kaggle.com/datasets/laotse/credit-risk-dataset

IBM. Machine Learning: conceito e aplicação prática. IBM Knowledge Center, 2024.

AWS Documentation. S3, Glue e Athena. https://aws.amazon.com/documentation/

Brasil. Lei nº 13.709/2018 (LGPD).

Gartner. Best Practices in Data Governance. Gartner Research Report, 2024.
