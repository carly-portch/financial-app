import streamlit as st
from datetime import date
import math

st.title("Design Your Dream Life")
st.write("This tool helps you estimate your retirement net worth and manage goals.")
st.write("Enter the required information below:")

# Input fields for retirement calculation
current_age = st.number_input("Enter your current age", min_value=0)
retirement_age = st.number_input("Enter your desired retirement age", min_value=current_age + 1)
monthly_income = st.number_input("Enter your monthly income (after tax)", min_value=0.0)
monthly_expenses = st.number_input("Enter your monthly expenses", min_value=0.0)
rate_of_return = st.number_input("Rate of return (%)", min_value=0.0, max_value=100.0, value=5.0)
st.write("Note: For stock market investments, 6-7% is the average rate of return; for savings, input the interest rate of your savings account.")

# Compound interest calculation
monthly_contributions = monthly_income - monthly_expenses
years_to_retirement = retirement_age - current_age
months_to_retirement = years_to_retirement * 12
rate_of_return_monthly = rate_of_return / 100 / 12

# Compound interest formula
if rate_of_return_monthly > 0:
    retirement_net_worth = monthly_contributions * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
else:
    retirement_net_worth = monthly_contributions * months_to_retirement

# Display retirement net worth
if st.button("Calculate Retirement Net Worth"):
    st.write(f"Your estimated retirement net worth at age {retirement_age} is: ${retirement_net_worth:,.2f}")

# Joint goals section
st.write("### Add a Joint Goal")

if 'goals' not in st.session_state:
    st.session_state.goals = []

def add_goal():
    st.session_state.goals.append({
        'goal_name': '',
        'goal_amount': 0.0,
        'goal_rate_of_return': 5.0,
        'goal_type': 'Desired date',
        'goal_year': date.today().year,
        'goal_monthly_contributions_input': 0.0,
    })

def delete_goal(index):
    if index < len(st.session_state.goals):
        del st.session_state.goals[index]

# Add goal functionality
if st.button("Add a joint goal"):
    add_goal()

for i, goal in enumerate(st.session_state.goals):
    st.write(f"### Goal {i + 1}")
    goal['goal_name'] = st.text_input(f"Goal name {i+1}", value=goal['goal_name'], key=f"goal_name_{i}")
    goal['goal_amount'] = st.number_input(f"Goal amount ($) {i+1}", value=goal['goal_amount'], min_value=0.0, key=f"goal_amount_{i}")
    goal['goal_rate_of_return'] = st.number_input(f"Rate of return for this goal (%) {i+1}", value=goal['goal_rate_of_return'], min_value=0.0, max_value=100.0, key=f"goal_rate_of_return_{i}")
    goal['goal_type'] = st.radio(f"Would you like to input a target date or monthly contribution? {i+1}", ["Target date", "Monthly contribution"], index=0 if goal['goal_type'] == "Target date" else 1, key=f"goal_type_{i}")

    if goal['goal_type'] == "Target date":
        goal['goal_year'] = st.number_input(f"Desired year to reach this goal (yyyy) {i+1}", value=goal['goal_year'], min_value=date.today().year, key=f"goal_year_{i}")
        months_to_goal = (goal['goal_year'] - date.today().year) * 12
        if months_to_goal > 0 and goal['goal_rate_of_return'] > 0:
            goal_monthly_contributions = goal['goal_amount'] * goal['goal_rate_of_return'] / 100 / 12 / ((1 + goal['goal_rate_of_return'] / 100 / 12) ** months_to_goal - 1)
            st.write(f"To reach {goal['goal_name']} by {goal['goal_year']}, you need to contribute ${goal_monthly_contributions:,.2f} per month.")
        else:
            st.write("Error: Ensure the rate of return is greater than 0 and the goal year is valid.")

    elif goal['goal_type'] == "Monthly contribution":
        goal['goal_monthly_contributions_input'] = st.number_input(f"How much would you like to contribute each month? {i+1}", value=goal['goal_monthly_contributions_input'], min_value=0.0, key=f"goal_monthly_contributions_input_{i}")
        if goal['goal_monthly_contributions_input'] > 0 and goal['goal_rate_of_return'] > 0:
            months_to_goal = math.log(goal['goal_monthly_contributions_input'] / (goal['goal_monthly_contributions_input'] - goal['goal_amount'] * goal['goal_rate_of_return'] / 100 / 12)) / math.log(1 + goal['goal_rate_of_return'] / 100 / 12)
            goal_completion_year = int(date.today().year + months_to_goal // 12)
            st.write(f"At ${goal['goal_monthly_contributions_input']:,.2f} per month, you'll reach {goal['goal_name']} by the year {goal_completion_year}.")
        else:
            st.write("Error: Ensure the rate of return and monthly contribution are greater than 0.")

    if st.button(f"Delete Goal {i+1}"):
        delete_goal(i)
