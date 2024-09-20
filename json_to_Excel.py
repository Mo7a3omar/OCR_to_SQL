import json
import pandas as pd

# Function to combine JSON files into an Excel file
def combine_json_to_excel(json_files, output_excel_file):
    """
    Combine multiple JSON files into one Excel file.
    Each JSON file corresponds to a row, and the keys form the columns.
    """
    combined_data = []

    # Extract data from each JSON file and flatten the structure into a row format
    for json_file in json_files:
        data = extract_important_data_from_json(json_file)
        # In case the JSON contains a list of dictionaries, we need to flatten it properly
        if isinstance(data, list):
            combined_data.extend(data)
        else:
            combined_data.append(data)

    # Create a DataFrame from the combined data
    df = pd.DataFrame(combined_data)
    
    # List of expected columns
    expected_columns = ['Name', 'Overall Score', 'Reading', 'Writing', 'Listening', 'Speaking', 'Date of Examination']
    
    # Ensure all expected columns are present, adding any missing columns with empty values
    for col in expected_columns:
        if col not in df.columns:
            df[col] = ""  # Add missing column with empty values
    
    # Reorder columns to match the expected order
    df = df[expected_columns]
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_excel_file, index=False)
    print(f"Combined data saved to {output_excel_file}")

# Function to extract important data from JSON
def extract_important_data_from_json(json_file):
    """
    Extract important data from the OCR JSON files.
    Handle both single dictionaries and lists of dictionaries.
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # If the data is a list of dictionaries, process each dictionary
    if isinstance(data, list):
        extracted_data = []
        for entry in data:
            structured_data = {
                'Name': entry.get('Name', 'N/A'),
                'Overall Score': entry.get('Overall Score', 'N/A'),
                'Reading': entry.get('Reading Score', 'N/A'),
                'Writing': entry.get('Writing Score', 'N/A'),
                'Listening': entry.get('Listening Score', 'N/A'),
                'Speaking': entry.get('Speaking Score', 'N/A'),
                'Date of Examination': entry.get('Date of Examination', 'N/A'),
            }
            extracted_data.append(structured_data)
        return extracted_data

    # If the data is a single dictionary, return the structured data directly
    structured_data = {
        'Name': data.get('Name', 'N/A'),
        'Overall Score': data.get('Overall Score', 'N/A'),
        'Reading': data.get('Reading Score', 'N/A'),
        'Writing': data.get('Writing Score', 'N/A'),
        'Listening': data.get('Listening Score', 'N/A'),
        'Speaking': data.get('Speaking Score', 'N/A'),
        'Date of Examination': data.get('Date of Examination', 'N/A'),
    }
    return [structured_data]  # Return as a list to maintain consistency
