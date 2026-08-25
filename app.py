import streamlit as st
import requests

st.set_page_config(page_title="Generator Skrip TikTok Shop", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop")
st.write("Buat naskah video jualan TikTok Shop secara gratis tanpa API Key.")

with st.form("tiktok_form"):
    nama_produk = st.text_input("Nama Produk TikTok Shop", placeholder="Contoh: Lampu Tidur Akrilik")
    keunggulan = st.text_area("Keunggulan / Promo Produk", placeholder="Contoh: Gratis ongkir, diskon 50%")
    gaya = st.selectbox("Gaya Video", ["Hard Sell", "Soft Sell / Storytelling", "Review Jujur"])
    
    submitted = st.form_submit_button("🚀 Buat Skrip Sekarang")

def generate_script_free(produk, promo, style):
    # Menggunakan model open-source publik via Hugging Face Router
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    
    prompt = f"<s>[INST] Buatkan skrip TikTok Shop singkat untuk produk {produk} dengan keunggulan {promo} dan gaya {style}. Berikan HOOK, ISI, dan CALL TO ACTION dalam bahasa Indonesia. [/INST]"
    
    response = requests.post(API_URL, json={"inputs": prompt, "parameters": {"max_new_tokens": 500}})
    
    if response.status_code == 200:
        result = response.json()
        return result[0]["generated_text"].replace(prompt, "").strip()
    else:
        return None

if submitted:
    if not nama_produk:
        st.error("Isi nama produk terlebih dahulu!")
    else:
        with st.spinner("Sedang memproses skrip..."):
            skrip = generate_script_free(nama_produk, keunggulan, gaya)
            if skrip:
                st.success("Skrip Berhasil Dibuat!")
                st.markdown(skrip)
            else:
                st.error("Gagal terhubung ke server gratis. Silakan coba klik tombol sekali lagi.")