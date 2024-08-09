import streamlit as st

# Title of the application
st.title("Simple Calculator")

# Input fields for the two numbers
num1 = st.number_input("masukan angka pertama", value=0.0)
num2 = st.number_input("masukan angka kedua", value=0.0)

# Dropdown menu for the operation
operation = st.selectbox("Pilih Operasi", ["+", "-", "x", "/"])

# Perform calculation based on the selected operation
if st.button("Calculate"):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "x":
        result = num1 * num2
    elif operation == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Error: pembagian dengan nol tidak boleh."
    
    # Display the result
    st.write(f"hasil: {result}")
