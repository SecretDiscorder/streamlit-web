import streamlit as st
import math
from decimal import Decimal
import roman

# Initialize session state for calculator
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Function to handle button clicks
def handle_button_click(value):
    if value == "=":
        try:
            # Evaluate the expression entered by the user
            # Replace '^' with '**' for exponentiation
            expression = st.session_state.expression.replace('x', '*').replace('^', '**')
            result = eval(expression)
            st.session_state.expression = str(result)
        except Exception as e:
            st.session_state.expression = f"Error: {str(e)}"
    elif value == "C":
        st.session_state.expression = ""
    else:
        st.session_state.expression += value

# Functions for additional features
def perform_operation(operation, expression):
    try:
        if operation == "log":
            a, b = map(float, expression.split())
            if b == 10:
                result = math.log10(a)
            else:
                result = math.log(a, b)
        elif operation == "to_roman":
            result = roman.toRoman(int(expression))
        elif operation == "from_roman":
            result = roman.fromRoman(expression)
        elif operation == "sin":
            result = math.sin(float(expression))
        elif operation == "cos":
            result = math.cos(float(expression))
        elif operation == "tan":
            result = math.tan(float(expression))
        elif operation == "factorial":
            result = math.factorial(int(expression))
        elif operation == "c_to_f":
            result = (float(expression) * 9/5) + 32
        elif operation == "f_to_c":
            result = (float(expression) - 32) * 5/9
        elif operation == "c_to_k":
            result = float(expression) + 273.15
        elif operation == "k_to_c":
            result = float(expression) - 273.15
        elif operation == "binary":
            result = format(int(expression), "b")
        elif operation == "num":
            result = int(expression, 2)
        elif operation == "sqrt":
            result = math.sqrt(float(expression))
        else:
            result = "Error: Operation not supported."
    except Exception as e:
        result = f"Error: {str(e)}"
    return result

# Title of the application
st.title("Kalkulator Kompleks")

# Display current input and result in a text area
st.text_area("Input", value=st.session_state.expression, height=50, max_chars=100, key="text_area", disabled=False)

# Create a layout for the calculator using button cards
buttons = [
    ("1", "1"), ("2", "2"), ("3", "3"), ("+", "+"),
    ("4", "4"), ("5", "5"), ("6", "6"), ("-", "-"),
    ("7", "7"), ("8", "8"), ("9", "9"), ("x", "x"),
    ("C", "C"), ("0", "0"), (".", "."), ("/", "/"),
    ("^", "^"), ("=", "=")
]

# Create a grid of buttons
n_cols = 4
for i in range(0, len(buttons), n_cols):
    cols = st.columns(n_cols)
    for j, (label, value) in enumerate(buttons[i:i + n_cols]):
        with cols[j]:
            st.button(label, key=label, use_container_width=True, on_click=handle_button_click, args=(value,))

# Additional features inputs
st.write("### Additional Operations")
operation = st.selectbox("Select Operation", [
    "None", "log", "to_roman", "from_roman", "sin", "cos", "tan", "factorial", 
    "c_to_f", "f_to_c", "c_to_k", "k_to_c", "binary", "num", "sqrt"
])
expression = st.text_input("Enter Expression")

if st.button("Calculate"):
    if operation != "None":
        result = perform_operation(operation, expression)
        st.write(f"**Result:** {result}")
    else:
        st.write("Select an operation from the dropdown.")

