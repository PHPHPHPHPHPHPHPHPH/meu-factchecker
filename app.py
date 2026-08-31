import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Fact-Checker IA",
    page_icon="⚖️",
    layout="centered"
)

CHAVE_API_GEMINI = st.secrets["CHAVE_API_GEMINI"]

# SOLUÇÃO PARA A COTA: O Cache salva as respostas por 1 hora (3600 segundos) 
# para não estourar os limites da API à toa.
@st.cache_data(ttl=3600)
def checar_fato_definitivo(afirmacao):
    try:
        genai.configure(api_key=CHAVE_API_GEMINI)
        model = genai.GenerativeModel('gemini-3.6-flash')
        
        prompt = f"""
        Escreva um artigo de checagem de fatos detalhado e explicativo sobre a seguinte frase: "{afirmacao}"
        
        Sua resposta final deve ser estruturada obrigatoriamente assim em Markdown:
        # ⚖️ VEREDITO: [Defina em maiúsculo se é VERDADEIRO ou FALSO]
        
        ### 📋 Resumo Direto
        [Adicione 2 frases diretas explicando o porquê do veredito]
        
        ### 🔍 Detalhes Científicos e Médicos
        [Crie um ou dois parágrafos longos, aprofundados e explicativos contendo o consenso científico ou médico sobre o assunto]
        """
        
        resposta = model.generate_content(prompt)
        
        if resposta and resposta.text:
            return resposta.text
        return "⚠️ A resposta retornou vazia da API do Gemini."
        
    except Exception as e:
        return f"🚨 Erro de Sistema ao processar resposta: {e}"

# --- INTERFACE DO USUÁRIO ---
st.title("🤖 Verificador de Fatos Inteligente")
st.write("Digite uma afirmação ou boato para receber uma análise baseada em consenso científico.")

with st.form(key="meu_formulario_factcheck"):
    frase_teste = st.text_input("O que você quer checar?", placeholder="Ex: Tomar muita coca cola faz mal à saúde")
    botao_enviar = st.form_submit_button("🔍 Processar Veredicto", use_container_width=True)

if botao_enviar:
    if frase_teste.strip():
        with st.spinner("🧠 Consultando inteligência de dados..."):
            # O Streamlit confere no cache antes de chamar a API externa
            resultado = checar_fato_definitivo(frase_teste)
            st.markdown("---")
            st.markdown(resultado)
    else:
        st.warning("⚠️ Por favor, digite alguma frase antes de pesquisar.")
