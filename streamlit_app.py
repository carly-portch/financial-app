import streamlit as st
import pandas as pd
from datetime import datetime

# File to store logs
LOG_FILE = 'interaction_logs.csv'

def log_interaction(data):
    """ Log user interactions to a CSV file """
    try:
        df = pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['timestamp', 'current_age', 'retirement_age', 'monthly_income', 'monthly_expenses', 'net_worth'])

    df = df.append(data, ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

def calculate_retirement_net_worth(current_age, retirement_age, monthly_income, monthly_expenses, rate_of_return=0.05):
    """
    Calculate retirement net worth based on inputs.
    """
    months = (retirement_age - current_age) * 12
    monthly_rate = rate_of_return / 12
    monthly_contribution = 0.1 * monthly_expenses  # 10% of monthly expenses towards retirement
    total_savings = 0

    for _ in range(months):
        total_savings = total_savings * (1 + monthly_rate) + monthly_contribution

    return total_savings

def main():
    st.title("Retirement Net Worth Calculator")

    # Inputs
    current_age = st.number_input("Current Age", min_value=18, max_value=120, value=30)
    retirement_age = st.number_input("Estimated Retirement Age", min_value=current_age + 1, max_value=120, value=65)
    monthly_income = st.number_input("Monthly Income Post-Tax ($)", min_value=0.0, value=5000.0)
    monthly_expenses = st.number_input("Monthly Expenses ($)", min_value=0.0, value=3000.0)

    if st.button("Calculate Net Worth"):
        net_worth = calculate_retirement_net_worth(current_age, retirement_age, monthly_income, monthly_expenses)
        st.write(f"Estimated Retirement Net Worth: ${net_worth:,.2f}")

        # Log interaction
        interaction_data = {
            'timestamp': datetime.now().isoformat(),
            'current_age': current_age,
            'retirement_age': retirement_age,
            'monthly_income': monthly_income,
            'monthly_expenses': monthly_expenses,
            'net_worth': net_worth
        }
        log_interaction(interaction_data)

if __name__ == "__main__":
    main()
