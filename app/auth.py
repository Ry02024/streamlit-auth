# app/auth.py
import streamlit as st
import streamlit_authenticator as stauth # type: ignore
import os

def get_allowed_emails_list():
    """環境変数から許可されたメールアドレスのリストを取得する"""
    allowed_emails_str = os.getenv("ALLOWED_USERS_EMAILS", "")
    return [email.strip() for email in allowed_emails_str.split(',') if email.strip()]

def get_authenticator_and_login():
    """streamlit-authenticatorを設定し、認証オブジェクトとログインウィジェットを表示する"""
    allowed_emails_list = get_allowed_emails_list()

    cookie_config = {
        'expiry_days': int(os.getenv("AUTH_COOKIE_EXPIRY_DAYS", "7")),
        'key': os.getenv("AUTH_COOKIE_KEY", "default_cookie_key_phase1"),
        'name': os.getenv("AUTH_COOKIE_NAME", "google_auth_cookie_phase1")
    }

    google_oauth_config = {
        'client_id': os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        'client_secret': os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
    }

    # Authenticatorオブジェクトのインスタンス化
    # この初期化方法は前回の KeyError を解消したものです
    authenticator = stauth.Authenticate(
        credentials={'usernames': {}}, # ユーザー名/パスワード認証は使わない
        cookie_name=cookie_config['name'],
        key=cookie_config['key'],
        cookie_expiry_days=cookie_config['expiry_days'],
        preauthorized_emails=allowed_emails_list,
        # Google OAuthの設定
        google_client_id=google_oauth_config['client_id'],
        google_client_secret=google_oauth_config['client_secret'],
        # google_redirect_uri は省略 (GCPコンソール側の設定が主)
        # これにより、authenticator.login() がGoogleログインボタンを表示するはず
    )

    # ログイン処理の呼び出し
    # authenticator.login() は、OAuthプロバイダが設定されていれば、
    # ユーザー名/パスワードフォームの下、または代わりにOAuthボタンを表示します。
    # 戻り値は、ログイン試行が行われた後 (例: フォーム送信、OAuthコールバック後) に意味を持ちます。
    # 初期表示時やOAuthプロセス中は None を返すことがある。

    # --- 修正ポイント ---
    # loginメソッドを呼び出し、その結果をセッションに保存する
    # ただし、loginメソッドがNoneを返す場合があるので、呼び出し方を工夫する。
    # 多くのサンプルでは、loginメソッドはメインのUI描画ループの中で呼び出され、
    # 認証状態 (st.session_state.authentication_status) を更新する。

    # ログインフォーム/ボタンを表示 (ここでOAuthボタンが表示されることを期待)
    authenticator.login(fields={'Form name': 'ログイン'}) # Form name はユーザー名/パスワード用だが、OAuthボタンも表示される

    # name, authentication_status, username は、st.session_state から取得する
    # authenticator.login() は内部で st.session_state.authentication_status などを更新する

    user_info = {
        "name": st.session_state.get("name"),
        "email": st.session_state.get("username"), # OAuthではusernameにemailが入る
        "uid": st.session_state.get("username")    # emailをUIDとして使う
    }
    # authenticator はそのまま返し、認証状態は app.py 側で st.session_state を見て判断する
    return authenticator, user_info


def display_logout_button(authenticator):
    """ログアウトボタンをサイドバーに表示する"""
    authenticator.logout("🔒 ログアウト", "sidebar", key='logout_button_phase1')