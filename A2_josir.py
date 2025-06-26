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
            ideias = banco_ideias.get(nicho, {}).get(plataforma, [])
            if ideias:
                ideia = ideias[i % len(ideias)]  # alterna as ideias
                cronograma.append({
                    'Data': dia,
                    'Plataforma': plataforma.capitalize(),
                    'Ideia de Conteúdo': ideia
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
