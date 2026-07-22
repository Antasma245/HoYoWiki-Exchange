import streamlit as st
import requests


@st.cache_resource
def get_gdrive_image(file_id: str) -> bytes:
    file_url = "https://drive.google.com/uc?id=%s" % file_id

    file_response = requests.get(file_url)
    file_response.raise_for_status()

    return file_response.content


if "discord_id" not in st.session_state:
    st.session_state["discord_id"] = None

if "cart" not in st.session_state:
    st.session_state["cart"] = {}

if "get_image_func" not in st.session_state:
    st.session_state["get_image_func"] = get_gdrive_image

home = st.Page(
    "pages/home.py",
    title = "HoYoWiki-Exchange",
    icon = ":material/home:",
    default = True
)

login = st.Page(
    "pages/login.py",
    title = "Log In",
    icon = ":material/login:"
)

logout = st.Page(
    "pages/logout.py",
    title = "Log Out",
    icon = ":material/logout:"
)

inventory = st.Page(
    "pages/inventory.py",
    title = "Inventory",
    icon = ":material/inventory_2:"
)

order = st.Page(
    "pages/order.py",
    title = "My Order",
    icon = ":material/shopping_cart:"
)

about = st.Page(
    "pages/about.py",
    title = "About this app",
    icon = ":material/info:"
)

if st.session_state["discord_id"]:
    if len(st.session_state["cart"]) == 0:
        conn = st.connection("neon", type = "sql")

        cart_items_df = conn.query("""
                SELECT
                    i.*
                FROM orders o
                JOIN order_items oi ON oi.order_id = o.id
                JOIN items i ON i.id = oi.item_id
                WHERE o.discord_id = :discord_id;
            """,
            ttl = 0,
            params = {
                "discord_id": st.session_state["discord_id"]
            }
        )

        for _, item in cart_items_df.iterrows():
            st.session_state["cart"].update({item["id"]: item})
    
    pg = st.navigation(
        {
            "Home": [home],
            "Authentication": [logout],
            "Exchange": [inventory, order],
            "Information": [about]
        }
    )
else:
    pg = st.navigation(
        {
            "Home": [home],
            "Authentication": [login],
            "Information": [about]
        }
    )

pg.run()