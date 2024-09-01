import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import os

# Download the vader_lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Check if the user is logged in

# Get the username from session state
name = st.session_state.username

# Title of the Journal App
st.title("Journal Saver & Analyzer")

# Selectbox to choose to view a journal or create a new one
view = st.selectbox("View a journal from another day - Y/N:", ["Y", "N"])
view = view.lower()

if view:
    match view:
        case "y":
            try:
                date = st.date_input("Enter date: ")
                with open(f"{name}_{date}.txt", "r") as file:
                    data = file.read()
                    st.text(data)
            except FileNotFoundError:
                st.warning("""
                         This File Does Not Exist!\n
                         Choose a different date instead!
                         """)
        case _:
            date = st.date_input("Enter today's date: ")
            mood = st.number_input("How do you rate your mood today from 1 to 5:", min_value=1, max_value=5, value=5)
            
            thought = st.text_area("Write any other info:\n")
            analyzer = SentimentIntensityAnalyzer()
            with open(f"{name}_{date}.txt", "w") as file:
                match mood:
                    case 1:
                        file.write("Mood - Very Bad! :(\n")
                    case 2:
                        file.write("Mood - Bad :(\n")
                    case 3:
                        file.write("Mood - Neutral :|\n")
                    case 4:
                        file.write("Mood - Good :)\n")
                    case 5:
                        file.write("Mood - Very Good! :)\n")
                    case _:
                        file.write("???\n")

                scores = analyzer.polarity_scores(thought)
                file.write("Other info: " + thought + "\n")
                if scores["pos"] > scores["neg"]:
                    file.write("This text is POSITIVE :)\n")
                elif scores["neu"] == 1.0:
                    file.write("This text is NEUTRAL :|\n")
                else:
                    file.write("This text is NEGATIVE :(\n")

            file.write(str(date))

            if os.path.exists(f"{name}_{date}.txt"):
                with open(f"{name}_{date}.txt", "r") as file:
                    st.text("You Are Editing A Created File")
