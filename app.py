import streamlit as st
import numpy as np
import joblib
import json

# Fungsi Navigasi
def go_to_predict():
    st.session_state.navigasi = "🔬 Prediksi Tanaman"

def go_to_home():
    st.session_state.navigasi = "🏠 Halaman Utama"

# Fungsi Validasi Input
def validate_input(n, p, k, temp, humidity, ph):
    """Memvalidasi input pengguna agar berada dalam rentang yang wajar."""
    warnings = []
    if n < 10 and n != 0: warnings.append("Nilai Nitrogen (N) terlihat sangat rendah dan tidak realistis.")
    if p < 10 and p != 0: warnings.append("Nilai Fosfor (P) terlihat sangat rendah dan tidak realistis.")
    if k < 10 and k != 0: warnings.append("Nilai Kalium (K) terlihat sangat rendah dan tidak realistis.")
    if not (10 <= temp <= 45): warnings.append(f"Suhu ({temp}°C) berada di luar rentang wajar untuk pertanian (10-45°C).")
    if not (20 <= humidity <= 100): warnings.append(f"Kelembapan ({humidity}%) berada di luar rentang wajar (20-100%).")
    if not (3.5 <= ph <= 9): warnings.append(f"Nilai pH Tanah ({ph}) berada di luar rentang wajar (3.5-9).")
    return warnings

# Fungsi untuk memuat CSS eksternal
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Fungsi Utama
def main():
    st.set_page_config(
        page_title="🌱 Crop Predictor App",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Load CSS eksternal
    load_css("style.css")

    # Memuat model dan pendukungnya
    try:
        model = joblib.load("best_model_lgbm.pkl")
        scaler = joblib.load("scaler.pkl")
        label_encoder = joblib.load("label_encoder.pkl")
        with open("kategori_tanaman.json", "r") as f:
            kategori_tanaman = json.load(f)
        model_ready = True
    except Exception as e:
        st.error(f"Gagal memuat file model atau pendukungnya: {e}")
        st.warning("Fungsi prediksi tidak akan berjalan. Pastikan file .pkl, .json, dan library yang dibutuhkan (seperti lightgbm) sudah benar.")
        model_ready = False

    # Sidebar Menu
    with st.sidebar:
        st.markdown("### 🎯 Menu")
        page = st.radio(
            "Pilih halaman:",
            ["🏠 Halaman Utama", "🔬 Prediksi Tanaman"],
            key="navigasi"
        )
        st.markdown("---")
        st.info("Aplikasi ini dibuat oleh Rafif Huda untuk memprediksi tanaman yang cocok berdasarkan kondisi tanah.")

    # Halaman Utama
    if page == "🏠 Halaman Utama":
        st.markdown("<h1 class='subtitle'>Sistem Prediksi Tanaman Menggunakan LGBM</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            <div class="info-section">
                <h3>📌 Tentang Sistem</h3>
                <p>Aplikasi ini menggunakan model LightGBM untuk memprediksi jenis tanaman yang sesuai berdasarkan parameter kondisi tanah dan lingkungan.</p>
                <h3>⚙️ Parameter yang Digunakan</h3>
                <p>1. Nitrogen (N)<br>2. Fosfor (P)<br>3. Kalium (K)<br>4. Suhu Udara<br>5. Kelembapan Udara<br>6. pH Tanah</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.button("Mulai Prediksi Sekarang 🚀", on_click=go_to_predict, type="primary")

    # Halaman Prediksi
    elif page == "🔬 Prediksi Tanaman":
        button_cols = st.columns(5)
        with button_cols[0]:
            st.button("⬅️ Kembali", on_click=go_to_home)

        st.markdown("<h1 class='subtitle'>Masukkan Parameter Kondisi Tanah</h1>", unsafe_allow_html=True)

        with st.form("prediction_form"):
            n = st.number_input("Nitrogen (N)", min_value=0.0, max_value=200.0, value=0.0, step=0.1)
            p = st.number_input("Fosfor (P)", min_value=0.0, max_value=200.0, value=0.0, step=0.1)
            k = st.number_input("Kalium (K)", min_value=0.0, max_value=200.0, value=0.0, step=0.1)
            temp = st.number_input("Suhu (°C)", min_value=-10.0, max_value=60.0, value=25.0, step=0.1)
            humidity = st.number_input("Kelembapan (%)", min_value=0.0, max_value=100.0, value=60.0, step=0.1)
            ph = st.number_input("pH Tanah", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
            submitted = st.form_submit_button("🚀 Prediksi Tanaman")

        if submitted:
            validation_warnings = validate_input(n, p, k, temp, humidity, ph)
            if n == 0 or p == 0 or k == 0:
                st.warning("⚠️ Harap isi semua parameter kondisi tanah.")
            elif validation_warnings:
                for w in validation_warnings:
                    st.warning(w)
            elif not model_ready:
                st.error("❌ Model tidak tersedia. Silakan periksa file model.")
            else:
                input_data = np.array([[n, p, k, temp, humidity, ph]])
                input_scaled = scaler.transform(input_data)
                y_pred = model.predict(input_scaled)
                nama_tanaman = label_encoder.inverse_transform(y_pred)[0]
                kategori = kategori_tanaman.get(nama_tanaman, "Tidak diketahui")

                st.markdown(f"""
                <div class="prediction-result">
                    <h2>🌾 Tanaman yang Cocok: {nama_tanaman.capitalize()}</h2>
                    <p>Kategori: {kategori}</p>
                </div>
                """, unsafe_allow_html=True)

                if hasattr(model, "predict_proba"):
                    proba = model.predict_proba(input_scaled)[0]
                    top_idx = np.argsort(proba)[::-1][:3]
                    st.subheader("📊 Top 3 Rekomendasi Tanaman")
                    for idx in top_idx:
                        st.write(f"- {label_encoder.inverse_transform([idx])[0].capitalize()} ({proba[idx]*100:.2f}%)")

if __name__ == "__main__":
    main()
