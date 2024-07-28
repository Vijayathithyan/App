This web application is designed to help you identify potential anomalies in your accounting data by applying Benford's Law. Benford's Law describes the frequency distribution of leading digits in many real-world datasets. Deviations from this Law can indicate potential data irregularities.
How to Use the App

1.	Upload Your Data:
•	Click the "Upload CSV" button to select the CSV file containing your accounting data.
•	Ensure the file is correctly formatted with a header row specifying column names.

2.	Select Column:
•	Choose the column from the dropdown list that contains the accounting figures you want to analyze.

3.	Data Cleaning:
•	The app automatically converts data to the appropriate numeric format and handles missing values.

4.	First Digit Analysis:
•	The app calculates the frequency distribution of the first digits in your selected data.
•	It compares this distribution to the expected Benford's Law distribution.
•	A Chi-square test is performed to determine if the observed distribution significantly differs from the expected distribution.
•	If the Chi-square test is insignificant, a Mean Absolute Difference (MAD) test is performed to identify digits with the most significant deviations from Benford's Law.

5.	Second Digit Analysis:
•	The app repeats the analysis for the second digits, following the same steps as for the first digits.

Interpretation of Results
•	Chi-square test:
•	A non-significant result suggests the data follows Benford's Law.
•	A significant result indicates potential anomalies.
•	Mean Absolute Difference (MAD) test:
•	Digits with a high MAD value deviate significantly from Benford's Law and warrant further investigation.

Additional Features
•	Threshold for MAD:
•	You can set a threshold value for the MAD test to filter results based on your desired level of sensitivity.

Disclaimer
This app is a tool for potential anomaly detection and should not be solely relied upon for fraud detection or financial analysis. Human expertise is essential in interpreting results and making informed decisions.

Note: The app assumes the uploaded CSV file contains numerical data in the selected column. If the data contains non-numeric values, the app may encounter errors.

By using this app, you agree to the following:
•	The data you upload will be processed solely for this analysis.
•	You are responsible for ensuring the accuracy and legality of the data you upload.

For any issues or questions, please contact vijay.adhi@gmail.com.
