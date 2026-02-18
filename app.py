import streamlit as st
import medical_data_visualizer

# Set the page title
st.set_page_config(page_title="Medical Data Visualizer", layout="wide")

st.title("🩺 Medical Data Analysis Dashboard")
st.markdown("""
This app visualizes medical examination data to identify correlations 
between lifestyle, health markers, and cardiovascular disease.
""")

# Add a sidebar for navigation
option = st.sidebar.selectbox(
    'Which plot would you like to see?',
    ('Home', 'Categorical Plot', 'Correlation Heat Map')
)

if option == 'Home':
    st.write("### Raw Data Preview")
    # Access the dataframe from your module
    st.dataframe(medical_data_visualizer.df.head(10))
    st.write("Use the sidebar to view specific visualizations.")

elif option == 'Categorical Plot':
    st.subheader("Categorical Features Split by Cardio")
    with st.spinner('Generating plot...'):
        fig = medical_data_visualizer.draw_cat_plot()
        st.pyplot(fig)
    st.info("This plot shows the counts of good/bad outcomes for features like cholesterol and glucose.")

elif option == 'Correlation Heat Map':
    st.subheader("Health Feature Correlation Heat Map")
    with st.spinner('Calculating correlations...'):
        fig = medical_data_visualizer.draw_heat_map()
        st.pyplot(fig)
    st.info("The heat map shows how different health metrics (like weight and blood pressure) relate to each other.")