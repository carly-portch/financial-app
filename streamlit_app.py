import streamlit as st
import datetime

# Title and instructions
st.title("Design Your Dream Life")
st.write("Input your details to calculate your retirement net worth and add your goals to see how much you need to save monthly to achieve them!")

# Inputs for personal financial info
current_age = st.number_input("Current Age", min_value=18, max_value=100)
retirement_age = st.number_input("Desired Retirement Age", min_value=current_age + 1, max_value=100)
monthly_income = st.number_input("Monthly Income After Tax", min_value=0)
monthly_expenses = st.number_input("Monthly Expenses", min_value=0)
rate_of_return = st.number_input("Rate of Return (%)", value=5.0)
st.write("Note: Stock market average rate of return is 6-7%, for savings accounts use your actual interest rate.")

# Compound interest calculation
monthly_contributions = monthly_income - monthly_expenses
years_to_retirement = retirement_age - current_age
months_to_retirement = years_to_retirement * 12
final_amount = monthly_contributions * (((1 + rate_of_return / 100 / 12) ** months_to_retirement - 1) / (rate_of_return / 100 / 12))

# Display retirement amount
if st.button("Calculate Retirement Net Worth"):
    st.write(f"At the age of {retirement_age}, your estimated retirement net worth will be: ${final_amount:,.2f}")

# Goal management
goals = []

def add_goal():
    goal_name = st.text_input("Goal Name")
    goal_amount = st.number_input("Goal Amount", min_value=0.0)
    goal_choice = st.selectbox("How would you like to calculate?", ["By Target Date", "By Monthly Contribution"])
    
    if goal_choice == "By Target Date":
        goal_year = st.number_input("Goal Target Year (yyyy)", min_value=datetime.datetime.now().year)
        months_to_goal = (goal_year - datetime.datetime.now().year) * 12
        goal_rate_of_return = st.number_input("Goal Rate of Return (%)", value=5.0)
        goal_monthly_contributions = goal_amount * goal_rate_of_return / 100 / 12 / ((1 + goal_rate_of_return / 100 / 12) ** months_to_goal - 1)
        
        if st.button("Calculate for Goal"):
            st.write(f"To reach {goal_name} by {goal_year}, you need to contribute ${goal_monthly_contributions:,.2f} per month.")
    
    elif goal_choice == "By Monthly Contribution":
        goal_monthly_contributions = st.number_input("Desired Monthly Contribution", min_value=0.0)
        goal_rate_of_return = st.number_input("Goal Rate of Return (%)", value=5.0)
        months_to_goal = st.number_input("Desired Months to Goal", min_value=0)
        goal_year = datetime.datetime.now().year + months_to_goal // 12
        
        if st.button("Calculate for Goal"):
            st.write(f"At ${goal_monthly_contributions:,.2f} per month, you will reach {goal_name} by {goal_year}.")

if st.button("Add a Joint Goal"):
    with st.expander("Goal Info"):
        add_goal()

# Option to add multiple goals
if st.button("Add Another Goal"):
    add_goal()

# Option to delete a goal
if st.button("Delete a Goal"):
    st.write("Goal Deleted")
