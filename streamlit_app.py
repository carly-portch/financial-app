import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date, datetime
from typing import List

# Function to calculate goal based on monthly contribution
def calculate_target_date(amount_needed, monthly_contribution, annual_interest_rate):
    months = 0
    monthly_interest_rate = annual_interest_rate / 100 / 12
    while amount_needed > 0:
        amount_needed = amount_needed * (1 + monthly_interest_rate) - monthly_contribution
        months += 1
    target_date = datetime.now() + pd.DateOffset(months=months)
    return target_date.year, months

# Function to calculate monthly contribution needed for target date
def calculate_monthly_contribution(amount_needed, target_year, annual_interest_rate):
    months = (target_year - datetime.now().year) * 12
    monthly_interest_rate = annual_interest_rate / 100 / 12
    if monthly_interest_rate > 0:
        monthly_contribution = amount_needed * monthly_interest_rate / ((1 + monthly_interest_rate) ** months - 1)
    else:
        monthly_contribution = amount_needed / months
    return monthly_contribution

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

# Initialize session state for goals
if 'goals' not in st.session_state:
    st.session_state.goals = []

# Add a goal section
with st.form("add_goal_form"):
    st.write("### Add a Goal")
    goal_name = st.text_input("Name of the goal")
    amount_needed = st.number_input("Amount needed for the goal", min_value=0.0)
    interest_rate = st.number_input("Interest rate (%)", min_value=0.0, max_value=100.0, value=5.0)
    goal_type = st.radio("Calculate goal based on", ["Target Date", "Monthly Contribution"])
    
    if goal_type == "Target Date":
        target_year = st.number_input("Target year (yyyy)", min_value=datetime.now().year)
        monthly_contribution = calculate_monthly_contribution(amount_needed, target_year, interest_rate)
    elif goal_type == "Monthly Contribution":
        monthly_contribution = st.number_input("Monthly contribution amount", min_value=0.0)
        target_year, _ = calculate_target_date(amount_needed, monthly_contribution, interest_rate)

    # Add goal button
    if st.form_submit_button("Add Goal"):
        if goal_name and amount_needed > 0:
            goal_data = {
                'name': goal_name,
                'amount_needed': amount_needed,
                'monthly_contribution': monthly_contribution,
                'target_year': target_year
            }
            st.session_state.goals.append(goal_data)
            st.write(f"Goal '{goal_name}' added!")

# Remove goal functionality
for i, goal in enumerate(st.session_state.goals):
    with st.expander(f"Goal: {goal['name']}", expanded=False):
        st.write(f"Amount needed: ${goal['amount_needed']:,.2f}")
        st.write(f"Monthly contribution: ${goal['monthly_contribution']:,.2f}")
        st.write(f"Target year: {goal['target_year']}")
        if st.button("Remove Goal", key=i):
            st.session_state.goals.pop(i)
            st.write(f"Goal '{goal['name']}' removed!")

# Calculate retirement net worth button
if st.button("Calculate Retirement Net Worth"):
    monthly_contributions = monthly_income - monthly_expenses - sum(goal['monthly_contribution'] for goal in st.session_state.goals)
    years_to_retirement = retirement_age - current_age
    months_to_retirement = years_to_retirement * 12
    rate_of_return_monthly = rate_of_return / 100 / 12

    # Compound interest formula
    if rate_of_return_monthly > 0:
        retirement_net_worth = monthly_contributions * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
    else:
        retirement_net_worth = monthly_contributions * months_to_retirement

    st.write(f"Your estimated retirement net worth at age {retirement_age} is: ${retirement_net_worth:,.2f}")

    # Plot the timeline
    def plot_timeline():
        today = date.today()
        current_year = today.year
        retirement_year = current_year + (retirement_age - current_age)

        # Create timeline data
        events = {
            'Year': [current_year, retirement_year] + [goal['target_year'] for goal in st.session_state.goals],
            'Event': ['Current Age', 'Retirement Age'] + [goal['name'] for goal in st.session_state.goals],
            'Text': [
                f"<b>Current Age:</b> {current_age}<br><b>Monthly Income:</b> ${monthly_income:,.2f}<br><b>Monthly Expenses:</b> ${monthly_expenses:,.2f}<br><b>Amount Going Towards Retirement:</b> ${monthly_contributions:,.2f}",
                f"<b>Retirement Age:</b> {retirement_age}<br><b>Net Worth at Retirement:</b> ${retirement_net_worth:,.2f}"
            ] + [
                f"<b>Goal:</b> {goal['name']}<br><b>Amount Needed:</b> ${goal['amount_needed']:,.2f}<br><b>Monthly Contribution:</b> ${goal['monthly_contribution']:,.2f}" for goal in st.session_state.goals
            ]
        }
        timeline_df = pd.DataFrame(events)

        # Create the figure
        fig = go.Figure()

        # Add red dots for current age, retirement age, and goal dates
        fig.add_trace(go.Scatter(
            x=[current_year, retirement_year] + [goal['target_year'] for goal in st.session_state.goals], 
            y=[0] * (2 + len(st.session_state.goals)),
            mode='markers', 
            marker=dict(size=12, color='red', line=dict(width=2, color='black')), 
            text=['Current Age', 'Retirement Age'] + [goal['name'] for goal in st.session_state.goals],
            textposition='top center', 
            hoverinfo='text', 
            hovertext=timeline_df['Text']
        ))

        # Add x marks for goals
        for goal in st.session_state.goals:
            fig.add_trace(go.Scatter(
                x=[goal['target_year']], 
                y=[0], 
                mode='markers', 
                marker=dict(size=12, color='blue', symbol='x', line=dict(width=2, color='black')), 
                text=[goal['name']], 
                textposition='top center', 
                hoverinfo='text', 
                hovertext=f"<b>Goal:</b> {goal['name']}<br><b>Amount Needed:</b> ${goal['amount_needed']:,.2f}<br><b>Monthly Contribution:</b> ${goal['monthly_contribution']:,.2f}"
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
                tickvals=[current_year, retirement_year] + [goal['target_year'] for goal in st.session_state.goals],
                ticktext=[f"{current_year}", f"{retirement_year}"] + [f"{goal['target_year']}" for goal in st.session_state.goals]
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

    plot_timeline()
