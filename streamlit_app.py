import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math
from datetime import date

st.title("Design Your Dream Life")
st.write("This tool helps you estimate your retirement net worth and manage goals.")
st.write("Enter the required information below:")

# Input fields for retirement calculation
current_age = st.number_input("Enter your current age", min_value=0, key='current_age')
retirement_age = st.number_input("Enter your desired retirement age", min_value=current_age + 1, key='retirement_age')
monthly_income = st.number_input("Enter your monthly income after tax", min_value=0.0, key='monthly_income')
monthly_expenses = st.number_input("Enter your monthly expenses", min_value=0.0, key='monthly_expenses')
rate_of_return = st.number_input("Rate of return (%)", min_value=0.0, max_value=100.0, value=5.0, key='rate_of_return')
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

# Plotting timeline
def plot_timeline():
    years = list(range(current_age, retirement_age + 1))
    years_as_dates = [date.today().year + year - current_age for year in years]

    # Create DataFrame for plotting
    timeline_df = pd.DataFrame({
        'Year': years_as_dates,
        'Age': years,
        'Text': [''] * len(years)  # Initialize with empty text
    })

    # Update the text for the dots
    timeline_df.loc[timeline_df['Age'] == current_age, 'Text'] = [f'Current Age: {current_age}\nMonthly Income: ${monthly_income:,.2f}\nExpenses: ${monthly_expenses:,.2f}\nSavings to Retirement: ${monthly_contributions:,.2f}']
    timeline_df.loc[timeline_df['Age'] == retirement_age, 'Text'] = [f'Retirement Age: {retirement_age}\nEstimated Net Worth: ${retirement_net_worth:,.2f}']

    fig = go.Figure()

    # Add line across the timeline
    fig.add_trace(go.Scatter(x=[years_as_dates[0], years_as_dates[-1]], y=[0, 0], mode='lines', line=dict(color='gray', width=2), showlegend=False))

    # Add red dots at current age and retirement age
    fig.add_trace(go.Scatter(
        x=timeline_df['Year'],
        y=[0] * len(timeline_df),
        mode='markers+text',
        text=timeline_df['Text'],
        textposition='top center',
        marker=dict(color='red', size=10),
        showlegend=False
    ))

    fig.update_layout(
        title="Life Timeline",
        xaxis_title="Year",
        yaxis=dict(showticklabels=False),  # Hide y-axis labels
        xaxis=dict(
            tickvals=[year for year in years_as_dates], 
            ticktext=[str(year) for year in years_as_dates]
        ),
        textfont=dict(size=20)
    )

    st.plotly_chart(fig, use_container_width=True)

plot_timeline()

# Add a goal section
st.write("### Add a Goal")

if 'goals' not in st.session_state:
    st.session_state.goals = []

def add_goal():
    st.session_state.goals.append({
        'goal_name': '',
        'goal_amount': 0.0,
        'goal_rate_of_return': 5.0,
        'goal_type': 'Target date',
        'goal_year': date.today().year,
        'goal_monthly_contributions_input': 0.0,
    })

def calculate_goal(goal):
    goal_amount = goal['goal_amount']
    rate_of_return = goal['goal_rate_of_return'] / 100 / 12
    if goal['goal_type'] == "Target date":
        goal_year = goal['goal_year']
        months_to_goal = (goal_year - date.today().year) * 12
        if months_to_goal > 0:
            if rate_of_return > 0:
                monthly_contributions = goal_amount * rate_of_return / ((1 + rate_of_return) ** months_to_goal - 1)
            else:
                monthly_contributions = goal_amount / months_to_goal
            return monthly_contributions
        else:
            return "Error: The target year must be in the future."
    elif goal['goal_type'] == "Monthly contribution":
        monthly_contributions = goal['goal_monthly_contributions_input']
        if monthly_contributions > 0:
            months_to_goal = math.log(monthly_contributions / (monthly_contributions - goal_amount * rate_of_return)) / math.log(1 + rate_of_return)
            goal_completion_year = int(date.today().year + months_to_goal // 12)
            return f"Year {goal_completion_year}"
        else:
            return "Error: Monthly contribution must be greater than 0."

if st.button("Add a Goal"):
    add_goal()

for i, goal in enumerate(st.session_state.goals):
    st.write(f"### Goal {i + 1}")
    goal['goal_name'] = st.text_input(f"Goal name", value=goal['goal_name'], key=f"goal_name_{i}")
    goal['goal_amount'] = st.number_input(f"Goal amount ($)", value=goal['goal_amount'], min_value=0.0, key=f"goal_amount_{i}")
    goal['goal_rate_of_return'] = st.number_input(f"Rate of return for this goal (%)", value=goal['goal_rate_of_return'], min_value=0.0, max_value=100.0, key=f"goal_rate_of_return_{i}")
    goal['goal_type'] = st.radio(f"Would you like to input a target date or monthly amount?", ["Target date", "Monthly contribution"], index=0 if goal['goal_type'] == "Target date" else 1, key=f"goal_type_{i}")

    if goal['goal_type'] == "Target date":
        goal['goal_year'] = st.number_input(f"Desired year to reach this goal (yyyy)", value=goal['goal_year'], min_value=date.today().year, key=f"goal_year_{i}")
        if st.button(f"Calculate Goal {i + 1}", key=f"calculate_goal_{i}"):
            result = calculate_goal(goal)
            st.write(f"To reach {goal['goal_name']} by {goal['goal_year']}, you need to contribute ${result:,.2f} per month.")
    elif goal['goal_type'] == "Monthly contribution":
        goal['goal_monthly_contributions_input'] = st.number_input(f"How much would you like to contribute each month?", value=goal['goal_monthly_contributions_input'], min_value=0.0, key=f"goal_monthly_contributions_input_{i}")
        if st.button(f"Calculate Goal {i + 1}", key=f"calculate_goal_{i}"):
            result = calculate_goal(goal)
            st.write(f"At ${goal['goal_monthly_contributions_input']:,.2f} per month, you'll reach {goal['goal_name']} by {result}.")
