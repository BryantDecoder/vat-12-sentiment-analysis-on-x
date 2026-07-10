import streamlit as st
from streamlit_option_menu import option_menu

from views.input_text import show_input_text
from views.upload_csv import show_upload_csv
from views.about import show_about
from utils.model import load_model, load_tokenizer
import time

st.set_page_config(
    page_title="Sentiment Analysis App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.logo("assets/logo_icon.png", size="large")

if "model_ready" not in st.session_state:

    placeholder = st.empty()

    with placeholder.container():

        st.title("Vat 12% Sentiment Analysis")

        st.info("Sedang menyiapkan aplikasi...", icon=":material/info:")

        progress = st.progress(0)

        progress.progress(
            25,
            text="Menyiapkan aplikasi..."
        )
        time.sleep(2.0)

        progress.progress(
            50,
            text="Memuat tokenizer..."
        )
        load_tokenizer()
        time.sleep(1.5)

        progress.progress(
            75,
            text="Memuat model..."
        )
        load_model()
        time.sleep(1.5)

        progress.progress(
            100,
            text="Website siap digunakan."
        )
        time.sleep(1.3)

    placeholder.empty()

    st.session_state.model_ready = True

st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* option menu spacing */
.nav-link {
    border-radius: 10px;
    padding: 10px !important;
    margin: 4px !important;
}

/* selected menu */
.nav-link-selected {
    background-color: #111827 !important;
    color: white !important;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

MENU_INPUT = "Input Teks"
MENU_UPLOAD = "Upload Dataset"
MENU_ABOUT = "About"

with st.sidebar:

    st.image(
        "assets/logo.png",
        use_container_width=True
    )

    selected = option_menu(
        menu_title="Main Menu",
        options=[MENU_INPUT, MENU_UPLOAD, MENU_ABOUT],
        icons=["chat-left-text", "cloud-upload", "info-circle"],
        menu_icon="house",
        default_index=0,
        styles={
            "container": {
                "padding": "5px",
                "background-color": "#ffffff"
            },
            "nav-link": {
                "font-size": "18px",
                "text-align": "left"
            }
        }
    )

if selected == MENU_INPUT:
    show_input_text()

elif selected == MENU_UPLOAD:
    show_upload_csv()

elif selected == MENU_ABOUT:
    show_about()