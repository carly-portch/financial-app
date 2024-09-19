import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import date
import math

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

# Plot timeline
def plot_timeline():
    today = date.today()
    current_year = today.year
    retirement_year = current_year + (retirement_age - current_age)
    
    timeline_df = pd.DataFrame({
        'Year': [current_year, retirement_year],
        'Event': ['Current Age', 'Retirement Age'],
        'Text': [f"Current Age: {current_age}\nMonthly Income: ${monthly_income:,.2f}\nMonthly Expenses: ${monthly_expenses:,.2f}\nAmount Going Towards Retirement: ${monthly_contributions:,.2f}",
                 f"Retirement Age: {retirement_age}\nNet Worth at Retirement: ${retirement_net_worth:,.2f}"]
    })
    
    fig = px.scatter(timeline_df, x='Year', y=[0]*len(timeline_df), text='Text', title="Life Timeline", labels={'Year': 'Year'})
    
    fig.update_traces(marker=dict(size=12, color='red', line=dict(width=2, color='black')), selector=dict(mode='markers+text'))
    fig.update_layout(showlegend=False, xaxis_title='Year', yaxis=dict(visible=False), xaxis=dict(tickmode='array', tickvals=[current_year, retirement_year], ticktext=[f"{current_year}", f"{retirement_year}"]))
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_visible=False,
        xaxis=dict(tickmode='array', tickvals=[current_year, retirement_year], ticktext=[f"{current_year}", f"{retirement_year}"])
    )
    
    # Add hover text with detailed information
    fig.update_traces(
        texttemplate='%{text}',
        hovertemplate='<br>'.join([
            '%{text}'
        ])
    )
    
    st.plotly_chart(fig)

# Plot the timeline
plot_timeline()
