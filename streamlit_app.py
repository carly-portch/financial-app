import streamlit as st

# Title of the app
st.title("Simple Calculator")

# Getting user input
st.header("Enter two numbers to calculate")

# Create two input fields for the numbers
num1 = st.number_input("Enter the first number", value=0)
num2 = st.number_input("Enter the second number", value=0)

# Dropdown menu for operations
operation = st.selectbox("Select operation", ("Add", "Subtract", "Multiply", "Divide"))

# Function to perform calculation
def calculate(num1, num2, operation):
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        if num2 != 0:
            return num1 / num2
        else:
            return "Cannot divide by zero"

# Button to perform calculation
if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.write(f"Result: {result}")

# Footer
st.write("Made with Streamlit")
