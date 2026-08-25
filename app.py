import streamlit as st
import google.generativeai as genai
from PIL import Image
import json

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Generator Skrip TikTok Shop (Vision)", layout="centered", page_icon="🛍️")

st.title("🛍️ Generator Skrip TikTok Shop Otomatis")
st.write("Upload gambar produk untuk mengisi detail secara otomatis (Maksimal 900 Kata).")

# Konfigurasi Google Gemini API Key
# Masukkan API Key Anda di bawah ini
GEMINI_API_KEY = "MASUKKAN_API_KEY_GEMINI_ANDA"
if GEMINI_API_KEY != "MASUKKAN_API_KEY_GEMINI_ANDA":
    genai.configure(api_key=GEMINI_API_KEY)

# Initial State untuk menyimpan data hasil ekstraksi gambar
if "nama_produk_auto" not in st.session_state:
    st.session_state["nama_produk_auto"] = ""
if "keunggulan_auto" not in st.session_state:
    st.session_state["keunggulan_auto"] = ""

# 1. MENU UPLOAD GAMBAR DI PALING ATAS
uploaded_image = st.file_uploader(
    "1. Upload Referensi Gambar Produk (Deteksi Otomatis)", 
    type=["jpg", "jpeg", "png", "webp"]
)

# Proses ekstraksi gambar jika ada file baru diunggah
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Gambar Referensi Produk", use_container_width=True)
    
    if st.button("🔍 Ekstrak Info dari Gambar"):
        if GEMINI_API_KEY == "MASUKKAN_API_KEY_GEMINI_ANDA":
            st.error("Silakan isi GEMINI_API_KEY pada kode terlebih dahulu!")
        else:
            with st.spinner("Menganalisis gambar produk..."):
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    prompt_vision = """
                    Analisis gambar produk ini. Kembalikan respons HANYA dalam format JSON berikut:
                    {
                        "nama_produk": "Nama produk ringkas",
                        "keunggulan": "3 keunggulan utama produk yang terlihat atau relevan"
                    }
                    """
                    response = model.generate_content([prompt_vision, image])
                    # Clean JSON response
                    clean_json = response.text.replace("```json", "").replace("```", "").strip()
                    data = json.loads(clean_json)
                    
                    # Simpan ke session state Streamlit
                    st.session_state["nama_produk_auto"] = data.get("nama_produk", "")
                    st.session_state["keunggulan_auto"] = data.get("keunggulan", "")
                    st.success("Teks berhasil diekstrak dari gambar!")
                except Exception as e:
                    st.error(f"Gagal menganalisis gambar: {e}")

st.write("---")

# 2. FORM INPUT (TERISI OTOMATIS JIKA GAMBAR DIEKSTRAK)
with st.form("tiktok_form"):
    st.write("### 2. Form Detail Produk")
    nama_produk = st.text_input(
        "Nama Produk TikTok Shop", 
        value=st.session_state["nama_produk_auto"],
        placeholder="Contoh: Solder 80W / Lampu Akrilik"
    )
    keunggulan = st.text_area(
        "Keunggulan / Promo Produk", 
        value=st.session_state["keunggulan_auto"],
        placeholder="Contoh: Gratis ongkir, diskon 50%, cepat panas"
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

# PROSES GENERATE SKRIP
if submitted:
    if not nama_produk:
        st.error("Isi nama produk terlebih dahulu!")
    else:
        hashtags = get_recommended_hashtags(gaya, nama_produk)
        header_perintah = f"[PANDUAN VIDEO 20 DETIK: {nama_produk}]\nGaya: Realistis/Elektronik. VO: Natural, jelas. Musik: Tidak Ada.\n\n"
        footer_aturan = "\n\nATURAN: Gunakan hanya yang ada di gambar. Bentuk/warna akurat. No klaim berlebihan/api/asap. VO natural, durasi pas 20s."

        skrip_template = f"""📌 Hook: {nama_produk} viral, promo {keunggulan}!
🎬 Isi: Kualitas mantap, cepat panas, hemat listrik. Stok terbatas.
🛒 CTA: Checkout sekarang di keranjang kuning!
Tag: {hashtags}"""
        
        skrip_akhir = potong_maksimal_900_kata(header_perintah + skrip_template + footer_aturan)
        jumlah_kata = len(skrip_akhir.split())

        st.success(f"✨ Skrip Berhasil Dibuat! (Total: {jumlah_kata} Kata - Maksimal 900 Kata)")
        st.code(skrip_akhir, language="markdown")
        st.download_button(
            label="📥 Download Skrip (TXT)",
            data=skrip_akhir,
            file_name=f"skrip_{nama_produk.lower().replace(' ', '_')}.txt",
            mime="text/plain"
        )