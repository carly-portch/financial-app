import streamlit as st
import plotly.graph_objects as go
import pandas as pd
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

# Initialize goals list
if 'goals' not in st.session_state:
    st.session_state.goals = []

# Add a goal
def add_goal():
    with st.form(key='goal_form'):
        goal_name = st.text_input("Name of Goal")
        goal_amount = st.number_input("Amount Needed for Goal", min_value=0.0)
        goal_type = st.radio("Calculate goal based on:", ("Target Date", "Monthly Contribution"))
        interest_rate = st.number_input("Interest Rate (%) (if applicable)", min_value=0.0, max_value=100.0, value=0.0)
        goal_year = None
        monthly_contribution = None

        if goal_type == "Target Date":
            goal_year = st.number_input("Target Year", min_value=current_age + 1)
            if st.form_submit_button("Calculate Goal"):
                months_needed = (goal_year - current_age) * 12
                if interest_rate > 0:
                    interest_rate_monthly = interest_rate / 100 / 12
                    monthly_contribution = goal_amount * (interest_rate_monthly * (1 + interest_rate_monthly) ** months_needed) / ((1 + interest_rate_monthly) ** months_needed - 1)
                else:
                    monthly_contribution = goal_amount / months_needed
                st.write(f"To reach {goal_name} by {goal_year}, you need to contribute ${monthly_contribution:,.2f} per month.")
        else:
            if st.form_submit_button("Calculate Goal"):
                months_needed = 0
                if interest_rate > 0:
                    interest_rate_monthly = interest_rate / 100 / 12
                    while goal_amount > 0:
                        goal_amount = goal_amount / (1 + interest_rate_monthly)
                        months_needed += 1
                else:
                    months_needed = goal_amount
                goal_year = current_age + (months_needed / 12)
                st.write(f"To meet {goal_name} with a monthly contribution, the goal will be reached by {goal_year:.0f}.")
        
        if goal_name and goal_amount and monthly_contribution:
            st.session_state.goals.append({
                'goal_name': goal_name,
                'goal_amount': goal_amount,
                'monthly_contribution': monthly_contribution,
                'goal_year': goal_year
            })

st.write("Add a goal:")
add_goal_button = st.button("Add a Goal")

# Show list of goals
st.write("Goals:")
for i, goal in enumerate(st.session_state.goals):
    st.write(f"**{goal['goal_name']}** - ${goal['goal_amount']:.2f} at ${goal['monthly_contribution']:.2f} per month")
    
# Calculate Retirement Net Worth
if st.button("Calculate Retirement"):
    monthly_contributions = monthly_income - monthly_expenses
    for goal in st.session_state.goals:
        monthly_contributions -= goal['monthly_contribution']
    
    years_to_retirement = retirement_age - current_age
    months_to_retirement = years_to_retirement * 12
    rate_of_return_monthly = rate_of_return / 100 / 12

    if rate_of_return_monthly > 0:
        retirement_net_worth = monthly_contributions * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
    else:
        retirement_net_worth = monthly_contributions * months_to_retirement

    st.write(f"Your estimated retirement net worth at age {retirement_age} is: ${retirement_net_worth:,.2f}")

# Plot timeline
def plot_timeline():
    today = date.today()
    current_year = today.year
    retirement_year = current_year + (retirement_age - current_age)
    
    goal_years = [goal['goal_year'] for goal in st.session_state.goals if goal['goal_year'] is not None]
    
    # Create timeline data
    timeline_df = pd.DataFrame({
        'Year': [current_year, retirement_year] + goal_years,
        'Event': ['Current Age', 'Retirement Age'] + ['Goal'] * len(goal_years),
        'Text': [
            f"<b>Current Age:</b> {current_age}<br><b>Monthly Income:</b> ${monthly_income:,.2f}<br><b>Monthly Expenses:</b> ${monthly_expenses:,.2f}<br><b>Amount Going Towards Retirement:</b> ${monthly_income - monthly_expenses:,.2f}",
            f"<b>Retirement Age:</b> {retirement_age}<br><b>Net Worth at Retirement:</b> ${retirement_net_worth:,.2f}"
        ] + [
            f"<b>Goal Name:</b> {goal['goal_name']}<br><b>Amount Needed:</b> ${goal['goal_amount']:.2f}<br><b>Monthly Contribution:</b> ${goal['monthly_contribution']:.2f}"
            for goal in st.session_state.goals
        ]
    })
    
    # Create the figure
    fig = go.Figure()
    
    # Add red dots for current and retirement ages
    fig.add_trace(go.Scatter(
        x=[current_year, retirement_year] + goal_years, 
        y=[0] * (2 + len(goal_years)), 
        mode='markers+text', 
        marker=dict(size=12, color='red', line=dict(width=2, color='black')), 
        text=['Current Age', 'Retirement Age'] + ['Goal'] * len(goal_years), 
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
    
    # Add lines connecting each goal to the timeline
    for goal_year in goal_years:
        fig.add_trace(go.Scatter(
            x=[goal_year, goal_year], 
            y=[0, 0], 
            mode='markers+text', 
            marker=dict(size=12, color='red', symbol='x', line=dict(width=2, color='black')),
            text=['Goal'], 
            textposition='top center',
            hoverinfo='text',
            hovertext=timeline_df.query(f"Year == {goal_year}")['Text'].values[0]
        ))

    # Update layout
    fig.update_layout(
        title="Life Timeline",
        xaxis_title='Year',
        yaxis=dict(visible=False),
        xaxis=dict(
            tickmode='array',
            tickvals=[current_year, retirement_year] + goal_years,
            ticktext=[f"{current_year}", f"{retirement_year}"] + [f"{year}" for year in goal_years]
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
