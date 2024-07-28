import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Benford's distributions
benford_first_digit = {1: 0.301, 2: 0.176, 3: 0.125, 4: 0.097, 5: 0.079, 6: 0.067, 7: 0.058, 8: 0.051, 9: 0.046}
benford_second_digit = {0: 0.1197, 1: 0.1139, 2: 0.1088, 3: 0.1043, 4: 0.1003, 5: 0.0967, 6: 0.0934, 7: 0.0904, 8: 0.0876, 9: 0.0850}

# Title and instructions
st.title("Fraud Detection in Accounts Using Benford’s Law by Vijayathithyan B B")
st.write("""
This web application is designed to help you identify potential anomalies in your accounting data by applying Benford's Law. 
Benford's Law describes the frequency distribution of leading digits in many real-world datasets. Deviations from this Law can indicate potential data irregularities.

**How to Use the App**
1. **Upload Your Data**:
   - Click the "Upload CSV" button to select the CSV file containing your accounting data.
   - Ensure the file is correctly formatted with a header row specifying column names.
2. **Select Column**:
   - Choose the column from the dropdown list that contains the accounting figures you want to analyze.
3. **Data Cleaning**:
   - The app automatically converts data to the appropriate numeric format and handles missing values.
4. **First Digit Analysis**:
   - The app calculates the frequency distribution of the first digits in your selected data.
   - It compares this distribution to the expected Benford's Law distribution.
   - A Chi-square test is performed to determine if the observed distribution significantly differs from the expected distribution.
   - If the Chi-square test is insignificant, a Mean Absolute Difference (MAD) test is performed to identify digits with the most significant deviations from Benford's Law.
5. **Second Digit Analysis**:
   - The app repeats the analysis for the second digits, following the same steps as for the first digits.

**Interpretation of Results**
- **Chi-square test**:
  - A non-significant result suggests the data follows Benford's Law.
  - A significant result indicates potential anomalies.
- **Mean Absolute Difference (MAD) test**:
  - Digits with a high MAD value deviate significantly from Benford's Law and warrant further investigation.

**Additional Features**
- **Threshold for MAD**:
  - You can set a threshold value for the MAD test to filter results based on your desired level of sensitivity.

**Disclaimer**
This app is a tool for potential anomaly detection and should not be solely relied upon for fraud detection or financial analysis. Human expertise is essential in interpreting results and making informed decisions.
Note: The app assumes the uploaded CSV file contains numerical data in the selected column. If the data contains non-numeric values, the app may encounter errors.
By using this app, you agree to the following:
- The data you upload will be processed solely for this analysis.
- You are responsible for ensuring the accuracy and legality of the data you upload.

For any issues or questions, please contact vijay.adhi@gmail.com.
""")

# File upload
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    columns = df.columns.tolist()
    
    # Select column
    selected_column = st.selectbox("Select Column", columns)
    
    if selected_column:
        data = df[selected_column].dropna()
        data = pd.to_numeric(data, errors='coerce').dropna()

        # Helper function to calculate first and second digit distributions
        def calculate_digit_distribution(data, position=1):
            if position == 1:
                digits = [int(str(abs(int(x)))[0]) for x in data if str(x)[0] != '0']
            elif position == 2:
                digits = [int(str(abs(int(x)))[1]) for x in data if len(str(x)) > 1]
            return pd.Series(digits).value_counts(normalize=True).sort_index()

        # First digit analysis
        first_digit_distribution = calculate_digit_distribution(data, position=1)
        first_digit_counts = first_digit_distribution * len(data)
        
        # Chi-square test for first digits
        first_digit_expected_counts = [benford_first_digit[d] * len(data) for d in range(1, 10)]
        first_digit_observed_counts = first_digit_counts.values
        chi2, p_value = chi2_contingency([first_digit_observed_counts, first_digit_expected_counts])[:2]
        
        # Display first digit results
        st.subheader("First Digit Analysis")
        st.write("**Observed First Digit Counts:**", first_digit_counts.to_dict())
        st.write("**Expected First Digit Counts (Benford's Law):**", dict(zip(range(1, 10), first_digit_expected_counts)))
        
        # Bar graph for first digits
        fig, ax = plt.subplots()
        ax.bar(range(1, 10), first_digit_counts, label='Observed', alpha=0.6, color='blue')
        ax.bar(range(1, 10), first_digit_expected_counts, label='Benford', alpha=0.6, color='red')
        ax.set_xlabel('First Digit')
        ax.set_ylabel('Count')
        ax.legend()
        st.pyplot(fig)
        
        # Chi-square test result
        st.write("**Chi-square Test Result for First Digit:**")
        st.write(f"Chi-square statistic: {chi2}, p-value: {p_value}")
        
        if p_value < 0.05:
            st.write("Significant association detected. Proceeding with Mean Absolute Difference test.")
            
            # MAD test for first digits
            mad_values = {d: abs(first_digit_distribution.get(d, 0) - benford_first_digit[d]) for d in range(1, 10)}
            st.write("**MAD Values for First Digits:**", mad_values)
            
            # MAD threshold selection
            mad_threshold = st.selectbox("Select MAD Threshold for First Digits", [0.000, 0.025, 0.05, 0.1])
            mad_outliers = {d: mad for d, mad in mad_values.items() if mad > mad_threshold}
            st.write("**Figures having the following numbers in their first digit are not in conformity with Benford’s Law:**", mad_outliers)
        
        else:
            st.write("No Anomalies detected in First-digit test.")
        
        # Second digit analysis
        second_digit_distribution = calculate_digit_distribution(data, position=2)
        second_digit_counts = second_digit_distribution * len(data)
        
        # Chi-square test for second digits
        second_digit_expected_counts = [benford_second_digit[d] * len(data) for d in range(10)]
        second_digit_observed_counts = second_digit_counts.values
        chi2, p_value = chi2_contingency([second_digit_observed_counts, second_digit_expected_counts])[:2]
        
        # Display second digit results
        st.subheader("Second Digit Analysis")
        st.write("**Observed Second Digit Counts:**", second_digit_counts.to_dict())
        st.write("**Expected Second Digit Counts (Benford's Law):**", dict(zip(range(10), second_digit_expected_counts)))
        
        # Bar graph for second digits
        fig, ax = plt.subplots()
        ax.bar(range(10), second_digit_counts, label='Observed', alpha=0.6, color='blue')
        ax.bar(range(10), second_digit_expected_counts, label='Benford', alpha=0.6, color='red')
        ax.set_xlabel('Second Digit')
        ax.set_ylabel('Count')
        ax.legend()
        st.pyplot(fig)
        
        # Chi-square test result
        st.write("**Chi-square Test Result for Second Digit:**")
        st.write(f"Chi-square statistic: {chi2}, p-value: {p_value}")
        
        if p_value < 0.05:
            st.write("Significant association detected. Proceeding with Mean Absolute Difference test.")
            
            # MAD test for second digits
            mad_values = {d: abs(second_digit_distribution.get(d, 0) - benford_second_digit[d]) for d in range(10)}
            st.write("**MAD Values for Second Digits:**", mad_values)
            
            # MAD threshold selection
            mad_threshold = st.selectbox("Select MAD Threshold for Second Digits", [0.000, 0.025, 0.05, 0.1])
            mad_outliers = {d: mad for d, mad in mad_values.items() if mad > mad_threshold}
            st.write("**Figures having the following numbers in their second digit are not in conformity with Benford’s Law:**", mad_outliers)
        
        else:
            st.write("No Anomalies detected in second-digit test.")
