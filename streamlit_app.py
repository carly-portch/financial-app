import streamlit as st
from datetime import date

# App title
st.title("Design your dream life")

# Instructions
st.write("This tool will help you calculate your estimated net worth at retirement based on your current financial details. Please fill in the following information.")

# Inputs for retirement
current_age = st.number_input("Current Age", min_value=0, max_value=120, value=30, step=1)
retirement_age = st.number_input("Desired Retirement Age", min_value=0, max_value=120, value=65, step=1)
monthly_income = st.number_input("Monthly Income (Post-Tax)", value=5000, step=100)
monthly_expenses = st.number_input("Monthly Expenses", value=2000, step=100)
rate_of_return = st.number_input("Rate of Return (%)", value=5.0, step=0.1)

# Note on rate of return
st.write("Note: If this money will be invested in the stock market, 6-7% is the average rate of return. For a savings account, use the interest rate on your account.")

# Add a button to "Calculate"
if st.button("Calculate"):
    # Calculate monthly contribution towards retirement
    monthly_contribution = monthly_income - monthly_expenses

    # Time period in years
    years_to_retirement = retirement_age - current_age

    # Convert rate of return to a decimal
    r = rate_of_return / 100

    # Number of times the interest is compounded per year (monthly compounding)
    n = 12

    # Compound interest formula: A = P * (1 + r/n)^(nt)
    future_value = monthly_contribution * (((1 + r/n)**(n*years_to_retirement) - 1) / (r/n))

    # Display the result
    st.write(f"Your estimated net worth at age {retirement_age} is: ${future_value:,.2f}")

# Add a section for joint goals
st.write("### Add a Joint Goal")

# Button to add a goal
if st.button("Add a joint goal"):
    goal_name = st.text_input("Goal Name", placeholder="e.g., New House")
    goal_amount = st.number_input("Goal Amount ($)", value=50000, step=1000)

    # Options for selecting a goal method
    goal_method = st.radio("How would you like to calculate the goal?",
                           ('By Desired Date', 'By Monthly Contribution'))

    if goal_method == 'By Desired Date':
        # Goal based on desired date
        desired_date = st.number_input("Desired Date (Year, YYYY)", min_value=date.today().year, step=1)
        # Calculate years to goal
        years_to_goal = desired_date - date.today().year
        
        # Calculate required monthly contribution
        if st.button("Calculate Goal by Date"):
            required_monthly_contribution = goal_amount / (years_to_goal * 12)
            st.write(f"To reach your goal of ${goal_amount:,.2f} by {desired_date}, you need to save ${required_monthly_contribution:,.2f} per month.")

    elif goal_method == 'By Monthly Contribution':
        # Goal based on fixed monthly contribution
        monthly_contribution_goal = st.number_input("Monthly Contribution for Goal ($)", value=500, step=10)

        # Calculate how many months and years it will take to reach the goal
        if st.button("Calculate Goal by Monthly Contribution"):
            months_to_goal = goal_amount / monthly_contribution_goal
            years_to_goal = months_to_goal / 12
            final_year = int(date.today().year + years_to_goal)
            st.write(f"With a monthly contribution of ${monthly_contribution_goal:,.2f}, you will reach your goal of ${goal_amount:,.2f} in {final_year}.")
