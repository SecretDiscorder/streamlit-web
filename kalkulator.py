import streamlit as st

# Initialize session state for calculator
if "current_input" not in st.session_state:
    st.session_state.current_input = ""
if "operation" not in st.session_state:
    st.session_state.operation = None
if "num1" not in st.session_state:
    st.session_state.num1 = None

# Function to handle button clicks
def handle_button_click(value):
    if value in ["+", "-", "x", "/"]:
        st.session_state.num1 = st.session_state.current_input
        # Convert 'x' to '*' for internal calculations
        st.session_state.operation = "*" if value == "x" else value
        st.session_state.current_input = ""
    elif value == "=":
        if st.session_state.num1 is not None and st.session_state.operation is not None:
            try:
                num1 = int(st.session_state.num1)  # Convert to integer
                num2 = int(st.session_state.current_input)  # Convert to integer
                if st.session_state.operation == "+":
                    result = num1 + num2
                elif st.session_state.operation == "-":
                    result = num1 - num2
                elif st.session_state.operation == "*":
                    result = num1 * num2
                elif st.session_state.operation == "/":
                    if num2 != 0:
                        result = num1 // num2  # Use integer division
                    else:
                        result = "Error: pembagian dengan nol tidak boleh."
                else:
                    result = "Error: operasi tidak valid."
            except ValueError:
                result = "Error: input tidak valid."
            
            st.session_state.current_input = str(result)
            st.session_state.num1 = None
            st.session_state.operation = None
        else:
            st.session_state.current_input = "Error: operasi tidak lengkap."
    elif value == "C":
        st.session_state.current_input = ""
        st.session_state.num1 = None
        st.session_state.operation = None
    else:
        st.session_state.current_input += value

# Title of the application
st.title("Kalkulator Sederhana")

# Display current input and result in a text area
st.text_area("Input", value=st.session_state.current_input, height=50, max_chars=100, key="text_area", disabled=False)

# Create a layout for the calculator using button cards
buttons = [
    ("1", "1"), ("2", "2"), ("3", "3"), ("+", "+"),
    ("4", "4"), ("5", "5"), ("6", "6"), ("-", "-"),
    ("7", "7"), ("8", "8"), ("9", "9"), ("x", "x"),
    ("C", "C"), ("0", "0"), (".", "."), ("/", "/"),
    ("=", "=")
]

# Create a grid of buttons
n_cols = 4
for i in range(0, len(buttons), n_cols):
    cols = st.columns(n_cols)
    for j, (label, value) in enumerate(buttons[i:i + n_cols]):
        with cols[j]:
            st.button(label, key=label, use_container_width=True, on_click=handle_button_click, args=(value,))

