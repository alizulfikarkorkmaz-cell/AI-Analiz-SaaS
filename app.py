import streamlit as st
from groq import Groq

# Streamlit Secrets'tan anahtarı çekiyoruz
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin.")

st.set_page_config(page_title="AI Ürün Analiz", page_icon="🚀")
st.title("🚀 Akıllı Ürün Analiz Paneli")

user_input = st.text_area("Müşteri yorumlarını buraya yapıştırın:", height=200)

if st.button("Hemen Analiz Et"):
    if user_input:
        with st.spinner('Yapay Zeka (Llama 3) inceliyor...'):
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"Aşağıdaki yorumları analiz et ve Türkçe olarak: 1. Memnuniyet oranı, 2. Temel şikayetler, 3. Çözüm önerisi yaz: {user_input}",
                    }
                ],
                model="llama3-8b-8192",
            )
            st.success("Analiz Hazır!")
            st.write(chat_completion.choices[0].message.content)
    else:
        st.warning("Lütfen yorum girin!")
