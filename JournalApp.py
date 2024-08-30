import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import streamlit as st
import os
import random

nltk.download('vader_lexicon')
st.title("Journal Saver & Anylayser")
name = st.text_input("What Is Your Name", help= "We need this to access your files.")
view = st.selectbox("View a journal from another day - Y/N:", ["Y", "N"])
view = view.lower()
if view and name:
    match view:
        case "y":
            try:
                date = st.date_input("Enter date: ")
                with open(f"{name}{date}.txt", "r") as file:
                    data = file.read()
                    st.text(data)
            except:
                st.warning("""
                         This File Does Not Exist!\n
                         Choose a different date instead!
                         """)
        case x:
            date = st.date_input("Enter today's date: ")
            mood = st.number_input("How do you rate your mood today from 1 to 5:", min_value = 1, max_value = 5, value = 5)
            
            thought = st.text_area("Write any other info:\n")
            analyzer = SentimentIntensityAnalyzer()
            with open(f"{name}{date}.txt", "w") as file:
            
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
                    case x:
                        file.write("???\n")

                scores = analyzer.polarity_scores(thought)
                file.write("Other info: " + thought + "\n")
                if scores["pos"] > scores["neg"]:
                    file.write("This text is POSITIVE :)\n")
                elif scores["neu"] == 1.0:
                    file.write("This text is NUETRAL :|\n")
                else:
                    file.write("This text is NEGATIVE :(\n")

            
                file.write(str(date))

                if os.path.exists(f"{name}{date}.txt"):
                    with open(f"{name}{date}.txt", "r") as file:
                        st.text("You Are Editing A Created File")