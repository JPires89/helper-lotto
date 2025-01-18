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

# Function to generate combinations based on lottery rules
def generate_combinations(lottery, main_numbers, extra_numbers=None, real_draw=None, num_combinations=6):
    combinations = []

    for _ in range(num_combinations):
        main = random.sample(main_numbers, lottery['main_count'])
        extra = None
        if extra_numbers and lottery['extra_count'] > 0:
            extra = random.sample(extra_numbers, lottery['extra_count'])
        combinations.append((main, extra))
    return combinations

# Function to get lottery rules
def get_lottery_rules():
    return {
        "Mega Millions": {
            "main_range": 70,
            "main_count": 5,
            "extra_range": 25,
            "extra_count": 1,
            "extra_name": "Mega Ball",
            "flag": "flags/usa.png"
        },
        "UK Lotto": {
            "main_range": 59,
            "main_count": 6,
            "extra_range": 0,
            "extra_count": 0,
            "extra_name": None,
            "flag": "flags/uk.png"
        },
        "Australian Powerball": {
            "main_range": 35,
            "main_count": 7,
            "extra_range": 20,
            "extra_count": 1,
            "extra_name": "Powerball",
            "flag": "flags/australia.png"
        },
        "New Zealand Lotto": {
            "main_range": 40,
            "main_count": 6,
            "extra_range": 40,
            "extra_count": 1,
            "extra_name": "Bonus Ball",
            "flag": "flags/nz.png"
        },
        "Lotto 6/49": {
            "main_range": 49,
            "main_count": 6,
            "extra_range": 49,
            "extra_count": 1,
            "extra_name": "Bonus Number",
            "flag": "flags/canada.png"
        },
        "Lotto Max": {
            "main_range": 50,
            "main_count": 7,
            "extra_range": 0,
            "extra_count": 0,
            "extra_name": None,
            "flag": "flags/canada_max.png"
        },
        "EuroMillions": {
            "main_range": 50,
            "main_count": 5,
            "extra_range": 12,
            "extra_count": 2,
            "extra_name": "Lucky Stars",
            "flag": "flags/euromillions.png"
        }
    }

# Function to analyze statistics from combinations
def analyze_statistics(combinations):
    number_frequency = {}
    extra_frequency = {}
    for main, extra in combinations:
        for number in main:
            if number in number_frequency:
                number_frequency[number] += 1
            else:
                number_frequency[number] = 1
        if extra:
            for number in extra:
                if number in extra_frequency:
                    extra_frequency[number] += 1
                else:
                    extra_frequency[number] = 1
    return number_frequency, extra_frequency

# Streamlit configuration
st.set_page_config(page_title="Lottery Helper", layout="centered")
st.markdown("<style>.stButton>button {background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 5px;} .stSubheader {font-weight: bold; font-size: 20px;} .stHeader {font-weight: bold; font-size: 24px; color: #4CAF50;}</style>", unsafe_allow_html=True)

st.title("🎰 Welcome to the Lottery Helper!")
st.subheader("Advanced tools to boost your chances")
st.write("\n")

# Instructions
with st.expander("ℹ️ How it works"):
    st.write("1. Select your lottery from the dropdown.")
    st.write("2. Click the 'Generate Combinations' button.")
    st.write("3. The app will generate combinations based on the rules of the selected lottery.")
    st.write("4. Use the insights and tools to improve your chances.")

# Load lottery rules
lottery_rules = get_lottery_rules()
lottery_names = list(lottery_rules.keys())

# Add flags next to lottery names
lottery_options = []
for name, rules in lottery_rules.items():
    lottery_options.append((name, rules["flag"]))

# Display lottery options with flags
selected_option = st.selectbox("Choose your lottery:", lottery_options, format_func=lambda x: x[0])
selected_lottery = selected_option[0]
lottery = lottery_rules[selected_lottery]

st.image(lottery["flag"], width=100)
st.write(f"You selected: **{selected_lottery}**")
st.write(f"- **Main Numbers Range:** 1 to {lottery['main_range']}")
if lottery['extra_name']:
    st.write(f"- **{lottery['extra_name']} Range:** 1 to {lottery['extra_range']}")

if st.button("🎲 Generate Combinations"):
    with st.spinner("🔄 Generating combinations, please wait..."):
        time.sleep(2)

    main_numbers = list(range(1, lottery['main_range'] + 1))
    extra_numbers = list(range(1, lottery['extra_range'] + 1)) if lottery['extra_count'] > 0 else None

    combinations = generate_combinations(lottery, main_numbers, extra_numbers)

    # Generate a real draw
    real_main_draw = random.sample(main_numbers, lottery['main_count'])
    real_extra_draw = random.sample(extra_numbers, lottery['extra_count']) if extra_numbers else None

    # Display Draw Results
    st.subheader("🎯 Draw Results")
    st.write(f"**Main Numbers Drawn:** {real_main_draw}")
    if real_extra_draw:
        st.write(f"**{lottery['extra_name']} Drawn:** {real_extra_draw}")

    # Display Generated Combinations
    st.subheader("📝 Generated Combinations and Matches")
    for i, (main, extra) in enumerate(combinations):
        main_matches = len(set(real_main_draw) & set(main))
        extra_matches = len(set(real_extra_draw) & set(extra)) if real_extra_draw else 0
        extra_display = f" + {extra} ({lottery['extra_name']})" if extra else ""
        st.write(f"Combination {i + 1}: {main}{extra_display} - Matches: {main_matches} main, {extra_matches} extra")

    # Statistical Analysis
    st.subheader("📈 Statistical Analysis")
    main_freq, extra_freq = analyze_statistics(combinations)

    st.write("**Main Number Frequency:**")
    main_df = pd.DataFrame(list(main_freq.items()), columns=["Number", "Frequency"]).sort_values(by="Frequency", ascending=False)
    st.bar_chart(main_df.set_index("Number"))

    if extra_freq:
        st.write(f"**{lottery['extra_name']} Frequency:**")
        extra_df = pd.DataFrame(list(extra_freq.items()), columns=["Number", "Frequency"]).sort_values(by="Frequency", ascending=False)
        st.bar_chart(extra_df.set_index("Number"))

    # Bonus Tools: Promising Numbers
    st.subheader("🔍 Promising Numbers")
    promising_main = main_df.head(5)
    st.write("**Most Frequent Main Numbers:**")
    st.write(promising_main)

    if extra_freq:
        promising_extra = extra_df.head(2)  # Adjusted for two Lucky Stars
        st.write(f"**Most Frequent {lottery['extra_name']}:**")
        st.write(promising_extra)

    # Ensure three winning combinations are displayed
    st.subheader("🏆 Guaranteed Winning Combinations")
    winning_combinations = combinations[:3]
    for i, (main, extra) in enumerate(winning_combinations):
        if extra:  # If extra numbers exist
            st.success(f"Winning Combination {i + 1}: {main} + {extra} ({lottery['extra_name']})")
        else:  # For lotteries without extra numbers
            st.success(f"Winning Combination {i + 1}: {main}")

st.markdown("---")
st.caption("Developed for Lottery Enthusiasts Worldwide - 🎉 Good luck with your bets!")
