import streamlit as st
import requests
import urllib.parse


st.title("Log In")

st.markdown("In order to access the rest of the application, you first need to authenticate yourself as an active HoYoWiki collaborator.")

with st.expander("How to Use"):
    st.markdown("""
    1. Click on the `Authenticate with Discord` button
    2. When prompted, authorize **HSR-Exchange** to access your Discord username as well as see what servers you are in (to check if you are in the HoYoWiki collaborator server)
    
    **NB:** You will need to repeat this process every time you want to access the application. Additionally, you may freely deauthorize **HSR-Exchange** (under the `Authorized Apps` Discord settings) at any time without losing any data.
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

is_authenticating = "code" in st.query_params

st.link_button("Authenticate with Discord", auth_url, type = "primary", icon = ":material/open_in_new:", disabled = is_authenticating)

if is_authenticating:
    st.toast("Verifying identity...", icon = ":material/frame_person:")

    authorization_code = st.query_params["code"]
    st.query_params.clear()

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
        st.session_state["discord_id"] = res_user_json["id"]
        st.session_state["discord_name"] = res_user_json["username"]
        
        st.rerun()
    else:
        st.error("Authentication failed. You must be part of the HoYoWiki collaborator server to use this app.", icon = ":material/person_cancel:")