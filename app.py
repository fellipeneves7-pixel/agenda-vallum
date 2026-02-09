import streamlit as st
import gspread
import google.generativeai as genai
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json

# --- CONFIGURAÇÃO DO SITE ---
st.set_page_config(page_title="Vallum Financeiro", page_icon="🏥")
st.title("🏥 Vallum System")

# --- PEGAR SEGREDOS (Para o 4G funcionar) ---
# Aqui o sistema vai ler a chave que vamos esconder no site do Streamlit
try:
    CHAVE_GEMINI = st.secrets["CHAVE_GEMINI"]
    creds_dict = dict(st.secrets["google_sheets"])
    
    # Conecta no Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    planilha = client.open("Banco de Dados Vallum").sheet1
    
    # Configura o Gemini
    genai.configure(api_key=CHAVE_GEMINI)
    modelo = genai.GenerativeModel('gemini-flash-latest')
    conexao_ok = True
except Exception as e:
    st.error("Aguardando configuração das chaves de segurança...")
    conexao_ok = False

# --- FUNÇÃO DA IA ---
def processar_ia(texto):
    hoje = datetime.now().strftime("%d/%m/%Y")
    prompt = f"Converta em JSON: {texto}. Hoje: {hoje}. Formato: {{\"Data\":\"{hoje}\",\"Paciente\":\"Nome\",\"Serviço\":\"Serviço\",\"Valor\":\"0,00\",\"Pagamento\":\"Pix/Dinheiro\"}}"
    resposta = modelo.generate_content(prompt)
    limpo = resposta.text.replace("```json", "").replace("```", "").strip()
    return json.loads(limpo)

# --- INTERFACE ---
with st.form("lancamento"):
    texto = st.text_area("Descreva o atendimento:")
    enviar = st.form_submit_button("🚀 Lançar")

if enviar and conexao_ok:
    with st.spinner('Processando...'):
        dados = processar_ia(texto)
        linha = [dados['Data'], dados['Paciente'], dados['Serviço'], dados['Valor'], dados['Pagamento']]
        planilha.append_row(linha)
        st.success(f"✅ Salvo: {dados['Paciente']} - R$ {dados['Valor']}")