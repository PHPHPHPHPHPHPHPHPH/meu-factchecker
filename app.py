import streamlit as st
import google.generativeai as genai

# Configuração da página para ficar bonita no celular
st.set_page_config(
    page_title="Fact-Checker IA",
    page_icon="⚖️",
    layout="centered"
)

# Chave API protegida (vamos configurar isso na hospedagem)
CHAVE_API_GEMINI = st.secrets["CHAVE_API_GEMINI"]

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
        
        if resposta.candidates and len(resposta.candidates) > 0:
            partes_texto = [part.text for part in resposta.candidates.content.parts if part.text]
            return "".join(partes_texto)
        return "⚠️ A resposta retornou vazia da API."
        
    except Exception as e:
        return f"🚨 Erro de Sistema: {e}"

# --- INTERFACE DO USUÁRIO (MOBILE FRIENDLY) ---
st.title("🤖 Verificador de Fatos Inteligente")
st.write("Digite uma afirmação ou boato para receber uma análise baseada em consenso científico.")

# Caixa de texto adaptada para celular
frase_teste = st.text_input("O que você quer checar?", placeholder="Ex: Tomar muita coca cola faz mal à saúde")

# Botão grande e fácil de clicar na tela touch
if st.button("🔍 Processar Veredicto", use_container_width=True):
    if frase_teste.strip():
        with st.spinner("🧠 Consultando inteligência de dados..."):
            resultado = checar_fato_definitivo(frase_teste)
            st.markdown("---")
            st.markdown(resultado)
    else:
        st.warning("⚠️ Por favor, digite alguma frase antes de pesquisar.")
