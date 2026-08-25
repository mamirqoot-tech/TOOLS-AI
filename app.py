import streamlit as st
import google.generativeai as genai

# Konfigurasi Tampilan Aplikasi
st.set_page_config(page_title="AI TikTok Affiliate Generator", layout="centered")

st.title("🚀 TikTok Affiliate Content Generator AI")
st.write("Generate skrip, storytelling, dan panduan visual video TikTok Affiliate dalam hitungan detik.")

# Form Input Pengguna
with st.form("affiliate_form"):
    nama_produk = st.text_input("Nama Produk", placeholder="Contoh: Solder 80W / Skincare Brightening")
    
    target_audiens = st.multiselect(
        "Target Audiens",
        ["Ibu Rumah Tangga", "Gen Z", "Pekerja Kantor", "Pelajar/Mahasiswa", "Pria/Wanita Umum"],
        default=["Gen Z"]
    )
    
    keunggulan = st.text_area("Keunggulan Utama Produk", placeholder="Contoh: Cepat panas, hemat listrik, garansi 1 tahun")
    
    gaya_penyampaian = st.selectbox(
        "Gaya Penyampaian / Durasi",
        [
            "Video Pendek Cepat (10-15 Detik)",
            "Review Jujur (30-45 Detik)",
            "Sketsa Drama Pendek (30-45 Detik)",
            "Storytelling Emosional (45-60 Detik)"
        ]
    )
    
    api_key = st.text_input("Masukkan API Key Gemini", type="password", help="Dapatkan API key gratis dari Google AI Studio")
    
    submitted = st.form_submit_button("✨ Generate Konten Sekarang")

# Proses saat Tombol Diklik
if submitted:
    if not api_key or not nama_produk:
        st.error("Mohon isi Nama Produk dan API Key Gemini terlebih dahulu!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""
            Bertindaklah sebagai Senior Content Director dan TikTok Affiliate Expert. 
            Buatkan satu paket lengkap pembuatan konten TikTok siap pakai untuk produk berikut:

            - Nama Produk: {nama_produk}
            - Target Audiens: {', '.join(target_audiens)}
            - Keunggulan Utama: {keunggulan}
            - Gaya Penyampaian: {gaya_penyampaian}

            Berikan output dengan struktur persis seperti ini:

            1. JUDUL & HOOK (Detik 0-3)
            - Teks di Layar (On-Screen Text): 
            - Kalimat Pembuka (Voiceover): 

            2. NASKAH STORYTELLING & VISUAL
            - Alur Cerita & Dialog: 
            - Panduan Adegan Visual: 

            3. CALL TO ACTION / CTA (Detik Terakhir)
            - Skrip Penutup & Teks Keranjang Kuning: 

            4. TEKNIS PENDUKUNG ALGORITMA
            - Rekomendasi Musik/Sound: 
            - Caption Singkat: 
            - 5 Hashtag FYP: 
            """
            
            with st.spinner("AI sedang merancang naskah dan konsep visual..."):
                response = model.generate_content(prompt)
                st.success("Berhasil Membuat Konten!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")