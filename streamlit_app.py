import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Financial Tool class
class FinancialTool:
    def __init__(self, current_age, retirement_age, checking_balance, savings_balance, investment_balance, income_after_tax, expenses):
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.checking_balance = checking_balance
        self.savings_balance = savings_balance
        self.investment_balance = investment_balance
        self.income_after_tax = income_after_tax
        self.expenses = expenses
        self.goals = []
        self.interest_rate = 0.03  # Annual compounding interest rate of 3%

    def add_goal(self, label, amount, age):
        self.goals.append({
            "label": label,
            "amount": amount,
            "age": age
        })

    def calculate_allocation(self):
        """Calculate the amount needed monthly to achieve each goal and the remaining amount for retirement."""
        total_months = (self.retirement_age - self.current_age) * 12
        monthly_savings = self.income_after_tax - self.expenses

        if monthly_savings <= 0:
            raise ValueError("Monthly savings amount is not enough to cover expenses. Please adjust your inputs.")

        goal_contributions = []
        total_goal_amount = sum(goal["amount"] for goal in self.goals)
        
        if total_goal_amount > monthly_savings * total_months:
            raise ValueError("Not enough funds to cover all goals with current income and expenses.")

        for goal in self.goals:
            months_to_goal = (goal["age"] - self.current_age) * 12
            required_contribution = goal["amount"] / ((1 + self.interest_rate / 12) ** months_to_goal - 1) * (self.interest_rate / 12)
            goal_contributions.append(required_contribution)

        remaining_for_retirement = monthly_savings - sum(goal_contributions)
        return goal_contributions, remaining_for_retirement

    def compound_interest(self, principal, monthly_contribution, years):
        """Calculate compound interest monthly."""
        months = years * 12
        monthly_rate = self.interest_rate / 12
        total = principal * (1 + monthly_rate) ** months + monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        return total

    def calculate_net_worth_at_retirement(self):
        """Calculate final net worth at retirement."""
        total_months = (self.retirement_age - self.current_age) * 12
        goal_contributions, remaining_for_retirement = self.calculate_allocation()
        
        total_savings = self.compound_interest(self.savings_balance, remaining_for_retirement, self.retirement_age - self.current_age)
        total_investments = self.compound_interest(self.investment_balance, remaining_for_retirement, self.retirement_age - self.current_age)

        net_worth = self.checking_balance + total_savings + total_investments
        net_worth_post_tax = net_worth * 0.5  # 50% capital gains tax
        return net_worth, net_worth_post_tax, goal_contributions

    def plot_timeline(self, goal_contributions, net_worth, net_worth_post_tax):
        """Plot the results."""
        ages = np.arange(self.current_age, self.retirement_age + 1)
        plt.figure(figsize=(10, 6))

        # Plot timeline
        plt.axhline(0, color='black', linewidth=0.5)
        plt.scatter([self.current_age, self.retirement_age], [0, 0], color='black', zorder=5)

        for goal in self.goals:
            plt.scatter(goal["age"], 0, color='red', zorder=5)
            plt.text(goal["age"], 0.02, f'{goal["label"]}: ${goal["amount"]:.2f}', ha='center')

        plt.text(self.current_age, -0.02, f'Current Age\n${self.checking_balance + self.savings_balance + self.investment_balance:.2f}', ha='center')
        plt.text(self.retirement_age, -0.02, f'Retirement Age\nPre-tax: ${net_worth:.2f}\nPost-tax: ${net_worth_post_tax:.2f}', ha='center')

        plt.xticks(np.arange(self.current_age, self.retirement_age + 1, 1))
        plt.yticks([])

        plt.title('Financial Timeline')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        st.pyplot(plt)


# Streamlit interface for the Financial Tool
st.title("Financial Planning Tool")

# Inputs for user data
current_age = st.number_input("Current Age:", min_value=18, max_value=100, value=30)
retirement_age = st.number_input("Estimated Retirement Age:", min_value=current_age + 1, max_value=100, value=65)
checking_balance = st.number_input("Current Checking Balance ($):", min_value=0.0, value=5000.0)
savings_balance = st.number_input("Current Savings Balance ($):", min_value=0.0, value=20000.0)
investment_balance = st.number_input("Current Investment Balance ($):", min_value=0.0, value=50000.0)
income_after_tax = st.number_input("Monthly Income After Tax ($):", min_value=0.0, value=3000.0)
expenses = st.number_input("Monthly Expenses ($):", min_value=0.0, value=2000.0)

# Add Goals
goals = []
if st.button("Add a Goal"):
    with st.form("goal_form"):
        goal_label = st.text_input("Goal Label:")
        goal_amount = st.number_input("Amount Needed for Goal ($):", min_value=0.0)
        goal_age = st.number_input("Age to Reach Goal:", min_value=current_age, max_value=retirement_age)
        submit_goal = st.form_submit_button("Submit")
        if submit_goal:
            goals.append({"label": goal_label, "amount": goal_amount, "age": goal_age})
            st.success(f"Goal '{goal_label}' added!")

# Financial calculation
if st.button("Calculate"):
    financial_tool = FinancialTool(current_age, retirement_age, checking_balance, savings_balance, investment_balance, income_after_tax, expenses)
    
    for goal in goals:
        financial_tool.add_goal(goal['label'], goal['amount'], goal['age'])

    try:
        goal_contributions, remaining_for_retirement = financial_tool.calculate_allocation()
        net_worth, net_worth_post_tax, _ = financial_tool.calculate_net_worth_at_retirement()

        # Display results
        st.subheader("Results")
        st.write(f"Net worth at retirement age (pre-tax): ${net_worth:.2f}")
        st.write(f"Net worth at retirement age (post-tax): ${net_worth_post_tax:.2f}")

        # Plot timeline
        financial_tool.plot_timeline(goal_contributions, net_worth, net_worth_post_tax)

    except ValueError as e:
        st.error(f"Error: {str(e)}")

