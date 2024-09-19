import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import math
from datetime import date

st.title("Design Your Dream Life")
st.write("This tool helps you estimate your retirement net worth and manage goals.")
st.write("Enter the required information below:")

# Input fields for retirement calculation
current_age = st.number_input("Enter your current age", min_value=0)
retirement_age = st.number_input("Enter your desired retirement age", min_value=current_age + 1)
monthly_income = st.number_input("Enter your monthly income after tax", min_value=0.0)
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

# Plot timeline
def plot_timeline():
    today = date.today()
    current_year = today.year
    retirement_year = current_year + (retirement_age - current_age)
    
    # Create timeline data
    timeline_df = pd.DataFrame({
        'Year': [current_year, retirement_year],
        'Event': ['Current Age', 'Retirement Age'],
        'Text': [
            f"<b>Current Age:</b> {current_age}<br><b>Monthly Income:</b> ${monthly_income:,.2f}<br><b>Monthly Expenses:</b> ${monthly_expenses:,.2f}<br><b>Amount Going Towards Retirement:</b> ${monthly_contributions:,.2f}",
            f"<b>Retirement Age:</b> {retirement_age}<br><b>Net Worth at Retirement:</b> ${retirement_net_worth:,.2f}"
        ]
    })
    
    # Create the figure
    fig = go.Figure()
    
    # Add red dots for current and retirement ages
    fig.add_trace(go.Scatter(
        x=[current_year, retirement_year], 
        y=[0, 0], 
        mode='markers', 
        marker=dict(size=12, color='red', line=dict(width=2, color='black')), 
        text=['Current Age', 'Retirement Age'], 
        textposition='top center', 
        hoverinfo='text', 
        hovertext=timeline_df['Text']
    ))
    
    # Add line connecting the red dots
    fig.add_trace(go.Scatter(
        x=[current_year, retirement_year], 
        y=[0, 0], 
        mode='lines', 
        line=dict(color='red', width=2)
    ))
    
    # Update layout
    fig.update_layout(
        title="Life Timeline",
        xaxis_title='Year',
        yaxis=dict(visible=False),
        xaxis=dict(
            tickmode='array',
            tickvals=[current_year, retirement_year],
            ticktext=[f"{current_year}", f"{retirement_year}"]
        ),
        showlegend=False
    )
    
    # Format hover text as lists and set font size
    fig.update_traces(
        hovertemplate='<b>%{text}</b><br><br>' + timeline_df['Text'] +
        '<extra></extra>',
        textfont=dict(size=18)  # Adjust font size for better readability
    )
    
    st.plotly_chart(fig)

# Plot the timeline
plot_timeline()
