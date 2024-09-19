import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.title("Design Your Dream Life")
st.write("This tool helps you estimate your retirement net worth and manage goals.")
st.write("Enter the required information below:")

# Input fields for retirement calculation
current_age = st.number_input("Enter your current age", min_value=0, key="current_age")
retirement_age = st.number_input("Enter your desired retirement age", min_value=current_age + 1, key="retirement_age")
monthly_income = st.number_input("Enter your monthly income after tax", min_value=0.0, key="monthly_income")
monthly_expenses = st.number_input("Enter your monthly expenses", min_value=0.0, key="monthly_expenses")
rate_of_return = st.number_input("Rate of return (%)", min_value=0.0, max_value=100.0, value=5.0, key="rate_of_return")
st.write("Note: For stock market investments, 6-7% is the average rate of return; for savings, input the interest rate of your savings account.")

# Calculate retirement net worth
monthly_contributions = monthly_income - monthly_expenses
years_to_retirement = retirement_age - current_age
months_to_retirement = years_to_retirement * 12
rate_of_return_monthly = rate_of_return / 100 / 12

# Compound interest calculation
if rate_of_return_monthly > 0:
    retirement_net_worth = monthly_contributions * ((1 + rate_of_return_monthly) ** months_to_retirement - 1) / rate_of_return_monthly
else:
    retirement_net_worth = monthly_contributions * months_to_retirement

if st.button("Calculate Retirement Net Worth"):
    st.write(f"Your estimated retirement net worth at age {retirement_age} is: ${retirement_net_worth:,.2f}")

# Function to plot the timeline
def plot_timeline():
    today = date.today()
    current_year = today.year
    years = list(range(current_age, retirement_age + 1))
    years_as_dates = [current_year + (age - current_age) for age in years]
    
    # Create a DataFrame for the timeline
    timeline_df = pd.DataFrame({'Age': years, 'Year': years_as_dates})
    
    # Plot the timeline
    try:
        fig = px.scatter(timeline_df, x='Year', y=[0]*len(timeline_df), text='Age', title="Life Timeline")
        fig.update_layout(
            showlegend=False,
            yaxis=dict(visible=False),  # Hide the y-axis
            xaxis_title="Year",
            xaxis=dict(
                tickmode='array',
                tickvals=[years_as_dates[0], years_as_dates[-1]],
                ticktext=[str(years_as_dates[0]), str(years_as_dates[-1])],
                showticklabels=True  # Show labels only at the ends
            ),
            title=dict(x=0.5)  # Center the title
        )
        
        # Add red dots at current age and retirement age
        fig.add_scatter(
            x=[current_year + (current_age - current_age), current_year + (retirement_age - current_age)],
            y=[0, 0],
            mode='markers+text',
            marker=dict(size=12, color='red'),
            text=[current_age, retirement_age],
            textposition='top center',
            showlegend=False
        )
        
        # Update text position
        fig.update_traces(textposition='top center')
        
        st.plotly_chart(fig)
    except ValueError as e:
        st.write(f"Error plotting the timeline: {e}")

# Call the plot function
plot_timeline()
