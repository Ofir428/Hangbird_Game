import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# Load JSON files and extract game data
data_rows = []
for file in os.listdir(r"C:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird_Game\data"):
    if file.endswith(".json"):
        with open(os.path.join(r"C:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird_Game\data", file), "r") as f:
            j = json.load(f)
            
            dataset = {}
            
            # Extract basic game info: word, event type, and word length
            word = j["the_word"]
            event = j["event_type"]
            length = str(len(word))
            
            dataset["word"] = word
            dataset["event"] = event
            dataset["length"] = length
            
            # Check for rare letters (J, Q, X, Z) individually
            rare_letters = ["J", "Q", "X", "Z"]
            for rare_letter in rare_letters:
                dataset[f"has_{rare_letter}"] = rare_letter in word
            
            # Check if word contains ANY rare letter
            has_rare_letter = any(letter in word for letter in rare_letters)
            dataset["has_rare_letter"] = has_rare_letter
            
            # Check if word has NO vowels
            vowels = ["A", "E", "I", "O", "U"]
            doesnt_have_vowel = all(vowel not in word for vowel in vowels)
            dataset["doesnt_have_vowel"] = doesnt_have_vowel
            
            data_rows.append(dataset)

# Convert to DataFrame for analysis
df = pd.DataFrame(data_rows)

# Calculate win rate by word length
wins = df[df.event == "player_win"].groupby("length").size()
totals = df.groupby("length").size()
win_rates_length = (wins / totals).fillna(0)

# Calculate win rate by letter/word characteristics
win_rates_letter = {}

for letter in rare_letters:
    wins = df[(df.event == "player_win") & (df[f"has_{letter}"] == True)].shape[0]
    totals = df[df[f"has_{letter}"] == True].shape[0]
    win_rates_letter[letter] = (wins / totals) if totals > 0 else 0

wins = df[(df.event == "player_win") & (df["has_rare_letter"] == True)].shape[0]
totals = df[df["has_rare_letter"] == True].shape[0]
win_rates_letter["has_rare_letter"] = (wins / totals) if totals > 0 else 0

wins = df[(df.event == "player_win") & (df["doesnt_have_vowel"] == True)].shape[0]
totals = df[df["doesnt_have_vowel"] == True].shape[0]
win_rates_letter["doesnt_have_vowel"] = (wins / totals) if totals > 0 else 0

# Visualize win rate vs word length
print(win_rates_length)
plt.bar(win_rates_length.index, win_rates_length.values * 100)
plt.xlabel("Word Length")
plt.ylabel("Win Rate (%)")
plt.title("Win Rate vs Word Length")
plt.show()

# Visualize win rate by letter characteristics
print(win_rates_letter)
plt.bar(win_rates_letter.keys(), [v*100 for v in win_rates_letter.values()])
plt.xlabel("Letter")
plt.ylabel("Win Rate (%)")
plt.title("Win Rate by Letter in Word")
plt.show()