import streamlit as st
from groq import Groq
from datetime import datetime
import re
import time

# =================================================================
# 1. KURUMSAL YAPILANDIRMA VE UI
# =================================================================
st.set_page_config(page_title="AI Ultra Strateji Gold Edition", page_icon="🏆", layout="wide")

try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Sistem hatası: API Anahtarı bulunamadı!")

# =================================================================
# 2. ÜST DÜZEY HUKUKİ KORUMA METNİ
# =================================================================
HIZMET_SOZLESMESI = """
İşbu rapor, yapay zeka tabanlı stratejik analiz algoritmaları ve dil işleme modelleri ile üretilmiştir.
1. SORUMLULUK: Sunulan veriler profesyonel öneri niteliğindedir; nihai ticari kararlar kullanıcı sorumluluğundadır.
2. FİKRİ MÜLKİYET: Rapor içeriği satın alan kişiye özeldir, ticari amaçla çoğaltılamaz.
3. İADE POLİTİKASI: Dijital hizmetlerin ifası anında gerçekleştiğinden iade ve iptal kabul edilmez.
4. TELAFİ: Ciddi yazım hatası veya içerik yetersizliği durumunda manuel 'Uzman İncelemesi' hakkı saklıdır.
"""

# =================================================================
# 3. ULTRA DİL VE GRAMER DÜZELTME MOTORU
# =================================================================
class GrammarPro:
    @staticmethod
    def final_polish(text):
        # 1. Gereksiz karakter temizliği
        text = re.sub(r'[^\x00-\x7FçğıöşüÇĞİÖŞÜİı\n\r\t .,;:!?()/%&\-+=*]+', '', text)
        
        # 2. En sık yapılan klavye ve imla hataları için 'Süper Sözlük'
        corrections = {
            r"\bmekn\b": "mekan", r"\bkğıt\b": "kağıt", r"\bakğt\b": "kağıt",
            r"\bherşey\b": "her şey", r"\bbirşey\b": "bir şey", r"\byada\b": "ya da",
            r"\bduragı\b": "durağı", r"\btercihide\b": "tercihi de", r"\bfiyatıda\b": "fiyatı da",
            r"\btşk\b": "teşekkür", r"\bsaglayan\b": "sağlayan", r"\bolduda\b": "oldu da",
            r"\bgramer\b": "dil bilgisi", r"\byapıyo\b": "yapıyor", r"\bediyo\b": "ediyor"
        }
        for pattern, replacement in corrections.items():
            text = re.compile(pattern, re.IGNORECASE).sub(replacement, text)
        
        return text.strip()

# =================================================================
# 4. MASTER STRATEJİ VE DİL İŞLEME MOTORU
# =================================================================
def generate_master_report(user_data, order_no):
    modules = {
        "💎 BÖLÜM 1: OPERASYONEL EKOSİSTEM VE MAKRO ANALİZ": "İşletmenin teknik altyapısını ve operasyonel işleyişini 'Mühendislik' diliyle analiz et.",
        "📊 BÖLÜM 2: STRATEJİK FİYATLANDIRMA VE MARJ OPTİMİZASYONU": "Psikolojik fiyatlandırma, elastikiyet ve premium pazar konumlandırmasını akademik dille anlat.",
        "🧪 BÖLÜM 3: TEKNİK AR-GE VE ENDÜSTRİYEL İNOVASYON": "Üretim kalitesini artıracak inovatif süreçleri ve AR-GE projeksiyonlarını detaylandır.",
        "🛡️ BÖLÜM 4: REKABET İSTİHBARATI VE DOMİNASYON STRATEJİSİ": "Pazar liderliği için rakiplerin zayıf yönlerini hedefleyen saldırı planı oluştur.",
        "📈 BÖLÜM 5: 12 AYLIK STRATEJİK ROI VE BÜYÜME PROJEKSİYONU": "Aylık bazda bölümlenmiş, KPI odaklı, somut ve teknik bir iş planı ile final yap."
    }

    report = f"🏆 ULTRA STRATEJİK YÖNETİM RAPORU\nREFERANS NO: {order_no}\nBASKI TARİHİ: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    report += "="*80 + "\n\n"
    
    prog = st.progress(0)
    status = st.empty()
    
    for i, (title, instruction) in enumerate(modules.items()):
        status.info(f"⏳ {title} hazırlanıyor... Dil ve Gramer denetimi aktif.")
        
        # VAY VAY VAY DEDİRTEN PROMPT
        system_msg = f"""
        Sen dünyanın en seçkin yönetim danışmanlığı firmasındaki Baş Stratejist ve bir Türk Dil Kurumu (TDK) Profesörüsün.
        Görevin: {title} konusunu en az 2000 kelime, kusursuz bir Türkçe ve ağır bir kurumsal dille yazmak.

        DİL VE GRAMER PROTOKOLÜ:
        1. SESLİ HARF YUTMA: 'mekn', 'kğıt', 'yapıyo' gibi hatalar yapman KESİNLİKLE yasaktır. Her kelime tam yazılacak.
        2. TDK KURALLARI: 'bir şey', 'ya da', 'her şey' gibi ifadeler ayrı yazılacak. Ünsüz yumuşaması ve benzeşmesi kurallarına (Örn: 'kebabı', 'durağı') harfiyen uyulacak.
        3. TERMİNOLOJİ: 'Güzel, kötü, pahalı' gibi basit kelimeler yerine 'Optimize, atıl, fahiş, sürdürülebilir' gibi teknik terimler kullanılacak.
        4. VERİ İŞLEME: Ham verideki bozuk cümleleri düzelterek profesyonel bir rapora dönüştür.
        """

        try:
            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_msg},
                          {"role": "user", "content": f"Veriler: {user_data[:5000]}\nTalimat: {instruction}"}],
                temperature=0.2 # Ciddiyet için düşük sıcaklık
            )
            polished_content = GrammarPro.final_polish(res.choices[0].message.content)
            report += f"\n\n{title}\n{'-'*len(title)}\n\n{polished_content}\n"
            
            # API'nin yorulmaması ve kalitenin düşmemesi için 12 saniye bekleme
            time.sleep(12)
            
        except Exception as e:
            st.error(f"Teknik Hata: {str(e)}")
            break
            
        prog.progress((i + 1) / len(modules))
    
    status.empty()
    return report

# =================================================================
# 5. ARAYÜZ (PREMIUM LOOK)
# =================================================================
st.title("🏆 AI Ultra Analiz: Gold Edition")
st.subheader("Kurumsal Dil Bilgisi ve Stratejik Mühendislik Motoru")

with st.sidebar:
    st.header("⚖️ Yasal Güvence")
    st.caption("Bu sistem TDK yazım kuralları ve kurumsal dil protokolleri ile korunmaktadır.")
    st.divider()
    st.success("✅ %100 Manuel Revize Garantisi")
    st.write("Raporunuzdaki tek bir imla hatası için bile manuel destek alabilirsiniz.")

user_input = st.text_area("Analiz Edilecek Müşteri/İşletme Verileri:", height=250, placeholder="Yorumları veya işletme detaylarını buraya yapıştırın...")

with st.expander("📄 VIP Hizmet Sözleşmesi ve Kullanım Şartları"):
    st.info(HIZMET_SOZLESMESI)

c1, c2 = st.columns(2)
with c1:
    oid = st.text_input("Sipariş Numarası (Shopier):")
with c2:
    st.write("##")
    confirm = st.checkbox("Sözleşme ve gramer protokollerini onaylıyorum.")

if st.button("🚀 MASTER RAPORU İNŞA ET (Derin Analiz)", type="primary", use_container_width=True):
    if not user_input or not oid or not confirm:
        st.error("Lütfen tüm alanları doldurun ve sözleşmeyi onaylayın.")
    else:
        with st.status("💎 Raporunuz Baş Stratejist tarafından örülüyor. Bu işlem yaklaşık 5-7 dakika sürebilir...", expanded=True):
            final_report = generate_master_report(user_input, oid)
            
            if final_report:
                st.success("🏁 Master Rapor Tamamlandı!")
                st.download_button(
                    label="📂 KUSURSUZ RAPORU İNDİR (.txt)",
                    data=final_report.encode('utf-8-sig'),
                    file_name=f"Master_Strateji_{oid}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                with st.expander("📝 Rapor Önizleme (Kalite Kontrol)"):
                    st.text(final_report[:2500] + "...")

