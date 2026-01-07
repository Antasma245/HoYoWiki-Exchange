import streamlit as st


if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

home = st.Page(
    "pages/home.py",
    title = "HoYoWiki-Exchange",
    icon = ":material/home:",
    default = True
)

login = st.Page(
    "pages/login.py",
    title = "Log in",
    icon = ":material/login:"
)

logout = st.Page(
    "pages/logout.py",
    title = "Log out",
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
    icon = ":material/orders:"
)

delivery = st.Page(
    "pages/delivery.py",
    title = "Delivery Details",
    icon = ":material/local_shipping:"
)

about = st.Page(
    "pages/about.py",
    title = "About this app",
    icon = ":material/info:"
)

if st.session_state["user_id"]:
    pg = st.navigation(
        {
            "Home": [home],
            "Authentication": [logout],
            "Exchange": [inventory, order, delivery],
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