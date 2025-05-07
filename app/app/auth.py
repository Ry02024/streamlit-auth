# app/auth.py
import streamlit as st
import streamlit_authenticator as stauth
import os

def get_allowed_emails_list():
    """環境変数から許可されたメールアドレスのリストを取得する"""
    allowed_emails_str = os.getenv("ALLOWED_USERS_EMAILS", "")
    return [email.strip() for email in allowed_emails_str.split(',') if email.strip()]

def get_authenticator_and_login():
    """streamlit-authenticatorを設定し、認証オブジェクトとログインウィジェットを表示する"""
    allowed_emails_list = get_allowed_emails_list()

    auth_config = {
        'credentials': {
            'usernames': {}, # Google OAuthのみ使用するため空
            'cookie': {
                'expiry_days': int(os.getenv("AUTH_COOKIE_EXPIRY_DAYS", "7")),
                'key': os.getenv("AUTH_COOKIE_KEY", "default_cookie_key_phase1"), # Codespaces Secretで設定
                'name': os.getenv("AUTH_COOKIE_NAME", "google_auth_cookie_phase1")
            },
            'preauthorized': {
                'emails': allowed_emails_list # Codespaces Secretで設定した許可メールリスト
            }
        },
        'oauth': {
            'google': {
                'client_id': os.getenv("GOOGLE_OAUTH_CLIENT_ID"), # Codespaces Secretで設定
                'client_secret': os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"), # Codespaces Secretで設定
                # 'redirect_uri' は指定せず、streamlit-authenticator に自動解決させるか、
                # Google Cloud Console 側の設定を優先する。
                # Codespacesの転送URLをGCPコンソールに登録することが重要。
            }
        }
    }

    authenticator = stauth.Authenticate(
        config=auth_config['credentials'],
        oauth_config=auth_config['oauth'],
        cookie_name=auth_config['credentials']['cookie']['name'],
        key=auth_config['credentials']['cookie']['key'],
        cookie_expiry_days=auth_config['credentials']['cookie']['expiry_days']
    )

    # ログインウィジェットを表示
    login_widget = stauth.Login(authenticator=authenticator, location="main", oauth_providers=['google'])
    login_widget.build_login_widget()

    user_info = {
        "name": st.session_state.get("name"),
        "email": st.session_state.get("email"),
        # uidはFirebase連携時に重要になるが、ここではemailを代用しておく
        "uid": st.session_state.get("uid", st.session_state.get("email"))
    }
    return authenticator, user_info

def display_logout_button(authenticator):
    """ログアウトボタンをサイドバーに表示する"""
    authenticator.logout("🔒 ログアウト", "sidebar", key='logout_button_phase1')
