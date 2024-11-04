# HealthLedgerSelector

**HealthLedgerSelector** é um sistema de seleção de tecnologias de Ledger Distribuído (DLT) para projetos de saúde. Este aplicativo ajuda a avaliar e comparar diferentes frameworks de DLT com base em critérios específicos para atender às necessidades de segurança, interoperabilidade, governança e eficiência energética no setor de saúde.

## Funcionalidades

- **Tela de Login e Registro**: Sistema de autenticação para acesso seguro.
- **Comparação de Frameworks**: Exibe uma tabela comparativa dos principais frameworks de DLT aplicados na saúde, incluindo métricas de avaliação e critérios de seleção.
- **Análise Metodológica**: Estrutura hierárquica de classificação das DLTs, com foco em segurança, escalabilidade, eficiência e governança.
- **Sistema de Visualização**: Gráficos interativos que ajudam a visualizar e comparar os frameworks com base nas métricas específicas.
- **Download de Dados**: Opção para baixar dados comparativos em formato CSV.
- **Recomendações Personalizadas**: Baseado nas respostas do usuário, o sistema sugere o framework DLT mais adequado.

## Instalação

### 1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/HealthLedgerSelector.git
   cd HealthLedgerSelector
      ```

### 2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash

python3 -m venv venv
source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   ```
### 3. Instale as dependências:
   ```bash
pip install -r requirements.txt
   ```
4. Uso

Execute a aplicação:
   ```bash

streamlit run main.py
Acesse a aplicação no seu navegador em http://localhost:8501.
Registre-se ou faça login para acessar a plataforma.
Navegue pelo menu lateral para acessar as seguintes funcionalidades:
Início: Página de boas-vindas e introdução ao HealthLedgerSelector.
Framework Proposto: Visualize e utilize o sistema de decisão baseado em árvore para recomendações personalizadas.
Métricas: Visualize e entenda as métricas de avaliação, como Índice de Gini e Entropia.
Comparações: Tabela e gráficos comparativos para todos os frameworks de DLT disponíveis.
Perfil: Acesse as recomendações salvas e o histórico de uso.
Estrutura do Projeto

main.py: Arquivo principal que inicializa a aplicação e configura o fluxo de navegação.
user_management.py: Gerenciamento de autenticação e controle de sessão.
decision_tree.py: Lógica de decisão que recomenda frameworks de DLT com base nos critérios especificados.
database.py: Interações com o banco de dados para salvar e recuperar dados do usuário.
metrics.py: Cálculos das métricas de avaliação, como Gini, Entropia e Profundidade Decisória.
utils.py: Funções auxiliares para inicialização do estado da sessão e outras utilidades.
requirements.txt: Lista de dependências do projeto.
Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues para sugestões ou relatar problemas. Se desejar contribuir com código, faça um fork do repositório e envie um pull request com suas alterações.

### Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

perl


### Instruções para Usar

1. Salve o conteúdo acima em um arquivo chamado `README.md` no diretório raiz do seu projeto.
2. O `README.md` fornece uma visão geral para outros desenvolvedores ou usuários que desejem saber mais sobre o projeto, como instalá-lo e usá-lo.

Este arquivo `README.md` serve como uma documentação básica, e você pode expandi-lo conforme adiciona novas funcionalidades ou mudanças ao seu projeto.
