import streamlit as st
import pandas as pd

# Load the login data from the CSV file
def load_login_data(file_path):
    try:
        login_data = pd.read_csv(file_path)
        return login_data
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "password"])

# Main app logic
def main():
    st.title("Login Form")

    # Path to the logins CSV file
    login_file_path = 'logins.csv'

    # Load login data
    login_data = load_login_data(login_file_path)

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None

    if not st.session_state.logged_in:
        with st.form(key="login_form"):
            name = st.text_input("What Is Your user_name", help="We need this to access your files. Make sure you save your files on this name and use this name to access your files. You can include numbers, etc for more safety.")
            password = st.text_input("Your password.", type="password")
            button = st.form_submit_button("Login")

            if button:
                if not login_data[(login_data['username'] == name) & (login_data['password'] == password)].empty:
                    st.session_state.logged_in = True
                    st.session_state.username = name
                    st.success("Login successful! You can now use the Journal App.")
                else:
                    st.error("Username or password is incorrect.")

    if st.session_state.logged_in:
        st.info(f"Logged in as {st.session_state.username}")

        st.markdown("Journal App [link](%s)" % "https://journalsaver.streamlit.app")

    st.markdown("[Don't have an account? Sign up here](#)")  # Placeholder link

if __name__ == "__main__":
    main()
