import streamlit as st


st.title("Welcome to HSR-Exchange-β!")

st.markdown("""
    Here you will be able to select items for our exchange event and manage your order, all in one place!

    All the necessary tools can be accessed from the sidebar at the left of this page.
""")

st.divider()

st.markdown("""
**:material/priority_high: IMPORTANT INFORMATION :material/priority_high:**

This year, there are **two currencies** you can use to redeem items: Special Attendance Points (**SP**), distributed automatically based on member activity, and Reward Pool Points (**RP**), obtained as usual.

Each currency system is handled through its own website with its own redeemable items. **SP** can be exchanged on HSR-Exchange-α, while **RP** can be exchanged on HSR-Exchange-β.

You can view your respective balance by entering your HoYoLAB ID on the `My Order` page after logging in.

:material/arrow_forward: You are currently on **HSR-Exchange-β**. To access HSR-Exchange-α, [click here](https://hsr-exchange-alpha.streamlit.app/).
""")

st.divider()

with st.expander("Browser Compatibility :material/warning:", width = "stretch"):
    st.markdown("""
        One of this program's components only guarantees support for recent versions of the following web browsers:
        * Google Chrome
        * Firefox
        * Microsoft Edge
        * Safari

        Compatibility with unsupported browsers or old versions of the above browsers is not guaranteed.
    """)

if st.session_state["discord_id"]:
    st.success(
        "Successfully logged in as **%s**. You may now close the other Streamlit tab in your web browser." % st.session_state["discord_name"],
        icon = ":material/person_check:"
    )