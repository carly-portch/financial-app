import streamlit as st
from datetime import datetime, date

# Title and Instructions
st.title("Design your dream life")
st.write("""
Welcome! Use this tool to calculate your retirement savings. Input your details below, and we'll estimate your retirement net worth. The rate of return is compounded monthly.
- **Rate of Return**: If investing in the stock market, 6-7% is typical. If using a savings account, enter the actual interest rate.
""")

# Inputs
current_birthday = st.date_input("Enter your birthday (YYYY-MM-DD)", value=date(1990, 1, 1))
retirement_age = st.number_input("Enter your estimated retirement age", min_value=18, max_value=100, value=65)
monthly_income = st.number_input("Enter your monthly income post-tax", min_value=0, value=5000)
monthly_expenses = st.number_input("Enter your monthly expenses", min_value=0, value=2000)
rate_of_return = st.number_input("Enter your expected rate of return (%)", min_value=0.0, value=5.0) / 100.0

# Convert today to a date object
today = date.today()

# Calculate current age and years to retirement
current_age_years = (today - current_birthday).days / 365.25
years_to_retirement = retirement_age - current_age_years

# Monthly contribution (difference between income and expenses)
monthly_contribution = monthly_income - monthly_expenses

# Button to trigger calculation
if st.button("Calculate"):
    # Variables for compound interest formula
    n = 12  # compounded monthly
    t = years_to_retirement
    C = monthly_contribution  # monthly contribution

    # Compound Interest Calculation (using formula A = P(1 + r/n)^(nt) + C[((1 + r/n)^(nt) - 1) / (r/n)])
    # Initial principal (P) is 0
    A = (C * (((1 + rate_of_return / n) ** (n * t) - 1) / (rate_of_return / n)))

    # Display Results
    st.write(f"With your inputs, your estimated retirement savings at age {retirement_age} is:")
    st.write(f"${A:,.2f}")
