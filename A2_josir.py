### Código não oficial (começamos o trabalho aqui mas o código está no prog.py)
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta


banco_ideias = {
    'moda': {
        'instagram': [
            'Look do dia com tags de marcas',
            'Tutorial: 3 formas de usar uma peça',
            'Desafio de 5 dias de looks criativos',
            'Unboxing de recebidos',
            'Enquete: “Qual look você usaria?”',
            'Dica de combinação de cores',
            'Bastidores de um ensaio fashion'
        ],
        'tiktok': [
            'Transformação de look com transição',
            'Expectativa vs Realidade de compras',
            'Dicas de styling com humor',
            'Top 3 tendências do mês',
            'Moda acessível em brechós',
            'Como montar um armário cápsula',
            'Reagindo a looks de famosos'
        ],
        'linkedin': [
            'A evolução do mercado fashion no digital',
            'Como influenciadores impactam a indústria',
            'Case de parceria com marca de moda',
            'Bastidores de uma campanha de moda',
            'Análise de tendências e impacto no varejo',
            'Dicas para empreender com moda',
            'Moda e ESG: como integrar propósito'
        ]
    },
    'culinária': {
        'instagram': [
            'Receita rápida em 30 segundos',
            'Dica de substituição saudável',
            'Mostre seu prato favorito da infância',
            'Desafio de receita com 3 ingredientes',
            'Tour pela despensa/cozinha',
            'Dica de organização da geladeira',
            '“O que tem pra hoje?” com enquete'
        ],
        'tiktok': [
            'Receita ASMR',
            'O que eu como em um dia',
            'Recriando receita de filme/série',
            'Teste de receita viral',
            'Dica de aproveitamento de alimentos',
            'Culinária nostálgica',
            'Montagem rápida e estética de prato'
        ],
        'linkedin': [
            'Mercado de gastronomia digital em expansão',
            'Como monetizar receitas nas redes',
            'Parcerias com marcas alimentícias',
            'Branding pessoal para chefs',
            'Culinária e saúde no trabalho',
            'Criando cursos ou eBooks de receitas',
            'Como usar conteúdo culinário como portfólio'
        ]
    },
    'dança': {
        'instagram': [
            'Coreografia da semana',
            'Passo a passo de um movimento difícil',
            'Enquete: “Qual ritmo você quer aprender?”',
            'Making of de ensaios',
            'Desafio de dança com seguidores',
            'Mostre erros de gravação (bloopers)',
            'Dueto com outro criador'
        ],
        'tiktok': [
            'Reagindo a danças virais',
            'Top 3 passos para iniciantes',
            'Evolução do treino (time lapse)',
            'Dança + dica de vida pessoal',
            'Desafio de dança por 30 dias',
            'Remix de música com coreografia própria',
            'Dançando com pais ou amigos'
        ],
        'linkedin': [
            'Dança como ferramenta de disciplina e foco',
            'Empreender com aulas de dança online',
            'Como criar um curso digital de dança',
            'Eventos e shows: bastidores e gestão',
            'Dança e saúde mental no trabalho',
            'Criando comunidade com alunos no digital',
            'Monetização e parcerias no nicho de dança'
        ]
    },
    'escrita': {
        'instagram': [
            'Dica de escrita criativa',
            'Trecho autoral com legenda explicando',
            'Antes e depois de um texto editado',
            'Cenas favoritas de livros comentadas',
            'Desafio de escrita em 1 minuto',
            'Top 3 livros que mudaram sua vida',
            'Ferramenta de escrita que uso'
        ],
        'tiktok': [
            'Reagindo a clichês de livros',
            'Leitura de um trecho autoral',
            'Curiosidades sobre personagens',
            'Como criar diálogos reais',
            'Livros para quem não gosta de ler',
            'Escrita ao vivo com o público',
            'Rotina de escritor (vlog)'
        ],
        'linkedin': [
            'Escrita como diferencial no trabalho',
            'Storytelling como ferramenta de liderança',
            'Case de autopublicação',
            'Como construir autoridade como autor',
            'Escrever e vender eBooks',
            'Escrita criativa aplicada ao marketing',
            'Redes sociais para escritores'
        ]
    },
    'estudos': {
        'instagram': [
            'Dica de estudo rápido',
            'Rotina de estudos em fotos',
            'Ferramentas que uso para estudar',
            'Antes/depois do caderno',
            'Técnica Pomodoro explicada',
            'Bastidores no dia da prova',
            'Estudo ao vivo com seguidores'
        ],
        'tiktok': [
            'Timelapse de estudo com música',
            '“Study with me” em tempo real',
            'Dica de organização do planner',
            'Como memorizar melhor',
            'Vida de vestibulando (realidade)',
            'Top 3 apps de produtividade',
            'Motivação: “Você não está sozinho”'
        ],
        'linkedin': [
            'Como desenvolver disciplina nos estudos',
            'Soft skills adquiridas com estudo constante',
            'Organize semana com estudos e estágio',
            'Como criar conteúdo sobre estudos no LinkedIn',
            'Técnicas de produtividade aplicadas ao trabalho',
            'Gestão de tempo para estudantes',
            'Estudar enquanto trabalha: é possível?'
        ]
    },
    'fitness': {
        'instagram': [
            'Treino em casa com objetos do dia a dia',
            'Antes e depois de alunos',
            'Dicas de suplementação',
            'Desafio fitness de 7 dias',
            'Alongamento para iniciantes',
            'Receita rápida pós-treino',
            'Vídeo motivacional para treinar'
        ],
        'tiktok': [
            'Rotina rápida de exercícios',
            'Desafio de agachamentos diários',
            'Dicas para melhorar a postura',
            'Como usar objetos de casa no treino',
            'Erros comuns na academia',
            'Treino HIIT de 15 minutos',
            'Acompanhamento de evolução pessoal'
        ],
        'linkedin': [
            'Como o fitness melhora a produtividade',
            'A importância do bem-estar no trabalho',
            'Como criar uma aula online de fitness',
            'Empreendendo com programas de saúde',
            'Tendências do mercado fitness digital',
            'Estudo de caso: marca fitness de sucesso',
            'Dicas para balancear trabalho e treino'
        ]
    },
    'alimentação saudável': {
        'instagram': [
            'Smoothies fáceis para o dia a dia',
            'Substituições saudáveis nas receitas',
            'Benefícios de alimentos naturais',
            'Planejamento semanal de refeições',
            'Receita detox rápida',
            'Dicas para reduzir açúcar',
            'Snacks saudáveis para o trabalho'
        ],
        'tiktok': [
            'Como montar marmitas saudáveis',
            'Receita de suco verde',
            'Testando comidas saudáveis populares',
            'Erros comuns em dietas',
            'Benefícios do jejum intermitente',
            'Preparando saladas rápidas',
            'Dicas para aumentar o consumo de fibras'
        ],
        'linkedin': [
            'Mercado de alimentos naturais em crescimento',
            'Empreender com delivery saudável',
            'Tendências em alimentação funcional',
            'Como nutricionistas usam redes sociais',
            'Parcerias entre marcas e influenciadores',
            'Estratégias para vender produtos naturais',
            'Alimentação saudável e produtividade'
        ]
    },
    'empreendedorismo': {
        'instagram': [
            'Dicas para quem está começando',
            'Bastidores do dia a dia empreendedor',
            'Como validar uma ideia de negócio',
            'Erros comuns de novos empreendedores',
            'Motivação e mindset empreendedor',
            'Como montar escritório em casa',
            'Histórias de sucesso inspiradoras'
        ],
        'tiktok': [
            'Passo a passo para abrir empresa',
            'Dicas rápidas de gestão financeira',
            'Ferramentas úteis para empreendedores',
            'Como montar um pitch de vendas',
            'Tendências para pequenos negócios',
            'Respondendo dúvidas frequentes',
            'Dicas para networking eficiente'
        ],
        'linkedin': [
            'Como estruturar plano de negócios',
            'Importância da cultura organizacional',
            'Marketing digital para PME',
            'Liderança e gestão remota',
            'Financiamento e captação de recursos',
            'Estudos de caso de startups',
            'Usar LinkedIn para negócios B2B'
        ]
    }
}

def gerar_cronograma(nicho, plataformas, dias=7):
    hoje = datetime.today()
    cronograma = []

    for i in range(dias):
        data = hoje + timedelta(days=i)
        dia = data.strftime('%d/%m/%Y')

        for plataforma in plataformas:
            ideias = banco_ideias.get(niche, {}).get(plataforma, [])
            if ideias:
                ideia = ideias[i % len(ideias)]  # alterna as ideias
                cronograma.append({
                    'Data': dia,
                    'Plataforma': plataforma.capitalize(),
                    'Ideia de Conteúdo': ideia
                })
    
    return pd.DataFrame(cronograma)

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
    """)

     with st.sidebar:
        st.header("⚙️ Configurações")
    
        niche = st.selectbox(
            "Seu nicho/área:",
            ["Moda", "Culinária", "Dança", "Escrita", "Estudos", "Fitness", "Alimentação Saudável", "Empreendedorismo"]
        )
        platforms = st.multiselect(
            "Plataformas:",
            ["Instagram", "TikTok", "LinkedIn", "Youtube"],
            default=["Instagram", "TikTok"]
        )

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
        with st.spinner("Gerando cronograma..."):
            content_ideas = get_content_ideas(
                niche,
                creativity
            )
            st.write("Ideias geradas:", content_ideas) 

st.write("Escolha o nicho")
nicho = st.text_input(' (ex: moda, culinária): ').strip().lower()
st.write("Escolha as plataformas separadas por vírgula (instagram, tiktok, linkedin):")
plataformas = st.text_input(' (instagram, tiktok, linkedin): ')
if plataformas:
    plataformas=[p.strip().lower() for p in plataformas.split(',')]
    df_cronograma = gerar_cronograma(nicho, plataformas, dias=7)
    st.write("\n🔹 Cronograma de Conteúdo (7 dias):")
    st.write(df_cronograma)
