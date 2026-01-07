import streamlit as st
import requests
import time
import urllib.parse


st.title("Log In")

st.markdown("In order to access the rest of the application, you first need to authenticate yourself as an active HoYoWiki collaborator.")

with st.expander("How to Use"):
    st.markdown("""
    1. Click on the `Authenticate with Discord` button
    2. When prompted, authorize **HoYoWiki-Exchange** to access your Discord username as well as see what servers you are in (to check if you are in the HoYoWiki collaborator server)
    
    **NB:** You will need to repeat this process every time you want to access the application. Additionally, you may freely deauthorize **HoYoWiki-Exchange** (under the `Authorized Apps` Discord settings) at any time without losing any data.
    """)

st.divider()

auth_url = (
    "https://discord.com/api/oauth2/authorize?" +
    urllib.parse.urlencode(
        {
            "client_id": st.secrets.discord["client_id"],
            "redirect_uri": st.secrets.discord["redirect_uri"],
            "response_type": "code",
            "scope": "identify guilds",
        }
    )
)

st.link_button("Authenticate with Discord", auth_url, type = "primary", icon = ":material/open_in_new:")

if "code" in st.query_params:
    st.toast("Verifying identity...", icon = ":material/frame_person:")

    authorization_code = st.query_params["code"]

    request_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": st.secrets.discord["redirect_uri"],
    }

    request_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    request_auth = (st.secrets.discord["client_id"], st.secrets.discord["client_secret"])

    res_token = requests.post(
        "https://discord.com/api/oauth2/token",
        data = request_data,
        headers = request_headers,
        auth = request_auth
    )

    res_token.raise_for_status()
    res_token_json = res_token.json()

    token_headers = {
        "Authorization": "Bearer %s" % res_token_json["access_token"]
    }

    res_user = requests.get(
        "https://discord.com/api/users/@me",
        headers = token_headers
    )

    res_user.raise_for_status()
    res_user_json = res_user.json()

    res_guilds = requests.get(
        "https://discord.com/api/users/@me/guilds",
        headers = token_headers
    )

    res_guilds.raise_for_status()
    res_guilds_json = res_guilds.json()

    in_wiki_guild = any(guild["id"] == st.secrets.discord["wiki_guild_id"] for guild in res_guilds_json)

    if in_wiki_guild:
        st.session_state["user_id"] = res_user_json["id"]

        user_alias = res_user_json["global_name"] or res_user_json["username"]

        st.success("Authentication successful. Logging you in as **%s**..." % user_alias, icon = ":material/person_check:")
        
        time.sleep(5)

        st.rerun()
    else:
        st.error("Authentication failed. You must be part of the HoYoWiki collaborator server to use this app.", icon = ":material/person_cancel:")