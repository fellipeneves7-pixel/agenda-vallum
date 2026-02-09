import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Vallum - Agenda", page_icon="📅", layout="wide")
ARQUIVO_HISTORICO = "historico_vallum.csv"

# --- FUNÇÕES DE "MEMÓRIA" (Banco de Dados) ---
def carregar_dados():
    if not os.path.exists(ARQUIVO_HISTORICO):
        return pd.DataFrame(columns=["Data", "Paciente", "Serviço", "Local", "Valor"])
    return pd.read_csv(ARQUIVO_HISTORICO)

def salvar_agendamento(nova_linha):
    df = carregar_dados()
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_csv(ARQUIVO_HISTORICO, index=False)
    return df

# --- BARRA LATERAL (Configuração) ---
with st.sidebar:
    st.header("⚙️ Configuração")
    st.info("💡 As mudanças de preço aqui são apenas para o SEU uso atual.")
    p_fisio = st.number_input("Fisioterapia", value=120.0)
    p_ergo = st.number_input("Ergonomia", value=250.0)
    t_olaria = st.number_input("Taxa Olaria", value=15.0)
    # (Adicionei apenas alguns para exemplo rápido)

# --- ÁREA PRINCIPAL ---
st.title("📅 Sistema Vallum Integrado")

col1, col2 = st.columns(2)
with col1:
    nome = st.text_input("Paciente")
    servico = st.selectbox("Serviço", ["Fisioterapia", "Ergonomia"])
with col2:
    local = st.selectbox("Local", ["Centro", "Olaria"])
    
# Cálculo Simples (Para teste)
valor = p_fisio if servico == "Fisioterapia" else p_ergo
if local == "Olaria": valor += t_olaria

st.metric("Valor Total", f"R$ {valor:.2f}")

# BOTÃO DE SALVAR (A Mágica)
if st.button("💾 Salvar no Histórico", type="primary"):
    if nome:
        novo_dado = {
            "Data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Paciente": nome,
            "Serviço": servico,
            "Local": local,
            "Valor": f"R$ {valor:.2f}"
        }
        salvar_agendamento(novo_dado)
        st.success("Agendamento Salvo com Sucesso!")
        st.rerun() # Atualiza a tela

st.divider()
st.subheader("📂 Histórico de Agendamentos (Sincronizado)")
# Mostra a tabela que todos veem
df_historico = carregar_dados()
st.dataframe(df_historico, use_container_width=True)

