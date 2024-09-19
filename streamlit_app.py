import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date

# Title and introduction
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

# Initialize goals list in session state
if 'goals' not in st.session_state:
    st.session_state.goals = []

# Display form to add a goal
with st.expander("Add a Goal"):
    goal_name = st.text_input("Name of goal")
    goal_amount = st.number_input("Amount needed for this goal", min_value=0.0)
    method = st.radio("Calculate goal based on:", ["Target Date", "Monthly Contribution"])
    
    if method == "Monthly Contribution":
        interest_rate = st.number_input("Interest rate (%) for this goal (monthly compounded)", min_value=0.0, max_value=100.0, value=0.0)
        goal_date = st.date_input("Estimated date to reach this goal")
    else:
        target_year = st.number_input("Year you want to reach this goal", min_value=current_age + 1)
        
    if st.button("Add Goal"):
        if method == "Monthly Contribution":
            months_until_goal = (goal_date.year - date.today().year) * 12 + (goal_date.month - date.today().month)
            monthly_contribution_needed = goal_amount / (((1 + (interest_rate / 100 / 12)) ** months_until_goal - 1) / (interest_rate / 100 / 12))
        else:
            months_until_goal = (target_year - current_age) * 12
            monthly_contribution_needed = goal_amount / months_until_goal
        
        st.session_state.goals.append({
            'goal_name': goal_name,
            'goal_amount': goal_amount,
            'monthly_contribution_needed': monthly_contribution_needed,
            'target_year': target_year if method == "Target Date" else goal_date.year
        })

# Display added goals with options to remove
for i, goal in enumerate(st.session_state.goals):
    st.write(f"**Goal Name:** {goal['goal_name']}")
    st.write(f"**Amount Needed:** ${goal['goal_amount']:,.2f}")
    st.write(f"**Monthly Contribution Needed:** ${goal['monthly_contribution_needed']:,.2f}")
    st.write(f"**Target Year:** {goal['target_year']}")
    if st.button(f"Remove Goal {i+1}"):
        st.session_state.goals.pop(i)
        st.experimental_rerun()

# Calculate retirement button
if st.button("Calculate Retirement"):
    # Calculate remaining savings
    total_goal_contributions = sum(goal['monthly_contribution_needed'] for goal in st.session_state.goals)
    remaining_contributions = max(0, monthly_income - monthly_expenses - total_goal_contributions)
    
    # Calculate retirement net worth
    years_to_retirement = retirement_age - current_age
    months_to_retirement = years_to_retirement * 12
    rate_of_return_monthly = rate_of_return / 100 / 12
    
    if rate_of_return_monthly > 0:
        retirement_net_worth = remaining_contributions * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
    else:
        retirement_net_worth = remaining_contributions * months_to_retirement
    
    st.write(f"Estimated retirement net worth at age {retirement_age} is: ${retirement_net_worth:,.2f}")

# Plot timeline
def plot_timeline():
    today = date.today()
    current_year = today.year
    retirement_year = current_year + (retirement_age - current_age)
    
    # Create timeline data
    timeline_df = pd.DataFrame({
        'Year': [current_year, retirement_year] + [goal['target_year'] for goal in st.session_state.goals],
        'Event': ['Current Age', 'Retirement Age'] + [goal['goal_name'] for goal in st.session_state.goals],
        'Text': [
            f"<b>Current Age:</b> {current_age}<br><b>Monthly Income:</b> ${monthly_income:,.2f}<br><b>Monthly Expenses:</b> ${monthly_expenses:,.2f}<br><b>Amount Going Towards Retirement:</b> ${remaining_contributions:,.2f}",
            f"<b>Retirement Age:</b> {retirement_age}<br><b>Net Worth at Retirement:</b> ${retirement_net_worth:,.2f}"
        ] + [
            f"<b>Goal Name:</b> {goal['goal_name']}<br><b>Amount Needed:</b> ${goal['goal_amount']:.2f}<br><b>Monthly Contribution:</b> ${goal['monthly_contribution_needed']:.2f}"
            for goal in st.session_state.goals
        ]
    })
    
    # Create the figure
    fig = go.Figure()
    
    # Add red dots for current and retirement ages, and goals
    fig.add_trace(go.Scatter(
        x=[current_year, retirement_year] + [goal['target_year'] for goal in st.session_state.goals],
        y=[0] * (2 + len(st.session_state.goals)),
        mode='markers',
        marker=dict(size=12, color='red', line=dict(width=2, color='black')),
        text=['Current Age', 'Retirement Age'] + [goal['goal_name'] for goal in st.session_state.goals],
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
    
    # Add lines from goals to retirement
    for goal in st.session_state.goals:
        fig.add_trace(go.Scatter(
            x=[goal['target_year'], retirement_year],
            y=[0, 0],
            mode='lines',
            line=dict(color='blue', width=1, dash='dash')
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

# Plot the timeline
plot_timeline()
