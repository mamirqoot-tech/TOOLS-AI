import streamlit as st
import requests
from PIL import Image

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Generator Skrip TikTok Shop", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop")
st.write("Buat naskah video dan caption TikTok Shop secara terpisah (Maksimal 900 Kata).")

# Form Input
with st.form("tiktok_form"):
    nama_produk = st.text_input("Nama Produk TikTok Shop", placeholder="Contoh: Solder 80W / Lampu Akrilik")
    keunggulan = st.text_area("Keunggulan / Promo Produk", placeholder="Contoh: Gratis ongkir, diskon 50%, cepat panas")
    
    uploaded_image = st.file_uploader(
        "Upload Referensi Gambar Produk (Opsional)", 
        type=["jpg", "jpeg", "png", "webp"]
    )
    
    gaya = st.selectbox("Gaya Video", ["Review Jujur", "Hard Sell", "Soft Sell", "Spill Harga Murah"])
    
    submitted = st.form_submit_button("🚀 Buat Skrip Sekarang")

def get_recommended_hashtags(style, produk):
    tag_produk = f"#{produk.lower().replace(' ', '')}"
    if style == "Spill Harga Murah":
        return f"{tag_produk} #fypindonesia #viral2026 #trendingindonesia #tiktoktrend #harianviral"
    elif style == "Soft Sell":
        return f"{tag_produk} #inspirasi2026 #kontenpositif #idekreatif #kreatorindo #edukatif"
    elif style == "Review Jujur":
        return f"{tag_produk} #trendingnow #tiktokindo #videoviral #kreatifbanget #foryoupage"
    else:
        return f"{tag_produk} #fypindonesia #foryou #viralindonesia #explorepage #supportlokal"

def potong_maksimal_900_kata(text):
    words = text.split()
    if len(words) > 900:
        return " ".join(words[:900])
    return text

# Proses Saat Tombol Diklik
if submitted:
    if not nama_produk:
        st.error("Isi nama produk terlebih dahulu!")
    else:
        if uploaded_image is not None:
            st.image(uploaded_image, caption=f"Referensi: {nama_produk}", use_container_width=True)
            
        with st.spinner("Sedang memproses skrip..."):
            hashtags = get_recommended_hashtags(gaya, nama_produk)
            
            # 1. BAGIAN NASKAH / SKRIP VIDEO
            naskah_video = f"""[PANDUAN VIDEO 20 DETIK: {nama_produk}]
Gaya: {gaya}. VO: Natural, jelas. Musik: Tidak Ada.

📌 Hook: {nama_produk} viral, promo {keunggulan}!
🎬 Isi: Kualitas mantap, cepat panas, hemat listrik. Stok terbatas.
🛒 CTA: Checkout sekarang di keranjang kuning!

ATURAN: Gunakan hanya yang ada di gambar. Bentuk/warna akurat. No klaim berlebihan. VO natural, durasi pas 20s."""

            # 2. BAGIAN CAPTION & HASHTAG
            caption_dan_hashtag = f"""Promo {nama_produk} hari ini! {keunggulan}. 
Jangan sampai kehabisan stoknya, yuk checkout sekarang sebelum kehabisan! 🔥

Tag: {hashtags}"""

            # Batasi kata maksimal 900 kata
            naskah_video_final = potong_maksimal_900_kata(naskah_video)
            caption_final = potong_maksimal_900_kata(caption_dan_hashtag)

            st.success("✨ Skrip & Caption Berhasil Dipisahkan!")

            # TAMPILAN PISAH 1: NASKAH VIDEO
            st.write("### 🎬 1. Naskah Skrip Video (VO & Visual)")
            st.code(naskah_video_final, language="markdown")
            st.download_button(
                label="📥 Download Naskah Video (TXT)",
                data=naskah_video_final,
                file_name=f"naskah_video_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )

            st.write("---")

            # TAMPILAN PISAH 2: CAPTION & HASHTAG
            st.write("### 📝 2. Caption & Hashtag TikTok")
            st.code(caption_final, language="markdown")
            st.download_button(
                label="📥 Download Caption & Hashtag (TXT)",
                data=caption_final,
                file_name=f"caption_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )