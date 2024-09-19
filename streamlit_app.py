import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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

# Initialize goal list
if 'goals' not in st.session_state:
    st.session_state.goals = []

# Display goal addition dropdown
with st.expander("Add a Goal"):
    goal_name = st.text_input("Name of goal")
    goal_amount = st.number_input("Amount of money for this goal", min_value=0.0)
    interest_rate = st.number_input("Interest rate (%) for the goal", min_value=0.0, max_value=100.0, value=5.0)
    goal_type = st.radio("Select how you want to calculate the goal", ["Target Date", "Monthly Contribution"])

    if goal_type == "Monthly Contribution":
        contribution_amount = st.number_input("Monthly contribution towards this goal", min_value=0.0)
        if contribution_amount > 0 and goal_amount > 0:
            rate_of_return_monthly = interest_rate / 100 / 12
            if rate_of_return_monthly > 0:
                # Calculate months required to reach goal
                numerator = np.log(contribution_amount / (contribution_amount - goal_amount * rate_of_return_monthly))
                denominator = np.log(1 + rate_of_return_monthly)
                if denominator == 0:  # Avoid division by zero
                    months_to_goal = float('inf')  # Set to infinity if no growth
                else:
                    months_to_goal = numerator / denominator
                target_year = date.today().year + int(np.ceil(months_to_goal / 12))  # Round up to ensure full year coverage
            else:
                target_year = date.today().year + int(np.ceil(goal_amount / contribution_amount / 12))  # No interest case
        else:
            target_year = None
    elif goal_type == "Target Date":
        target_year = st.number_input("Target year to reach this goal (yyyy)", min_value=date.today().year)
        contribution_amount = None

    # Add goal button
    if st.button("Add goal to timeline"):
        if goal_name and goal_amount > 0:
            if goal_type == "Monthly Contribution":
                # Use calculated target_year
                if target_year is None:
                    st.error("Please provide a valid monthly contribution or target year.")
                    return
            elif goal_type == "Target Date":
                target_year = int(target_year)
            
            # Append goal to session state
            st.session_state.goals.append({
                'goal_name': goal_name,
                'goal_amount': goal_amount,
                'monthly_contribution': contribution_amount if contribution_amount else 0,
                'target_date': target_year
            })

            st.success(f"Goal '{goal_name}' added successfully.")
            st.session_state.plot_updated = False  # Flag to update the plot
        else:
            st.error("Please enter a valid goal name and amount.")

# Function to calculate retirement net worth without goals
def calculate_retirement_net_worth_without_goals():
    monthly_savings = monthly_income - monthly_expenses
    years_to_retirement = retirement_age - current_age
    months_to_retirement = years_to_retirement * 12
    rate_of_return_monthly = rate_of_return / 100 / 12

    if rate_of_return_monthly > 0:
        retirement_net_worth = monthly_savings * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
    else:
        retirement_net_worth = monthly_savings * months_to_retirement

    return retirement_net_worth

# Function to calculate retirement net worth with goals
def calculate_retirement_net_worth_with_goals():
    remaining_contributions = monthly_income - monthly_expenses
    for goal in st.session_state.goals:
        remaining_contributions -= goal['monthly_contribution']

    years_to_retirement = retirement_age - current_age
    months_to_retirement = years_to_retirement * 12
    rate_of_return_monthly = rate_of_return / 100 / 12

    if rate_of_return_monthly > 0:
        retirement_net_worth = remaining_contributions * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
    else:
        retirement_net_worth = remaining_contributions * months_to_retirement

    return retirement_net_worth

# Plot timeline
def plot_timeline():
    # Clear the plot if already updated
    if 'plot_updated' in st.session_state and st.session_state.plot_updated:
        return
    
    today = date.today()
    current_year = today.year
    retirement_year = current_year + (retirement_age - current_age)
    
    # Create timeline data
    timeline_data = {
        'Year': [current_year, retirement_year] + [goal['target_date'] for goal in st.session_state.goals],
        'Event': ['Current Age', 'Retirement Age'] + [goal['goal_name'] for goal in st.session_state.goals],
        'Text': [
            f"<b>Current Age:</b> {current_age}<br><b>Monthly Income:</b> ${monthly_income:,.2f}<br><b>Monthly Expenses:</b> ${monthly_expenses:,.2f}<br><b>Amount Going Towards Retirement:</b> ${monthly_income - monthly_expenses - sum(goal['monthly_contribution'] for goal in st.session_state.goals):,.2f}",
            f"<b>Retirement Age:</b> {retirement_age}<br><b>Net Worth at Retirement:</b> ${calculate_retirement_net_worth_with_goals():,.2f}"
        ] + [
            f"<b>Goal:</b> {goal['goal_name']}<br><b>Amount:</b> ${goal['goal_amount']:.2f}<br><b>Monthly Contribution:</b> ${goal['monthly_contribution']:.2f}"
            for goal in st.session_state.goals
        ]
    }

    timeline_df = pd.DataFrame(timeline_data)

    # Create the figure
    fig = go.Figure()
    
    # Add red dots for current and retirement ages and goals
    fig.add_trace(go.Scatter(
        x=[current_year, retirement_year] + [goal['target_date'] for goal in st.session_state.goals], 
        y=[0] * (2 + len(st.session_state.goals)), 
        mode='markers+text', 
        marker=dict(size=12, color='red', line=dict(width=2, color='black')), 
        text=['Current Age', 'Retirement Age'] + [goal['goal_name'] for goal in st.session_state.goals], 
        textposition='top center', 
        hoverinfo='text', 
        hovertext=timeline_df['Text']
    ))
    
    # Add line connecting the red dots
    fig.add_trace(go.Scatter(
        x=[current_year, retirement_year] + [goal['target_date'] for goal in st.session_state.goals], 
        y=[0] * (2 + len(st.session_state.goals)), 
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
            tickvals=[current_year, retirement_year] + [goal['target_date'] for goal in st.session_state.goals],
            ticktext=[f"{current_year}", f"{retirement_year}"] + [f"{goal['target_date']}" for goal in st.session_state.goals]
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig)
    st.session_state.plot_updated = True

# Display existing goals and provide option to remove
st.sidebar.header("Manage Goals")
goal_to_remove = st.sidebar.selectbox("Select a goal to remove", [""] + [goal['goal_name'] for goal in st.session_state.goals])

if st.sidebar.button("Remove Goal"):
    if goal_to_remove:
        st.session_state.goals = [goal for goal in st.session_state.goals if goal['goal_name'] != goal_to_remove]
        st.sidebar.success(f"Goal '{goal_to_remove}' removed successfully.")
        st.session_state.plot_updated = False  # Flag to update the plot
    else:
        st.sidebar.error("Please select a goal to remove.")

# Calculate retirement based on remaining savings after goals
if st.button("Calculate Retirement"):
    if st.session_state.goals:
        st.write(f"Your estimated retirement net worth at age {retirement_age} after considering goals is: ${calculate_retirement_net_worth_with_goals():,.2f}")
    else:
        st.write(f"Your estimated retirement net worth at age {retirement_age} without goals is: ${calculate_retirement_net_worth_without_goals():,.2f}")

# Plot the timeline
plot_timeline()
