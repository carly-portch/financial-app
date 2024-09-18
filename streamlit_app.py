import streamlit as st
from datetime import datetime
import math

# Function to calculate compound interest for retirement net worth
def calculate_net_worth(birthday, retirement_age, monthly_income, monthly_expenses, rate_of_return):
    # Calculate current age
    today = datetime.today()
    birthday = datetime.strptime(birthday, "%Y-%m-%d")
    current_age = (today - birthday).days / 365.25

    # Years to retirement
    years_to_retirement = retirement_age - current_age
    if years_to_retirement < 0:
        st.error("Retirement age must be greater than your current age.")
        return

    # Monthly surplus (money towards retirement)
    monthly_surplus = monthly_income - monthly_expenses
    if monthly_surplus <= 0:
        st.error("Monthly expenses exceed or equal your income. No money to save for retirement.")
        return

    # Number of months to retirement
    months_to_retirement = int(years_to_retirement * 12)

    # Compound interest formula: Future Value = P * [(1 + r/n)^(nt) - 1] / (r/n)
    # P = monthly contribution (monthly_surplus)
    # r = annual rate of return (input as a percentage)
    # n = number of times interest is compounded per year (12 for monthly)
    # t = number of years to retirement

    r = rate_of_return / 100  # Convert percentage to decimal
    n = 12  # Compounded monthly
    t = years_to_retirement  # Time in years
    if t <= 0:
        st.error("Retirement age must be greater than current age.")
        return

    # Future Value calculation with monthly compounding and contributions
    future_net_worth = monthly_surplus * ((math.pow(1 + r / n, n * t) - 1) / (r / n))

    return future_net_worth

# Streamlit app
st.title("Retirement Net Worth Calculator")

# User inputs
birthday = st.text_input("Enter your birthday (YYYY-MM-DD):")
retirement_age = st.number_input("Enter your estimated retirement age:", min_value=18, max_value=100, value=65)
monthly_income = st.number_input("Enter your monthly income after tax:", min_value=0.0, value=5000.0)
monthly_expenses = st.number_input("Enter your monthly expenses:", min_value=0.0, value=3000.0)
rate_of_return = st.number_input("Enter your expected rate of return (%):", min_value=0.0, value=6.0)

# Informational note about the rate of return
st.markdown("""
**Note:** If this money is invested in the stock market, the average rate of return is around 6-7%.
If the money is in a savings account, use the interest rate on your savings account.
""")

# Calculate net worth
if st.button("Calculate"):
    if birthday:
        net_worth = calculate_net_worth(birthday, retirement_age, monthly_income, monthly_expenses, rate_of_return)
        if net_worth:
            st.success(f"Your estimated net worth at retirement is: ${net_worth:,.2f}")
    else:
        st.error("Please enter your birthday.")
