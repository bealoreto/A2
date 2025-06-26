### Código não oficial (começamos o trabalho aqui mas o código está no prog.py)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta


banco_ideias = {
    'moda': {
        'instagram': ['Look do dia', 'Reels de transição de roupa', 'Carrossel de tendências'],
        'tiktok': ['Desafio de estilo', 'Transformação visual', 'Dicas de moda com voz'],
        'linkedin': ['Moda no mercado corporativo', 'Dicas de imagem pessoal', 'História da sua marca de moda']
    },
    'culinária': {
        'instagram': ['Receita rápida nos Stories', 'Reels de preparo', 'Carrossel de dicas de ingredientes'],
        'tiktok': ['Receita ASMR', 'Cozinhando com humor', 'Desafio de 5 ingredientes'],
        'linkedin': ['Empreendedorismo gastronômico', 'História da sua marca', 'Tendências alimentares']
    }
}

def gerar_cronograma(nicho, plataformas, dias=7):
    hoje = datetime.today()
    cronograma = [1,7]

    for i in range(dias):
        data = hoje + timedelta(days=i)
        dia = data.strftime('%d/%m/%Y')

        for plataforma in plataformas:
            ideias = banco_ideias.get(nicho, {}).get(plataforma, [])
            if ideias:
                ideia = ideias[i % len(ideias)]  # alterna as ideias
                cronograma.append({
                    'Data': dia,
                    'Plataforma': plataforma.capitalize(),
                    'Ideia de Conteúdo': ideia
                })

    return pd.DataFrame(cronograma)

st.write("Escolha o nicho")
nicho = st.text_input(' (ex: moda, culinária): ').strip().lower()
st.write("Escolha as plataformas separadas por vírgula (instagram, tiktok, linkedin):")
plataformas = st.text_input(' (instagram, tiktok, linkedin): ')
if plataformas:
    plataformas=[p.strip().lower() for p in plataformas.split(',')]
    df_cronograma = gerar_cronograma(nicho, plataformas, dias=7)
    st.write("\n🔹 Cronograma de Conteúdo (7 dias):")
    st.write(df_cronograma)
