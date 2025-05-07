# app.py
import streamlit as st
from app import auth # appパッケージからauthモジュールをインポート

def main():
    st.set_page_config(page_title="Google Auth Only Demo", layout="centered")
    st.title("Google認証システム (フェーズ1)")

    # authenticatorオブジェクトを取得し、ログインUIを表示する
    # get_authenticator_and_login は authenticator.login() を呼び出してUIを描画し、
    # 認証情報を st.session_state に格納する。
    authenticator, user_info_from_auth_module = auth.get_authenticator_and_login() # 修正: user_infoも受け取る

    # 認証状態は st.session_state.authentication_status で確認
    if st.session_state.get("authentication_status"): # Trueなら認証成功
        # user_info_from_auth_module を使うか、再度st.session_stateから取得する
        user_name = st.session_state.get("name")
        user_email = st.session_state.get("username") # authenticatorが設定するキー

        st.sidebar.write(f"ようこそ、**{user_name}** さん") # st.session_state.name を使う
        auth.display_logout_button(authenticator)

        st.header("ログイン成功！")
        st.success(f"Googleアカウント ({user_email}) での認証に成功しました。")
        st.write("次のフェーズでFirestore連携を追加します。")
        st.balloons()

    elif st.session_state.get("authentication_status") is False: # Falseなら認証失敗
        st.error("認証に失敗しました。許可されていないアカウントか、認証情報に問題があります。")
        allowed_emails = auth.get_allowed_emails_list()
        if allowed_emails:
            st.warning(f"許可されたGoogleアカウントでログインしてください。許可リスト: {', '.join(allowed_emails)}")
    elif st.session_state.get("authentication_status") is None: # Noneなら未認証（初期状態またはOAuthプロセス中）
        st.warning("Googleアカウントでログインしてください。")
        # この状態で login() がUI（ユーザー名/パスワードフォームとOAuthボタン）を表示している
        if not auth.get_allowed_emails_list():
             st.caption("注意: 現在、許可ユーザーリストが空です。管理者はCodespaces Secret `ALLOWED_USERS_EMAILS` を設定してください。")

    st.markdown("---")
    st.caption("フェーズ1: Google認証のみ")

if __name__ == "__main__":
    main()