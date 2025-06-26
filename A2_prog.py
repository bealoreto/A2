import streamlit as st
import pandas as pd
import datetime
import random
import os
from dotenv import load_dotenv
from pyngrok import ngrok

load_dotenv()  

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

import google.generativeai as genai

def get_content_ideas(niche, objective, num_ideas, creativity=0.8):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Você é um especialista em marketing digital. Gere {num_ideas} ideias de conteúdo
    criativas para o nicho de {niche} com foco em {objective}.
  
    As ideias devem ser:
    - Diversificadas (variedade de formatos e abordagens)
    - Aplicáveis às principais redes sociais
    - Alinhadas com as últimas tendências
    - Com potencial de engajamento
  
    Retorne APENAS as ideias, uma por linha, sem numeração ou formatação adicional.
    """
  
    try:
       response = model.generate_content(
              prompt,
              generation_config={"temperature": creativity, "max_output_tokens": 2000}
          )
      
          ideas = response.text.strip().split('\n')
          return [idea for idea in ideas if idea.strip()]

    except Exception as e:
        print(f"Erro na geração de conteúdo: {e}")
        return [
            f"Conteúdo sobre {niche} para {objective}",
            f"Tutorial relacionado a {niche}",
            f"Dicas de {niche} para iniciantes",
            f"Novas tendências em {niche}",
            f"Como melhorar seu desempenho em {niche}"
        ][:num_ideas]  
      
def generate_content_plan(start_date, weeks, frequency, platforms, ideas, include_hashtags=True, include_times=True):
    dates = []
    current_date = start_date
  
    for _ in range(weeks):
        for _ in range(frequency):
              day_offset = random.randint(0, 6)
              post_date = current_date + datetime.timedelta(days=day_offset)
              dates.append(post_date)
          current_date += datetime.timedelta(weeks=1)
    dates.sort()
    schedule = pd.DataFrame({
        "Data": dates,
        "Plataforma": [random.choice(platforms) for _ in dates],
        "Tópico": random.sample(ideas, len(dates)),
        "Formato": [random.choice(["Reels", "Story", "Post", "Video"]) for _ in dates]
    })

    if include_hashtags:
        niche_hashtags = {
            "Moda": ["Moda", "Estilo", "Tendências"],
            "Beleza": ["Beleza", "Maquiagem", "Skincare"],
            "Tecnologia": ["Tech", "Inovação", "Tecnologia"],
            "Gastronomia": ["Comida", "Receita", "Chef"],
            "Fitness": ["Fitness", "Treino", "Saúde"],
            "Educação": ["Educação", "Aprendizado", "Conhecimento"]
        }
      
        schedule["Hashtags"] = schedule["Plataforma"].apply(
            lambda p: "#" + p + " " + " ".join(["#" + h for h in niche_hashtags.get(niche, ["Conteúdo"])])
        )
      
    if include_times:
        best_times = {
            "Instagram": ["09:00", "12:00", "15:00", "18:00"],
            "TikTok": ["10:00", "14:00", "17:00", "21:00"],
            "LinkedIn": ["08:00", "12:00", "17:00"],
            "Twitter": ["08:00", "12:00", "16:00", "20:00"],
            "Facebook": ["09:00", "13:00", "19:00"]
        }
      
        schedule["Horário Sugerido"] = schedule.apply(
            lambda row: random.choice(best_times.get(row["Plataforma"], ["10:00"])),
            axis=1
        )

    return schedule

from fpdf import FPDF

def save_ideas(ideas):
    """Salva ideias em arquivo CSV"""
    df = pd.DataFrame(ideas, columns=["Ideia"])
    df.to_csv("content_ideas.csv", index=False)

def load_ideas():
    """Carrega ideias de arquivo CSV"""
    if os.path.exists("content_ideas.csv"):
        df = pd.read_csv("content_ideas.csv")
        return df["Ideia"].tolist()
    return None

def generate_pdf(schedule, niche, objective, start_date):
    """Gera PDF do cronograma"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Cronograma de Conteúdo - {niche}", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Objetivo: {objective}", 0, 1)
    pdf.cell(0, 10, f"Data de início: {start_date.strftime('%d/%m/%Y')}", 0, 1)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    col_widths = [30, 30, 60, 30, 40]
    headers = ["Data", "Plataforma", "Tópico", "Formato", "Horario"]
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1)
    pdf.ln()
    pdf.set_font("Arial", "", 10)
    for _, row in schedule.iterrows():
        pdf.cell(col_widths[0], 10, row["Data"].strftime("%d/%m"), 1)
        pdf.cell(col_widths[1], 10, row["Plataforma"], 1)
        pdf.cell(col_widths[2], 10, row["Tópico"], 1)
        pdf.cell(col_widths[3], 10, row["Formato"], 1)
        pdf.cell(col_widths[4], 10, row.get("Horário Sugerido", ""), 1)
        pdf.ln()

    return pdf.output(dest="S").encode("latin1")

def estimate_engagement(niche, platforms, frequency, weeks):
    """Estima engajamento com base em parâmetros"""
    base_reach = {
        "Moda": 10000,
        "Beleza": 8000,
        "Tecnologia": 6000,
        "Gastronomia": 7000,
        "Fitness": 5000,
        "Educação": 4000
    }

    platform_multiplier = {
        "Instagram": 1.2,
        "TikTok": 1.5,
        "LinkedIn": 0.8,
        "Twitter": 0.7,
        "Facebook": 1.0
    }
  
    base = base_reach.get(niche, 5000)
    platform_factor = sum(platform_multiplier[p] for p in platforms) / len(platforms)
    total_posts = frequency * weeks
    total_reach = base * platform_factor * total_posts
    engagement_rate = 0.05  # 5% de taxa de engajamento
    total_engagement = total_reach * engagement_rate
    follower_growth = total_reach * 0.01  # 1% de taxa de conversão

    return {
        "reach": int(total_reach),
        "engagement": int(total_engagement),
        "followers": int(follower_growth)
    }

def main():
    st.set_page_config(
        page_title="Social Content Planner",
        page_icon="📅",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📅 Social Content Planner - IA")
    st.markdown("""
    **Crie cronogramas de conteúdo perfeitos para suas redes sociais**
    Use inteligência artificial para planejar suas postagens e aumentar seu engajamento.
    """)

    with st.sidebar:
        st.header("⚙️ Configurações")

        niche = st.selectbox(
            "Seu nicho/área:",
            ["Moda", "Beleza", "Tecnologia", "Gastronomia", "Fitness", "Educação", "Outro"]
        )

        objective = st.selectbox(
            "Objetivo principal:",
            ["Aumentar engajamento", "Gerar vendas", "Construir marca", "Divulgar produto"]
        )

        platforms = st.multiselect(
            "Plataformas:",
            ["Instagram", "TikTok", "LinkedIn", "Twitter", "Facebook"],
            default=["Instagram", "TikTok"]
        )

        frequency = st.slider(
            "Postagens por semana:",
            1, 20, 7
        )

        start_date = st.date_input(
            "Data de início:",
            datetime.date.today()
        )
        weeks = st.slider("Semanas de planejamento:", 1, 12, 4)

        with st.expander("Configurações avançadas"):
            creativity = st.slider("Criatividade da IA:", 0.5, 1.0, 0.8)
            include_hashtags = st.checkbox("Incluir hashtags sugeridas", True)
            include_times = st.checkbox("Incluir melhores horários", True)

        generate_button = st.button("Gerar Cronograma", type="primary")

    st.sidebar.divider()
    with st.sidebar.expander("💡 Banco de Ideias"):
        if st.button("Carregar ideias salvas"):
            saved_ideas = load_ideas()
            if saved_ideas:
                st.session_state.ideas = saved_ideas
                st.success("Ideias carregadas com sucesso!")
            else:
                st.warning("Nenhum arquivo de ideias encontrado")

        if st.button("Salvar ideias atuais"):
            if 'ideas' in st.session_state:
                save_ideas(st.session_state.ideas)
                st.success("Ideias salvas com sucesso!")
            else:
                st.error("Nenhuma ideia para salvar")

    if generate_button:
        with st.spinner("Gerando cronograma com IA..."):
            content_ideas = get_content_ideas(
                niche,
                objective,
                frequency * weeks,
                creativity
            )

            schedule = generate_content_plan(
                start_date,
                weeks,
                frequency,
                platforms,
                content_ideas,
                include_hashtags,
                include_times
            )

            engagement = estimate_engagement(
                niche,
                platforms,
                frequency,
                weeks
            )

            st.session_state.schedule = schedule
            st.session_state.ideas = content_ideas
            st.session_state.engagement = engagement

    if 'schedule' in st.session_state:
        st.divider()
        st.header("📋 Cronograma Gerado")

        if 'engagement' in st.session_state:
            eng = st.session_state.engagement
            col1, col2, col3 = st.columns(3)
            col1.metric("Alcance Estimado", f"{eng['reach']:,}")
            col2.metric("Engajamento Esperado", f"{eng['engagement']:,}")
            col3.metric("Crescimento de Seguidores", f"+{eng['followers']:,}")
        st.dataframe(
            st.session_state.schedule,
            use_container_width=True,
            height=600
        )

        st.subheader("Visualização em Calendário")
        calendar_view = st.selectbox(
            "Tipo de visualização:",
            ["Mensal", "Semanal", "Diário"]
        )

        calendar_options = {
            "editable": False,
            "selectable": True,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": f"{calendar_view.lower()}Day,{calendar_view.lower()}Week,dayGridMonth"
            },
            "initialView": "dayGridMonth" if calendar_view == "Mensal" else "timeGridWeek",
        }

        events = []
        for _, row in st.session_state.schedule.iterrows():
            events.append({
                "title": row['Tópico'],
                "start": row['Data'].strftime("%Y-%m-%dT%H:%M:%S"),
                "end": row['Data'].strftime("%Y-%m-%dT%H:%M:%S"),
                "color": "#FF4B4B" if "Instagram" in row['Plataforma'] else "#1A73E8"
            })

        st.calendar(
            events=events,
            options=calendar_options,
            custom_css="""
                .fc-event {
                    cursor: pointer;
                    font-size: 0.8em;
                    padding: 2px 5px;
                }
            """
        )

        st.divider()
        st.subheader("📤 Exportar Cronograma")

        col1, col2 = st.columns(2)
        with col1:
            csv = st.session_state.schedule.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar como CSV",
                data=csv,
                file_name=f"cronograma_{niche}_{start_date}.csv",
                mime='text/csv'
            )

        with col2:
            if st.button("Gerar PDF"):
                pdf = generate_pdf(
                    st.session_state.schedule,
                    niche,
                    objective,
                    start_date
                )
                st.download_button(
                    label="Baixar PDF",
                    data=pdf,
                    file_name=f"cronograma_{niche}.pdf",
                    mime='application/pdf'
                )
        st.divider()
        st.subheader("💡 Banco de Ideias Geradas")
        st.write(f"Total de ideias: {len(st.session_state.ideas)}")
        st.dataframe(
            pd.DataFrame(st.session_state.ideas, columns=["Ideias de Conteúdo"]),
            use_container_width=True,
            height=300
        )

    elif generate_button:
        st.warning("Ocorreu um erro ao gerar o cronograma. Tente novamente.")

    else:
        st.divider()
        st.info("💡 Configure as opções na barra lateral e clique em 'Gerar Cronograma' para começar")
        st.image("https://via.placeholder.com/800x400?text=Exemplo+de+Sa%C3%ADda+do+Simulador", use_column_width=True)
      
if __name__ == "__main__":
    main()

print("Variáveis encontradas:")
print([k for k in os.environ if "NGROK" in k])
print("\nValor do NGROK_AUTH_TOKEN:")
print(os.environ.get("NGROK_AUTH_TOKEN"))

from getpass import getpass
os.environ["NGROK_AUTH_TOKEN"] = getpass("2z38ESxrYXjLLxo7FDOQmM1En4u_4S1veCicQy6shApYaDTgY: ")

NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTH_TOKEN")
if NGROK_AUTH_TOKEN:
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
else:
    print("NGROK_AUTH_TOKEN não encontrado. Defina-o manualmente antes desta célula.")
  
public_url = ngrok.connect(8501)
print(f"\n✅ Acesse o aplicativo em: {public_url}\n")

!streamlit run /content/app.py --server.port 8501 &>/dev/null &

