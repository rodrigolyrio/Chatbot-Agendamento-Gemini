# Agente de Agendamento com Gemini e Streamlit

Chatbot inteligente projetado para automatizar o agendamento de consultas para uma clínica odontológica fictícia. Construído com a API do Google Gemini para processamento de linguagem natural e Streamlit para a interface web, o agente conversa com os pacientes para coletar as informações necessárias e registra os agendamentos diretamente em uma planilha do Google Sheets.

## Funcionalidades

-   **Interface de Chat Interativa**: Uma interface web amigável criada com Streamlit para facilitar a comunicação com o paciente.
-   **Processamento de Linguagem Natural**: Utiliza o poder do Google Gemini para entender as solicitações dos usuários, como datas ("amanhã", "próxima segunda"), motivos da consulta e dados pessoais.
-   **Coleta Automatizada de Dados**: O chatbot é instruído a coletar nome, contato e motivo da consulta de forma estruturada.
-   **Integração com Google Sheets**: Salva os detalhes do agendamento em tempo real em uma planilha, funcionando como um sistema de agenda simples e eficaz.
-   **Verificação de Disponibilidade**: O sistema consulta a planilha para encontrar e sugerir horários disponíveis, evitando conflitos de agendamento.

## Pré-requisitos

Antes de começar, você precisará ter:
-   Python 3.8 ou superior.
-   Uma conta no Google Cloud Platform com:
    -   A **API do Google Sheets** ativada.
    -   A **Generative Language API** (API do Gemini) ativada.
-   Uma Planilha Google para ser usada como banco de dados da agenda.

## Configuração do Ambiente

Siga estes passos para configurar e executar o projeto em sua máquina local.

### 1. Clonar o Repositório

Primeiro, clone este repositório para a sua máquina local:
```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd <NOME_DA_PASTA_DO_PROJETO>
```

### 2. Criar um Ambiente Virtual e Instalar Dependências

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instale as bibliotecas a partir do arquivo requirements.txt
pip install -r requirements.txt
```

### 3. Configuração de Credenciais

Este projeto necessita de duas chaves de acesso que **NÃO** devem ser enviadas para o GitHub.

#### a) Credenciais do Google Sheets (`credentials.json`)

1.  Acesse o [Console do Google Cloud](https://console.cloud.google.com/).
2.  Crie um novo projeto ou selecione um existente.
3.  No menu de navegação, vá para "APIs e Serviços" > "Credenciais".
4.  Clique em "Criar Credenciais" e selecione "Conta de Serviço".
5.  Preencha os detalhes, conceda a ela o papel de **Editor** e clique em "Concluir".
6.  De volta à tela de credenciais, clique na conta de serviço que você acabou de criar.
7.  Vá para a aba "CHAVES", clique em "ADICIONAR CHAVE" > "Criar nova chave".
8.  Selecione **JSON** como o tipo de chave e clique em "Criar". O download do arquivo começará automaticamente.
9.  **Renomeie o arquivo baixado para `credentials.json`** e coloque-o na pasta raiz do seu projeto.
10. Abra sua Planilha Google, clique em "Compartilhar" e adicione o email da conta de serviço (encontrado no arquivo `credentials.json` no campo `client_email`) como um **Editor**.

O arquivo `credentials.json` já está incluído no `.gitignore` para garantir que ele não seja enviado ao seu repositório.

#### b) Chave da API do Google Gemini

1.  Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey) para gerar sua chave de API.
2.  Clique em "Create API key".
3.  Copie a chave gerada.
4.  Você precisa configurar esta chave como uma **variável de ambiente** para que o código possa acessá-la de forma segura.

    -   **No Windows (no terminal atual):**
        ```powershell
        $env:GEMINI_API_KEY="SUA_CHAVE_API_AQUI"
        ```
    -   **No macOS/Linux (no terminal atual):**
        ```bash
        export GEMINI_API_KEY="SUA_CHAVE_API_AQUI"
        ```
    **Atenção**: Para tornar essa variável permanente, você deve adicioná-la às configurações de variáveis de ambiente do seu sistema operacional.

### 4. Executando a Aplicação

Com o ambiente virtual ativado e as credenciais configuradas, inicie a aplicação Streamlit com o seguinte comando:

```bash
streamlit run app.py
```

Abra seu navegador e acesse `http://localhost:8501` para interagir com o seu agente de agendamento.
