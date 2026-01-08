import streamlit as st
from groq import Groq

# Kasadaki anahtarı kullanıyoruz
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Kasa anahtarı (Secret) hatalı!")

st.set_page_config(page_title="Yapay Zeka Analiz", page_icon="🚀")
st.title("🚀 Akıllı Ürün Analiz Motoru")

user_input = st.text_area("Yorumları buraya yapıştırın:", placeholder="Örn: Ürün çok güzel ama kargo yavaştı...", height=200)

if st.button("Hemen Strateji Üret"):
    if user_input:
        with st.spinner('Yapay Zeka derinlemesine inceliyor...'):
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Şu yorumları analiz et: {user_input}. Bana Türkçe olarak 1. Memnuniyet %'si, 2. En büyük sorun, 3. Satış artırıcı tavsiye ver."}],
                    model="llama3-8b-8192",
                )
                st.success("Analiz Tamamlandı!")
                st.markdown(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
    else:
        st.warning("Analiz için yorum girmelisin usta!")
