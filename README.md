# SeletorDLTSaude

## Descrição
O SeletorDLTSaude é uma aplicação interativa desenvolvida para auxiliar profissionais e pesquisadores na escolha da melhor solução de Distributed Ledger Technology (DLT) e algoritmo de consenso para projetos de saúde.

## Funcionalidades
- Seleção guiada de DLT baseada em requisitos específicos
- Visualização interativa do processo de decisão
- Comparação detalhada entre diferentes DLTs
- Sistema de recomendação baseado em características priorizadas
- Armazenamento de recomendações por usuário
- Visualização de métricas técnicas

## Tecnologias Utilizadas
- Streamlit
- SQLite
- Plotly
- Pandas
- BCrypt

## Instalação
1. Clone o repositório
2. Instale as dependências: pip install -r requirements.txt
3. Execute a aplicação: streamlit run main.py --server.port 5000

## Estrutura do Projeto
- main.py: Arquivo principal da aplicação
- decision_tree.py: Lógica da árvore de decisão
- decision_logic.py: Lógica de recomendação
- dlt_data.py: Dados sobre DLTs e algoritmos
- database.py: Gerenciamento do banco de dados
- metrics.py: Cálculo de métricas técnicas
- utils.py: Funções utilitárias
- user_management.py: Gerenciamento de usuários

## Referências
Baseado em pesquisas acadêmicas recentes (2024-2025) sobre DLTs na área da saúde.
