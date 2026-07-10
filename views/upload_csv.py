import streamlit as st
import pandas as pd
import plotly.express as px
from utils.model import predict
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

REQUIRED_COLUMN = "text"

st.markdown("""
<style>

/* METRIC STYLE */
[data-testid="stMetric"] {
    background-color: #f9f9f9;
    border-radius: 12px;
    padding: 15px;
}

/* CONTAINER STYLE */
[data-testid="stContainer"] {
    border-radius: 16px;
}

/* GLOBAL SPACING */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

def generate_advanced_insight(df):
    total = len(df)

    pos = (df["sentiment"]=="positif").sum()
    neg = (df["sentiment"]=="negatif").sum()
    neu = (df["sentiment"]=="netral").sum()

    pos_pct = pos/total
    neg_pct = neg/total
    neu_pct = neu/total

    avg_conf = df["confidence"].mean()

    return f"""
Jumlah distribusi sentimen untuk sentimen positif adalah ({pos_pct:.1%}), 
diikuti negatif sebesar ({neg_pct:.1%}) dan netral sebanyak ({neu_pct:.1%}). 

Rata-rata confidence model sebesar {avg_conf:.2f}.
"""

def show_upload_csv():

    st.title("Upload CSV")

    file = st.file_uploader("Upload file CSV", type=["csv"])
    st.info("Kolom 'text' *WAJIB ADA*, kolom 'created_at' _opsional_", icon=":material/info:")

    if file:
        df = pd.read_csv(file)

        if REQUIRED_COLUMN not in df.columns:
            st.error("Kolom 'text' wajib ada", icon=":material/error:")
        else:
            st.success("Dataset valid", icon=":material/verified:")

            with st.container(border=True):
                st.subheader("Preview Data")
                st.dataframe(df.head(10), use_container_width=True)

            if st.button("Run AI Model", icon_position="right", icon=":material/network_intelligence:"):

                with st.spinner("Dataset diproses & diprediksi... (lama waktu berdasarkan jumlah dataset)"):
                    before = len(df)

                    df[REQUIRED_COLUMN] = df[REQUIRED_COLUMN].fillna("").astype(str)
                    df = df[df[REQUIRED_COLUMN].str.strip() != ""]

                    after = len(df)

                    if before != after:
                        st.warning(f"{before - after} data kosong dihapus sebelum analisis", icon=":material/data_alert:")

                    results = df[REQUIRED_COLUMN].apply(predict)
                    df["sentiment"] = results.apply(lambda x: x[0])
                    df["confidence"] = results.apply(lambda x: x[1])
                    st.session_state["df_result"] = df

                total = len(df)
                pos = (df["sentiment"]=="positif").sum()
                neg = (df["sentiment"]=="negatif").sum()
                neu = (df["sentiment"]=="netral").sum()

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(label="Total Data :material/functions:", value=total, border=True)

                with col2:
                    st.metric(label="Positif :material/sentiment_satisfied:", value=pos, border=True)

                with col3:
                    st.metric(label="Negatif :material/sentiment_dissatisfied:", value=neg, border=True)

                with col4:
                    st.metric(label="Netral :material/sentiment_neutral:", value=neu, border=True)

                with st.container(border=True):
                    st.info(generate_advanced_insight(df), icon=":material/info:")

                with st.container(border=True):
                    st.subheader("Hasil Analisis Sentimen")
                    st.dataframe(df, use_container_width=True)

                csv_data = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="hasil_sentimen.csv",
                    mime="text/csv", 
                    icon=":material/download:"
                )

                # if st.button("Search Insights", icon_position="right", icon=":material/search_insights:"):

                color_map = {
                    "positif": "#22c55e",
                    "negatif": "#ef4444",
                    "netral": "#eab308"
                }

                sentiment_count = df["sentiment"].value_counts().reset_index()
                sentiment_count.columns = ["sentiment", "count"]

                st.markdown("### :material/search_insights: Insight & Visualization")

                col1, col2, col3 = st.columns(3)

                with col1:
                    with st.container(border=True):
                        st.subheader("Distribusi Sentimen")
                        fig1 = px.pie(
                            sentiment_count,
                            names="sentiment",
                            values="count",
                            hole=0.6,
                            color="sentiment",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                with col2:
                    with st.container(border=True):
                        st.subheader("Perbandingan Sentimen")
                        fig2 = px.bar(
                            sentiment_count,
                            x="sentiment",
                            y="count",
                            color="sentiment",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                with col3:
                    with st.container(border=True):
                        st.subheader("Distribusi Confidence")
                        fig3 = px.histogram(
                            df,
                            x="confidence",
                            color="sentiment",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig3, use_container_width=True)

                col4, col5, col6 = st.columns(3)

                with col4:
                    with st.container(border=True):
                        st.subheader("Scatter Confidence")
                        df["index"] = range(len(df))
                        fig4 = px.scatter(
                            df,
                            x="index",
                            y="confidence",
                            color="sentiment",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig4, use_container_width=True)

                with col5:
                    with st.container(border=True):
                        st.subheader("Boxplot Confidence")
                        fig5 = px.box(
                            df,
                            x="sentiment",
                            y="confidence",
                            color="sentiment",
                            color_discrete_map=color_map
                        )
                        st.plotly_chart(fig5, use_container_width=True)

                with col6:
                    with st.container(border=True):
                        st.subheader("Trend Sentimen (Time Series)")

                        if "created_at" in df.columns:

                            df["created_at"] = pd.to_datetime(df["created_at"], utc=True, errors="coerce")
                            df["date"] = df["created_at"].dt.date

                            trend = df.groupby(["date", "sentiment"]).size().reset_index(name="count")

                            fig = px.line(
                                trend,
                                x="date",
                                y="count",
                                color="sentiment",
                                markers=True,
                                color_discrete_map={
                                    "positif": "#22c55e",
                                    "negatif": "#ef4444",
                                    "netral": "#eab308"
                                }
                            )

                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Kolom created_at tidak tersedia")

                col7, col8, col9 = st.columns(3)

                with col7:
                    with st.container(border=True):
                        st.subheader("Positif")

                        text_pos = " ".join(df[df["sentiment"] == "positif"]["text"])
                        words_pos = text_pos.split()

                        wc = WordCloud(background_color="white", colormap="Greens").generate(text_pos)

                        fig, ax = plt.subplots()
                        ax.imshow(wc)
                        ax.axis("off")
                        st.pyplot(fig)

                        top_pos = Counter(words_pos).most_common(3)

                        st.markdown("**Top 3 Keywords:**")
                        st.markdown(
                            f"""
                1. {top_pos[0][0] if len(top_pos) > 0 else '-'}  
                2. {top_pos[1][0] if len(top_pos) > 1 else '-'}  
                3. {top_pos[2][0] if len(top_pos) > 2 else '-'}  
                            """
                        )

                with col8:
                    with st.container(border=True):
                        st.subheader("Negatif")

                        text_neg = " ".join(df[df["sentiment"] == "negatif"]["text"])
                        words_neg = text_neg.split()

                        wc = WordCloud(background_color="white", colormap="Reds").generate(text_neg)

                        fig, ax = plt.subplots()
                        ax.imshow(wc)
                        ax.axis("off")
                        st.pyplot(fig)

                        top_neg = Counter(words_neg).most_common(3)

                        st.markdown("**Top 3 Keywords:**")
                        st.markdown(
                            f"""
                1. {top_neg[0][0] if len(top_neg) > 0 else '-'}  
                2. {top_neg[1][0] if len(top_neg) > 1 else '-'}  
                3. {top_neg[2][0] if len(top_neg) > 2 else '-'}  
                            """
                        )

                with col9:
                    with st.container(border=True):
                        st.subheader("Netral")

                        text_neu = " ".join(df[df["sentiment"] == "netral"]["text"])
                        words_neu = text_neu.split()

                        wc = WordCloud(background_color="white", colormap="Wistia").generate(text_neu)

                        fig, ax = plt.subplots()
                        ax.imshow(wc)
                        ax.axis("off")
                        st.pyplot(fig)

                        top_neu = Counter(words_neu).most_common(3)

                        st.markdown("**Top 3 Keywords:**")
                        st.markdown(
                            f"""
                1. {top_neu[0][0] if len(top_neu) > 0 else '-'}  
                2. {top_neu[1][0] if len(top_neu) > 1 else '-'}  
                3. {top_neu[2][0] if len(top_neu) > 2 else '-'}  
                            """
                        )

                with st.container(border=True):
                    st.subheader("Top Words")

                    words = " ".join(df["text"]).split()
                    freq = Counter(words).most_common(10)

                    words_df = pd.DataFrame(freq, columns=["word", "count"])

                    fig = px.bar(words_df, x="word", y="count")
                    st.plotly_chart(fig, use_container_width=True)