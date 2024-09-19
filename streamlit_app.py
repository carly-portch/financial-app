import streamlit as st

# App title
st.title("Design your dream life")

# Instructions
st.write("This tool will help you calculate your estimated net worth at retirement based on your current financial details. Please fill in the following information.")

# Inputs
current_age = st.number_input("Current Age", min_value=0, max_value=120, value=30, step=1)
retirement_age = st.number_input("Desired Retirement Age", min_value=0, max_value=120, value=65, step=1)
monthly_income = st.number_input("Monthly Income (Post-Tax)", value=5000, step=100)
monthly_expenses = st.number_input("Monthly Expenses", value=2000, step=100)
rate_of_return = st.number_input("Rate of Return (%)", value=5.0, step=0.1)

# Note on rate of return
st.write("Note: If this money will be invested in the stock market, 6-7% is the average rate of return. For a savings account, use the interest rate on your account.")

# Calculate monthly contribution towards retirement
monthly_contribution = monthly_income - monthly_expenses

# Time period in years
years_to_retirement = retirement_age - current_age

# Convert rate of return to a decimal
r = rate_of_return / 100

# Number of times the interest is compounded per year (monthly compounding)
n = 12

# Compound interest formula: A = P * (1 + r/n)^(nt)
# Here, P = 0 (starting with no savings), but we have regular monthly contributions
future_value = monthly_contribution * (((1 + r/n)**(n*years_to_retirement) - 1) / (r/n))

# Display the result
st.write(f"Your estimated net worth at age {retirement_age} is: ${future_value:,.2f}")
