import streamlit as st
import pandas as pd
from send_emaill import send_email

# Load the login data from the CSV file
def load_login_data(file_path):
    try:
        login_data = pd.read_csv(file_path)
        return login_data
    except FileNotFoundError:
        return pd.DataFrame(columns=["username", "password"])

# Save the login data to the CSV file
def save_login_data(file_path, login_data):
    login_data.to_csv(file_path, index=False)

# Check if username already exists
def username_exists(username, login_data):
    return not login_data[login_data['username'] == username].empty

# Main app logic
def main():
    st.title("Signup Form")

    # Path to the logins CSV file
    login_file_path = 'logins.csv'

    # Load login data
    login_data = load_login_data(login_file_path)

    if 'correct_code' not in st.session_state:
        st.session_state.correct_code = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'password' not in st.session_state:
        st.session_state.password = None
    if 'email' not in st.session_state:
        st.session_state.email = None

    with st.form(key="signup_form"):
        name = st.text_input("Make a username", help="We need this to access your files. Make sure you save your files on this name and use this name to access your files. You can include numbers, etc for more safety.")
        password = st.text_input("Make a password.", type="password")
        email = st.text_input("What is your email", placeholder="user@example.com")
        button = st.form_submit_button("Sign Up!")

        if button:
            if len(password) < 6 or not any(char.isdigit() for char in name):
                st.warning("Password must be at least 6 characters and username must contain at least one number.")
            elif username_exists(name, login_data):
                st.warning("Username already exists. Please choose a different username.")
            else:
                correct_code = send_email(email)
                st.session_state.correct_code = correct_code
                st.session_state.username = name
                st.session_state.password = password
                st.session_state.email = email
                st.info("Please check your inbox. We have sent you an 8-digit code.")

    if st.session_state.correct_code:
        with st.form(key="verify_form"):
            code = st.text_input("Your Code", max_chars=8)
            verify_button = st.form_submit_button("Verify")
            
            if verify_button:
                if code == st.session_state.correct_code:
                    # Add the new user to the login data
                    new_user = pd.DataFrame([[st.session_state.username, st.session_state.password]], columns=["username", "password"])
                    login_data = pd.concat([login_data, new_user], ignore_index=True)
                    
                    # Save the updated login data
                    save_login_data(login_file_path, login_data)
                    
                    st.success("Signup successful! You can now log in.")
                    # Reset session state
                    st.session_state.correct_code = None
                    st.session_state.username = None
                    st.session_state.password = None
                    st.session_state.email = None
                else:
                    st.warning("Incorrect code!")

if __name__ == "__main__":
    main()
