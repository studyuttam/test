import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ["LMUStaff", "NYTStaff"]
usernames = ["lmu", "nyt"]
passwords = ["lmu@123", "nyt@123"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as f:
    pickle.dump(hashed_passwords, f)