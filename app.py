import streamlit as st
import requests
from PIL import Image

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Generator Skrip TikTok Shop", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop")
st.write("Buat naskah video (maksimal 900 kata) dan caption TikTok Shop secara terpisah.")

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
        return f"{tag_produk} #fypindonesia #viral2026 #trendingindonesia #tiktoktrend #harianviral #videoviral #kontenkekinian #harianviral #exploreindo #postinganviral"
    elif style == "Soft Sell":
        return f"{tag_produk} #inspirasi2026 #kontenpositif #idekreatif #kreatorindo #edukatif #vibespositif #goodvibesonly #inspiratif #motivasihidup"
    elif style == "Review Jujur":
        return f"{tag_produk} #trendingnow #tiktokindo #videoviral #kreatifbanget #foryoupage #contentcreator #kontenunik #lifestyleindonesia"
    else:
        return f"{tag_produk} #fypindonesia #foryou #viralindonesia #explorepage #supportlokal #tiktokcommunity #kreatorindo #indonesiamaju"

def count_words(text):
    if not text:
        return 0
    return len(text.split())

def potong_maksimal_900_kata(text):
    """Memotong teks naskah secara ketat jika melebihi 900 kata."""
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
            
            # 1. BAGIAN NASKAH / SKRIP VIDEO (Dibatasi Maksimal 900 Kata)
            naskah_video_mentah = f"""[PANDUAN VIDEO 20 DETIK: {nama_produk}]
Gaya: {gaya}. VO: Natural, jelas. Musik: Tidak Ada.

📌 HOOK (Detik 0-3)
Teks Layar: JANGAN BELI {nama_produk.upper()} SEBELUM LIHAT INI! 😱
Voiceover: "Jangan beli {nama_produk} sebelum kamu lihat promo hari ini!"

🎬 ISI KONTEN (Detik 3-15)
Visual: Tunjukkan detail produk {nama_produk} secara dekat di depan kamera. Perlihatkan bentuk, warna, dan material produk secara akurat.
Voiceover: "Biasanya harganya mahal, tapi khusus hari ini lagi ada promo {keunggulan}. Kualitasnya mantap banget dan sangat rekomended buat dimiliki!"

🛒 CALL TO ACTION (Detik 15-20)
Visual: Tunjuk panah ke arah keranjang kuning di kiri bawah.
Voiceover: "Langsung klik keranjang kuning di kiri bawah sebelum stok promonya habis!"

ATURAN PENTING
Gunakan hanya produk dan perlengkapan yang terlihat pada gambar referensi. Jangan mengubah warna, bentuk, jumlah, atau desain produk. Jangan menambahkan produk atau fitur yang tidak terlihat. Jangan membuat klaim berlebihan. Jangan menampilkan api, percikan listrik, atau asap berlebihan. Jangan menggunakan musik. Pastikan voice-over terdengar natural dan seluruh video tepat 20 detik."""

            # Memotong Naskah Video agar TIDAK LEBIH dari 900 kata
            naskah_video_final = potong_maksimal_900_kata(naskah_video_mentah)
            kata_naskah = count_words(naskah_video_final)

            # 2. BAGIAN CAPTION & HASHTAG (Boleh Lebih Panjang / Fleksibel)
            caption_dan_hashtag = f"""🔥 PROMO SPESIAL {nama_produk.upper()} 🔥

Lagi cari {nama_produk} dengan kualitas terbaik dan harga terjangkau? Ini solusinya! 
Produk ini hadir dengan keunggulan utama: {keunggulan}.

Kenapa harus beli sekarang?
✅ Kualitas terjamin dan sesuai gambar referensi
✅ Promo khusus hari ini: {keunggulan}
✅ Garansi pengiriman cepat dan aman

Jangan tunggu sampai stok habis! Yuk langsung di-checkout sekarang juga melalui keranjang kuning di bawah ini! 👇

{hashtags}"""
            
            kata_caption = count_words(caption_dan_hashtag)

            st.success("✨ Skrip & Caption Berhasil Dibuat!")

            # TAMPILAN PISAH 1: NASKAH VIDEO (Maksimal 900 Kata)
            st.write(f"### 🎬 1. Naskah Skrip Video (VO & Visual) — [{kata_naskah} Kata / Maks 900 Kata]")
            st.code(naskah_video_final, language="markdown")
            st.download_button(
                label="📥 Download Naskah Video (TXT)",
                data=naskah_video_final,
                file_name=f"naskah_video_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )

            st.write("---")

            # TAMPILAN PISAH 2: CAPTION & HASHTAG (Fleksibel / Tanpa Batas 900 Kata)
            st.write(f"### 📝 2. Caption & Hashtag TikTok — [{kata_caption} Kata]")
            st.code(caption_dan_hashtag, language="markdown")
            st.download_button(
                label="📥 Download Caption & Hashtag (TXT)",
                data=caption_dan_hashtag,
                file_name=f"caption_{nama_produk.lower().replace(' ', '_')}.txt",
                mime="text/plain"
            )