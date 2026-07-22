import streamlit as st
from sqlalchemy import text
import pandas as pd


if "hoyolab_id" not in st.session_state:
    st.session_state["hoyolab_id"] = None

if "comment" not in st.session_state:
    st.session_state["comment"] = None

st.title("My Order")

st.markdown("Enter your personal details, review your order and register it.")

st.divider()

st.subheader("Details")

discord_username = st.text_input("Your Discord username (required)", value = st.session_state["discord_name"], disabled = True)

conn = st.connection("neon", type = "sql")

if st.session_state["hoyolab_id"] is None:
    user_details_df = conn.query("""
            SELECT
                hoyolab_id,
                comment
            FROM orders
            WHERE discord_id = :discord_id;
        """,
        ttl = 0,
        params = {
            "discord_id": st.session_state["discord_id"]
        }
    )

    if not user_details_df.empty:
        st.session_state["hoyolab_id"] = user_details_df.at[0, "hoyolab_id"]
        st.session_state["comment"] = user_details_df.at[0, "comment"]

hoyolab_id = st.text_input("Your HoYoLAB ID (required)", value = st.session_state["hoyolab_id"])

if hoyolab_id:
    st.session_state["hoyolab_id"] = hoyolab_id

comment = st.text_area("Anything to add?", value = st.session_state["comment"])

if comment:
    st.session_state["comment"] = comment

st.subheader("Wishlist")

cart = st.session_state["cart"]

item_ids = [item["id"] for item in cart.values()]
item_names = [item["name"] for item in cart.values()]
item_prices = [item["price"] for item in cart.values()]

cart_display = {
    "ID": item_ids,
    "Name": item_names,
    "Price (RP)": item_prices
}

cart_display_df = pd.DataFrame(cart_display)
cart_display_df.set_index("ID", inplace = True)

st.table(cart_display_df)

balance = 0

if hoyolab_id:
    user_balance_df = conn.query(
        "SELECT balance FROM users WHERE hoyolab_id = :hoyolab_id;",
        ttl = 600,
        params = {
            "hoyolab_id": hoyolab_id
        }
    )

    if not user_balance_df.empty:
        balance = user_balance_df.at[0, "balance"]

total_cost = sum(item_prices)

st.markdown("**Total cost:** %s RP" % total_cost)
st.markdown("**Your points:** %s RP" % balance, help = "Reward Pool Points (RP) based on the provided HoYoLAB ID. If you think the value is not correct, please contact staff.")

register_button_enabled = st.secrets.other["exchange_open"] and balance >= total_cost and hoyolab_id

if st.button("Register Order", type = "primary", disabled = not register_button_enabled):
    st.toast("Processing order...", icon = ":material/order_play:")

    with conn.session as s:
        order_id = s.execute(
            text("""
                INSERT INTO orders (discord_id, hoyolab_id, comment)
                VALUES (:discord_id, :hoyolab_id, :comment)
                ON CONFLICT (discord_id)
                DO UPDATE SET
                    hoyolab_id = EXCLUDED.hoyolab_id,
                    comment = EXCLUDED.comment
                RETURNING id
            """),
            params = {
                "discord_id": st.session_state["discord_id"],
                "hoyolab_id": hoyolab_id,
                "comment": comment
            }
        ).scalar()

        s.execute(
            text("DELETE FROM order_items WHERE order_id = :oid"),
            params = {
                "oid": order_id
            }
        )

        for id in item_ids:
            s.execute(
                text("""
                    INSERT INTO order_items (order_id, item_id)
                    VALUES (:oid, :iid)
                """),
                params = {
                    "oid": order_id,
                    "iid": id,
                }
            )
        
        s.commit()

    st.success("Order registered. You may edit it anytime within the exchange period by adding/removing items from your cart and clicking the button again.", icon = ":material/inventory:")