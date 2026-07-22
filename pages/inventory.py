import streamlit as st
from io import BytesIO
import pandas as pd
from PIL import Image
import re


def extract_drive_id(url: str) -> str:
    pattern = r"(?:/d/|id=)([a-zA-Z0-9_-]+)"
    match = re.search(pattern, url)

    return match[1]


get_gdrive_image = st.session_state["get_image_func"]


def build_item_selector(items: pd.DataFrame) -> None:
    item_columns = st.columns(4, vertical_alignment = "bottom")

    for position, (_, item) in enumerate(items.iterrows()):
        if position % 4 == 0 and position > 0:
            item_columns = st.columns(4, vertical_alignment = "bottom")

        with item_columns[position % 4]:
            image_id = extract_drive_id(item["image_url"])
            image_bytes = get_gdrive_image(image_id)

            st.image(Image.open(BytesIO(image_bytes)))
            
            st.markdown("\u3010%s\u3011%s" % (item["id"], item["name"]), text_alignment = "center")
            st.markdown("**Price:** %s RP" % item["price"], text_alignment = "center")
            st.markdown("**Total stock:** %s" % item["stock"], help = "**%s** people interested" % item["interested_users"], text_alignment = "center")

            button_columns = st.columns(2)

            item_in_cart = item["id"] in st.session_state["cart"]

            with button_columns[0]:
                if st.button(":material/remove_shopping_cart:", help = "Remove from cart", disabled = not item_in_cart, use_container_width = True, key = "remove_%s" % item["id"]):
                    st.session_state["cart"].pop(item["id"])

                    st.rerun()
            
            with button_columns[1]:
                if st.button(":material/add_shopping_cart:", help = "Add to cart", disabled = item_in_cart, use_container_width = True, key = "add_%s" % item["id"]):
                    st.session_state["cart"].update({item["id"]: item})

                    st.rerun()

            st.space("small")


st.title("Inventory")

st.markdown("View the items available for exchange and add them to your cart. You can also see how many people are interested in each item (if the number is higher than the total stock, the item will be subject to raffle).")

st.divider()

conn = st.connection("neon", type = "sql")

items_df = conn.query("""
        SELECT
            i.*,
            COUNT(oi.item_id) AS interested_users
        FROM items i
        LEFT JOIN order_items oi ON oi.item_id = i.id
        GROUP BY i.id;
    """,
    ttl = 600
)

categories = {
    "Genshin Impact": "GI",
    "Honkai Impact 3rd": "HI3",
    "Honkai Star Rail": "HSR",
    "Zenless Zone Zero": "ZZZ"
}

tabs = st.tabs(list(categories.keys()))

for tab, category in zip(tabs, categories.values()):
    with tab:
        category_items = items_df[items_df["category"] == category]

        category_items_sorted = category_items.sort_values(
            by = "id",
            key = lambda id_series: id_series.str.extract(r"(\d+)").astype(int)[0]
        )

        build_item_selector(category_items_sorted)