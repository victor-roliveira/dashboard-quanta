import streamlit as st
import pandas as pd

# Carrega a planilha
df = pd.read_excel("ProjectEmExcel_MKE.xlsx", sheet_name="Planilha1")

# Trata e ordena pela hierarquia
df["Número Hierárquico"] = df["Número Hierárquico"].astype(str)

def sort_key(value):
    return [int(part) for part in value.split('.') if part.isdigit()]
df = df.sort_values(by="Número Hierárquico", key=lambda col: col.map(sort_key))

# Trata valores nulos em % Concluída
df["% Concluída"] = pd.to_numeric(df["% Concluída"], errors="coerce").fillna(0)

# Título
st.title("Acompanhamento Geral Macaé")
st.markdown("Explore o andamento das tarefas do contrato SEMED")

# Função recursiva modificada
def render_hierarchical_items(parent_num, df, level=0):
    # Filtra apenas os filhos diretos (próximo nível)
    children = df[df["Número Hierárquico"].str.fullmatch(f"{parent_num}\\.\\d+$")]
    
    for _, row in children.iterrows():
        current_num = row["Número Hierárquico"]
        nome = row["Nome da Tarefa"]
        concluido = round(row["% Concluída"] * 100)
        
        # Verifica se este item tem filhos (qualquer nível abaixo)
        has_children = df["Número Hierárquico"].str.startswith(f"{current_num}.").any()
        
        if has_children:
            with st.expander(f"{'&nbsp;' * 4 * level}👉 {current_num} - {nome} — {concluido}%", expanded=False):
                # Renderiza apenas os filhos deste nível
                render_hierarchical_items(current_num, df, level + 1)
        else:
            indent = "&nbsp;" * 4 * level
            st.markdown(f"{indent}🔹 {current_num} - {nome} ({concluido}%)", unsafe_allow_html=True)

# Itens de nível mais alto (que não têm ".")
top_level_items = df[df["Número Hierárquico"].str.fullmatch(r'^\d+$')]

# Renderiza a hierarquia começando pelos itens de nível mais alto
for _, row in top_level_items.iterrows():
    current_num = row["Número Hierárquico"]
    nome = row["Nome da Tarefa"]
    concluido = round(row["% Concluída"] * 100)
    
    has_children = df["Número Hierárquico"].str.startswith(f"{current_num}.").any()
    
    if has_children:
        with st.expander(f"👉 {current_num} - {nome} — {concluido}%", expanded=False):
            render_hierarchical_items(current_num, df, 1)
    else:
        st.markdown(f"🔹 {current_num} - {nome} ({concluido}%)")