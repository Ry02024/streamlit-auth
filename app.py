# app.py
import streamlit as st
from app import auth # appパッケージからauthモジュールをインポート

def main():
    st.set_page_config(page_title="Google Auth Only Demo", layout="centered")
    st.title("Google認証システム (フェーズ1)")

    # 認証オブジェクトの取得とログインウィジェットの表示
    authenticator, user_info = auth.get_authenticator_and_login()

    # 認証状態に応じた処理
    if st.session_state.get("authentication_status"):
        st.sidebar.write(f"ようこそ、**{user_info.get('name')}** さん")
        auth.display_logout_button(authenticator)

        st.header("ログイン成功！")
        st.success(f"Googleアカウント ({user_info.get('email')}) での認証に成功しました。")
        st.write("次のフェーズでFirestore連携を追加します。")
        st.balloons()

    elif st.session_state.get("authentication_status") is False:
        st.error("認証に失敗しました。許可されていないアカウントか、認証情報に問題があります。")
        allowed_emails = auth.get_allowed_emails_list()
        if allowed_emails:
            st.warning(f"許可されたGoogleアカウントでログインしてください。許可リスト: {', '.join(allowed_emails)}")
    elif st.session_state.get("authentication_status") is None:
        st.warning("Googleアカウントでログインしてください。")
        if not auth.get_allowed_emails_list():
             st.caption("注意: 現在、許可ユーザーリストが空です。管理者はCodespaces Secret `ALLOWED_USERS_EMAILS` を設定してください。")

    st.markdown("---")
    st.caption("フェーズ1: Google認証のみ")

if __name__ == "__main__":
    main()
