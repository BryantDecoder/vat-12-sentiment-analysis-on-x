import streamlit as st
from utils.model import predict
import time

def show_input_text():

    st.title("Analisis Sentimen (3 Kategori)")

    text = st.text_area("Masukkan teks")

    if st.button("Analisis"):
        if text.strip():

            with st.status("Sedang menganalisis...", expanded=True) as status:
                st.write("Teks sedang diproses...")
                sentiment, conf, probs = predict(text)
                st.write("Teks sedang diprediksi...")
                time.sleep(2.5)
                st.write("Menampilkan hasil...")
                time.sleep(2.5)
                status.update(label="Prediksi selesai!", state="complete", expanded=False)

            col1, col2 = st.columns(2)

            col1.metric("Confidence Value", f"{conf*100:.1f}%", border=True, help="Nilai seberapa yakin model dalam memprediksi")
            col2.metric("Sentiment Category", sentiment.upper(), border=True, help="Hasil prediksi dari model")

            st.write(" Nilai Probabilitas 3 Kelas:")
            st.write({
                "Negatif": float(probs[0][0]),
                "Netral": float(probs[0][1]),
                "Positif": float(probs[0][2])
            })

        else:
            st.warning("Teks tidak boleh kosong", icon=":material/warning:")