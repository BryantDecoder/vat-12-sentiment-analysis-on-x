import streamlit as st


def developer_card(image_path, name, nim):
    with st.container(border=True):

        left, center, right = st.columns([1, 1, 1])

        with center:
            st.image(image_path, width=200)

        st.markdown(f"### {name}", text_alignment="center")
        st.markdown(f"#### NIM.{nim}", text_alignment="center")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
        - **Semester VIII**
        - **Teknik Informatika**
        """)

        with col2:
            st.markdown("""
        - **Fakultas Informatika**
        - **Universitas Mikroskil**
        """)

def show_about():

    st.title("About Us")

    st.write(
        """
        Website ini dikembangkan sebagai implementasi penelitian **Analisis Sentimen
        Publik terhadap Kebijakan PPN 12% pada Media Sosial X menggunakan
        model IndoBERT-BiLSTM**.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        developer_card(
            "assets/bry.jpg",
            "Bryant Alfronso Purba",
            "221113288"
        )

    with col2:
        developer_card(
            "assets/roy.jpg",
            "Roy Jannes Simbolon",
            "221113506"
        )

    with col3:
        developer_card(
            "assets/sam.jpg",
            "Samuel Natalino Sitorus",
            "221111771"
        )

    st.divider()

    st.subheader("Project Information")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Model", "IndoBERT-BiLSTM")

        st.metric("Framework", "Streamlit")

    with col2:
        st.metric("Programming Language", "Python")

        st.metric("Classification", "3 Sentiment Classes")

    st.divider()

    st.caption(
        "© 2026 VAT 12% Sentiment Analysis | "
        "Faculty of Informatics | Universitas Mikroskil"
    )