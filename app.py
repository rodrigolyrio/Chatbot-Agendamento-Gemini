# app.py
import streamlit as st
import gspread
import google.generativeai as genai
import os
import pandas as pd
from datetime import datetime, timedelta
import json
import re

# --- 1. CONFIGURAÇÃO DAS APIS ---

# Tenta carregar a chave da API do Gemini a partir das variáveis de ambiente
try:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        raise ValueError("A variável de ambiente GEMINI_API_KEY não foi configurada.")
    genai.configure(api_key=GEMINI_API_KEY)
except ValueError as e:
    st.error(f"Erro de configuração: {e}")
    st.stop() # Interrompe a execução do app se a chave não for encontrada

# Configura a API do Google Sheets
# O arquivo 'credentials.json' deve estar no mesmo diretório ou o caminho deve ser especificado.
try:
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("AgendaClínica")
    worksheet = sh.sheet1
except FileNotFoundError:
    st.error("Erro de configuração: O arquivo 'credentials.json' não foi encontrado.")
    st.info("Por favor, certifique-se de que o arquivo de credenciais do Google Cloud está no diretório correto.")
    st.stop()
except Exception as e:
    st.error(f"Ocorreu um erro ao conectar com o Google Sheets: {e}")
    st.stop()


# --- 2. FUNÇÕES DE LÓGICA DA AGENDA ---

def encontrar_horarios_disponiveis(dia_desejado, duracao_minutos=60):
    try:
        registros = worksheet.get_all_records()
        df = pd.DataFrame(registros)
        horarios_ocupados = []
        if not df.empty and 'data_inicio' in df.columns:
            df['data_inicio'] = pd.to_datetime(df['data_inicio'])
            df['data_fim'] = pd.to_datetime(df['data_fim'])
            for _, row in df.iterrows():
                horarios_ocupados.append((row['data_inicio'], row['data_fim']))
        inicio_dia = dia_desejado.replace(hour=9, minute=0, second=0)
        fim_dia = dia_desejado.replace(hour=18, minute=0, second=0)
        slot_atual = inicio_dia
        slots_disponiveis = []
        while slot_atual + timedelta(minutes=duracao_minutos) <= fim_dia:
            slot_fim = slot_atual + timedelta(minutes=duracao_minutos)
            ocupado = False
            for inicio_ocupado, fim_ocupado in horarios_ocupados:
                if (slot_atual < fim_ocupado) and (slot_fim > inicio_ocupado):
                    ocupado = True
                    break
            if not ocupado:
                slots_disponiveis.append(slot_atual)
            slot_atual += timedelta(minutes=duracao_minutos)
        return slots_disponiveis
    except Exception as e:
        st.error(f"Erro ao ler a agenda: {e}")
        return []

def agendar_consulta(nome, contato, motivo, data_inicio):
    """
    Adiciona uma nova linha na planilha com os dados do agendamento.
    """
    try:
        if isinstance(data_inicio, str):
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d %H:%M:%S')
        duracao_padrao = timedelta(minutes=60)
        data_fim = data_inicio + duracao_padrao
        nova_linha = [
            str(data_inicio), str(data_fim), nome, contato, motivo, str(datetime.now())
        ]
        worksheet.append_row(nova_linha, value_input_option='USER_ENTERED')
        return True
    except Exception as e:
        st.error(f"Erro ao salvar na agenda: {e}")
        return False

# --- 3. INTERFACE DO CHATBOT (STREAMLIT) ---

st.title("Agente de Agendamento Odontológico")

model = genai.GenerativeModel('gemini-1.5-pro-latest')

system_prompt_template = """
Você é 'Clara', uma assistente de agendamento para uma clínica odontológica.
A data de hoje é {data_atual}.

Sua função é:
1. Saudar o paciente e perguntar o motivo da visita.
2. Coletar o nome completo, o telefone e a preferência de dia/hora do paciente.
3. NUNCA ofereça conselhos médicos. Seja sempre empática, profissional e direta.

IMPORTANTE: Depois de coletar todas as informações, sua única e exclusiva resposta deve ser um JSON.
Baseado na data de hoje, converta pedidos como "amanhã" ou "segunda-feira" em uma data completa.
O formato do JSON deve ser:
{{"acao": "agendar", "nome": "NOME COMPLETO", "contato": "TELEFONE", "motivo": "MOTIVO", "data_desejada": "YYYY-MM-DD HH:MM:SS"}}
"""

# Inicializa o histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializa o chat do Gemini
if "chat" not in st.session_state:
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    system_prompt_preenchido = system_prompt_template.format(data_atual=data_hoje)
    
    st.session_state.chat = model.start_chat(history=[
        {'role': 'user', 'parts': [system_prompt_preenchido]},
        {'role': 'model', 'parts': ["Olá! Eu sou a Clara, sua assistente virtual. Como posso lhe ajudar hoje? Você gostaria de marcar uma limpeza, avaliação, ou tem uma emergência?"]}
    ])

# Exibe o histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Obtém a nova entrada do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.chat.send_message(prompt)
    
    # --- LÓGICA DE INTERPRETAÇÃO DA RESPOSTA ---
    resposta_ia = response.text
    final_response = ""

    try:
        match = re.search(r'\{.*\}', resposta_ia, re.DOTALL)
        if match:
            clean_json_str = match.group(0)
            dados_agendamento = json.loads(clean_json_str)
        else:
            raise json.JSONDecodeError("Nenhum JSON encontrado", resposta_ia, 0)

        if isinstance(dados_agendamento, dict) and dados_agendamento.get("acao") == "agendar":
            nome = dados_agendamento.get("nome")
            contato = dados_agendamento.get("contato")
            motivo = dados_agendamento.get("motivo")
            data_str = dados_agendamento.get("data_desejada")
            
            data_obj = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')

            sucesso = agendar_consulta(
                nome=nome, contato=contato, motivo=motivo, data_inicio=data_obj
            )

            if sucesso:
                data_formatada = data_obj.strftime("%d/%m/%Y às %H:%M")
                final_response = f"Agendamento efetuado com sucesso! Sua consulta de '{motivo}' para {nome} foi marcada para o dia {data_formatada}."
            else:
                final_response = "Peço desculpas, mas não consegui realizar o agendamento devido a um erro interno. Por favor, tente novamente."
        else:
            final_response = resposta_ia

    except (json.JSONDecodeError, TypeError):
        final_response = resposta_ia
    except Exception as e:
        final_response = "Desculpe, encontrei um problema ao processar sua solicitação. Poderia tentar novamente?"
        print(f"Ocorreu um erro inesperado: {e}") 
    
    st.session_state.messages.append({"role": "assistant", "content": final_response})
    with st.chat_message("assistant"):
        st.markdown(final_response)
