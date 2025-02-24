import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Growth", layout="wide")
st.markdown("""
<style>
.stApp{
    padding: 0;
    background-color: black;
    color: white;
    font-family: "Arial", sans-serif;
}
</style>
""", unsafe_allow_html=True)


#title and description
st.title("📊 Datasweeper Sterling Integrator By Farah Almas 🚀")
st.write("This app allows you to upload your files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for the project-1")


#upload file
uploaded_files = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == "xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file name: {file_extension }")
            continue

        #file details
        st.write(f"Processing file: {file.name}")
        st.dataframe(df.head())

        #data cleaning
        st.subheader("Data Cleaning")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from the file : {file.name}"):
                    df = df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully")
            with col2:
                if st.button(f"Remove missing values from the file : {file.name}"):
                   numeric_cols = df.select_dtypes(include=['number']).columns
                   df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                   st.write("✅ Missing values removed successfully")


        st.subheader("select Columns to Keep")
        columns = st.multiselect(f"Select columns for {file.name}", df.columns,default = df.columns)
        df = df[columns]

        #data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show data visualization for {file.name}"):
           st.bar_chart(df.select_dtypes(include=['number']).iloc[:,2])


        #conversion options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"convert {file.name} to",["Excel","CSV"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
              df.to_csv(buffer, index=False)
              file_name = file.name.replace(file_extension,".csv")
              mime = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_extension,".xlsx")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            st.download_button(
                label = f"Download {conversion_type} file", 
                data = buffer,
                file_name = file_name,
                mime = mime
                )
st.success("✅ All files have been processed successfully")


























