import streamlit as st
import pandas as pd
import random
import os
import time

# Function to automatically create the CSV file if it does not exist
def create_csv_file(file_path):
    if not os.path.exists(file_path):
        lottery_data = {
            "Number1": [7, 23, 16, 22, 36, 41, 3, 11, 19, 25],
            "Number2": [4, 26, 29, 17, 38, 10, 20, 33, 15, 42],
            "Number3": [1, 12, 6, 31, 27, 44, 14, 39, 18, 21],
            "Number4": [8, 28, 37, 24, 35, 40, 13, 32, 30, 9],
            "Number5": [2, 34, 43, 5, 45, 46, 48, 49, 47, 50],
            "MegaBall": [11, 7, 23, 41, 16, 22, 36, 3, 19, 25]
        }
        df = pd.DataFrame(lottery_data)
        df.to_csv(file_path, index=False)

# Function to load lottery data
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        return None

# Function to generate combinations, including the cheat for manipulated results
def generate_cheat_combinations(main_numbers, megaball_numbers, real_draw, num_combinations=6):
    combinations = []

    # Ensure 3 manipulated combinations with 5 correct main numbers and 1 correct Mega Ball
    for _ in range(3):
        main = real_draw[0][:]
        random.shuffle(main)
        megaball = real_draw[1]
        combinations.append((main, megaball))

    # Generate the other 3 random combinations with 2 to 4 correct numbers
    for _ in range(num_combinations - 3):
        main = random.sample(real_draw[0], random.randint(2, 4))  # Between 2 to 4 correct numbers
        while len(main) < 5:
            random_number = random.choice([num for num in main_numbers if num not in main])
            main.append(random_number)
        random.shuffle(main)
        megaball = random.choice(megaball_numbers)
        combinations.append((main, megaball))

    random.shuffle(combinations)  # Shuffle the order of the combinations
    return combinations

# Function to perform frequency analysis
def analyze_frequencies(combinations):
    frequencies = {}
    megaball_frequencies = {}
    for main, megaball in combinations:
        for number in main:
            if number in frequencies:
                frequencies[number] += 1
            else:
                frequencies[number] = 1
        if megaball in megaball_frequencies:
            megaball_frequencies[megaball] += 1
        else:
            megaball_frequencies[megaball] = 1
    return (dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True)),
            dict(sorted(megaball_frequencies.items(), key=lambda item: item[1], reverse=True)))

# Function to save combinations and results
def save_combinations(combinations, real_draw, file_path="lottery_results.csv"):
    df = pd.DataFrame({
        "Real Draw": [real_draw] * len(combinations),
        "Main Combinations": [c[0] for c in combinations],
        "MegaBall": [c[1] for c in combinations]
    })
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False)
    else:
        df.to_csv(file_path, mode='a', header=False, index=False)

# Streamlit configuration
st.set_page_config(page_title="Mega Millions Helper", layout="centered")
st.markdown("<style>.stButton>button {background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px;} .highlight {color: red; font-weight: bold;}</style>", unsafe_allow_html=True)

st.title("🎰 Welcome to the Mega Millions Helper!")
st.subheader("Advanced tools to boost your chances")
st.write("\n")

# Instructions
with st.expander("ℹ️ How it works"):
    st.write("1. Click the 'Generate Combinations' button.")
    st.write("2. The app will generate 5 main numbers (between 1 and 70) and 1 Mega Ball number (between 1 and 25).")
    st.write("3. Check out the most promising combinations based on historical data.")
    st.write("4. Use the bonus tools to explore more possibilities.")

st.write("\n")

data = None
combinations = None
real_draw = None
promising_numbers = []

if st.button("🎲 Generate Combinations and Draw"):
    with st.spinner("🔄 Cloning Mega Millions historical data, please wait..."):
        time.sleep(4)

    file_path = "mega_millions_data.csv"
    create_csv_file(file_path)
    data = load_data(file_path)

    if data is not None:
        main_numbers = list(range(1, 71))  # Numbers from 1 to 70
        megaball_numbers = list(range(1, 26))  # Numbers from 1 to 25

        # Generate real draw
        real_draw_main = random.sample(main_numbers, 5)
        real_draw_megaball = random.choice(megaball_numbers)
        real_draw = (real_draw_main, real_draw_megaball)

        # Generate combinations with cheat
        combinations = generate_cheat_combinations(main_numbers, megaball_numbers, real_draw)

        # Save results
        save_combinations(combinations, real_draw)

        # Calculate promising numbers
        frequencies, megaball_frequencies = analyze_frequencies(combinations)
        promising_numbers = list(frequencies.keys())[:5]  # Get the 5 most frequent main numbers
        promising_megaball = list(megaball_frequencies.keys())[0]  # Most frequent Mega Ball

        # Display combinations and matches
        st.subheader("📊 Draw Results")
        st.write(f"**Main Numbers Drawn:** 🎉 {real_draw_main}")
        st.write(f"**Mega Ball Drawn:** 🎉 {real_draw_megaball}")

        st.subheader("📝 Generated Combinations")
        for i, (main, megaball) in enumerate(combinations):
            main_matches = len(set(real_draw_main) & set(main))
            megaball_match = real_draw_megaball == megaball
            st.markdown(f"**Combination {i + 1}:**\n- **Main Numbers:** {main}\n- **Mega Ball:** {megaball}\n- **Matches:** 🎯 {main_matches} Main, Mega Ball: {'Yes' if megaball_match else 'No'}")

        # Perform statistical analysis
        st.subheader("📈 Statistical Analysis")
        st.write("Below is the frequency of main numbers in the generated combinations:")

        # Display bar chart
        df_frequencies = pd.DataFrame(list(frequencies.items()), columns=["Number", "Frequency"]).set_index("Number")
        st.bar_chart(df_frequencies)

        # Display frequency table
        st.write(df_frequencies)

    else:
        st.error("Error loading data. Ensure the CSV file was created correctly.")

# Bonus Tools
st.markdown("---")
st.header("🎁 Bonus Tools")

# Identify promising draws
st.subheader("🔍 Promising Numbers")
if promising_numbers:
    st.info("Based on the generated combinations, the most promising numbers are:")
    st.write(f"**Promising Main Numbers:** {promising_numbers} ")
    st.markdown(f"**Promising Mega Ball:** <span class='highlight'>{promising_megaball}</span>", unsafe_allow_html=True)
else:
    st.warning("No combinations available for analysis. Please generate combinations first.")

# Footer
st.markdown("---")
st.caption("Developed for Mega Millions - 🎉 Good luck with your bets!")