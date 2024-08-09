import streamlit as st
import matplotlib.pyplot as plt #import matplotlib untuk visualisasi data

# Title of the application
st.title('Visual Data Diagram Lingkaran')

# Sidebar inputs for the pie chart
st.sidebar.header('Input Data')

# irisan angka dengan minimal 1 maximal 10 
num_slices = st.sidebar.slider('Number of slices', min_value=1, max_value=10, value=3) 

# Labels and sizes
labels = [] #label
sizes = [] #ukuran

for i in range(num_slices):
    label = st.sidebar.text_input(f'Label for slice {i+1}', f'Slice {i+1}', key=f'label_{i}')
    size = st.sidebar.number_input(f'Size for slice {i+1}', min_value=1, max_value=100, value=10, key=f'size_{i}')
    
    labels.append(label)
    sizes.append(size)
    
# Plot pie chart
if st.sidebar.button('Hasilkan data diagram'):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # menyamakan rasio aspek agar terbentuk pie chart
    
    st.pyplot(fig)
    