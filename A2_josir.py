### Código Oficial
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from fpdf import FPDF

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
        ],
        'youtube': [
            'Lookbook completo da estação',
            'Dicas de compras inteligentes',
            'Tutorial de customização de roupas',
            'Vlog de evento de moda',
            'Entrevista com estilista famoso',
            'Análise de tendências do mercado',
            'Como montar um guarda-roupa cápsula'
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
        ],
        'youtube': [
            'Receitas detalhadas passo a passo',
            'Vídeos de técnicas culinárias',
            'Tour pela cozinha profissional',
            'Desafios de culinária com convidados',
            'Análise de tendências gastronômicas',
            'Entrevistas com chefs renomados',
            'Como montar cardápios saudáveis'
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
        ],
        'youtube': [
            'Aulas completas de dança para iniciantes',
            'Coreografias detalhadas por ritmo',
            'Vlogs de eventos e workshops',
            'Entrevistas com profissionais da dança',
            'Dicas para melhorar técnica',
            'Rotinas de treino para dança fitness',
            'História dos estilos de dança'
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
        ],
        'youtube': [
            'Workshops de escrita criativa',
            'Análise de obras literárias',
            'Dicas para autores independentes',
            'Escrita ao vivo e exercícios práticos',
            'Entrevistas com escritores',
            'Como publicar seu livro',
            'Storytelling para marketing'
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
        ],
        'youtube': [
            'Aulas online para reforço escolar',
            'Técnicas de estudo detalhadas',
            'Planos de estudo para concursos',
            'Dicas para organização do tempo',
            'Vídeos motivacionais para estudantes',
            'Como usar apps de estudo',
            'Entrevistas com especialistas em educação'
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
        ],
        'youtube': [
            'Treinos completos para casa',
            'Dicas de exercícios para iniciantes',
            'Rotinas de alongamento e mobilidade',
            'Vídeos motivacionais de transformação',
            'Nutrição para atletas amadores',
            'Técnicas de treino HIIT',
            'Entrevistas com personal trainers'
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
        ],
        'youtube': [
            'Receitas saudáveis passo a passo',
            'Explicações sobre superalimentos',
            'Desafios de alimentação saudável',
            'Vlogs de mercado orgânico',
            'Entrevistas com nutricionistas',
            'Planejamento de refeições semanais',
            'Como ler rótulos de alimentos'
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
        ],
        'youtube': [
            'Como começar um negócio do zero',
            'Estratégias de marketing para startups',
            'Entrevistas com empreendedores de sucesso',
            'Dicas para gestão financeira pessoal',
            'Como criar um pitch vencedor',
            'Ferramentas essenciais para empreendedores',
            'Erros comuns e como evitá-los'
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
            ideias = banco_ideias.get(nicho, {}).get(plataforma, [])
            if ideias:
                ideia = ideias[i % len(ideias)]  # alterna as ideias
                cronograma.append({
                    'Data': dia,
                    'Plataforma': plataforma.capitalize(),
                    'Ideia de Conteúdo': ideia
                })
    
    return pd.DataFrame(cronograma)
    start_date = datetime.today()
    pdf_data = generate_pdf(
        schedule=df.rename(columns={
            'Ideia de Conteúdo': 'Tópico',
            'Plataforma': 'Plataforma',
            'Data': 'Data'
        }),
        niche=nicho.capitalize(),
        objective="Aumentar engajamento",
        start_date=start_date
    )
    st.download_button(
        label="📄 Baixar como PDF",
        data=pdf_data,
        file_name="cronograma_conteudo.pdf",
        mime="application/pdf"
    )

def generate_pdf(schedule, nicho, objective, start_date):
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
        layout="wide"
    )

    st.title("📅 Social Content Planner - IA")
    st.markdown("**Crie cronogramas de conteúdo perfeitos para suas redes sociais**")

    # Configurações na barra lateral
    with st.sidebar:
        st.header("⚙️ Configurações")
        nicho = st.selectbox(
            "Escolha seu nicho:",
            list(banco_ideias.keys()),
            format_func=lambda x: x.capitalize()
        )
        plataformas = st.multiselect(
            "Selecione as plataformas:",
            ["instagram", "tiktok", "linkedin"],
            default=["instagram", "tiktok"]
        )
        dias = st.slider("Dias de cronograma", 1, 31, 7)

        gerar = st.button("Gerar Cronograma")

    # Resultado
    if gerar:
        df = gerar_cronograma(nicho, plataformas, dias)
        st.subheader("🔹 Cronograma de Conteúdo")
        st.dataframe(df)

        # Exportar CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar como CSV",
            data=csv,
            file_name="cronograma_conteudo.csv",
            mime='text/csv'
        )

# Executa a função principal
if __name__ == "__main__":
    main()
