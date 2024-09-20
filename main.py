import os
from ocr_extraction import process_images  # Extract text to a single .txt file
from text_to_json import NLPProcessor  # Extract structured data using Langchain & Gemini and save to a JSON file
from json_to_Excel import combine_json_to_excel  # Combine the single JSON file into an Excel file
from excel_to_sql import excel_to_sql  # Import the new function to convert Excel to SQL

def main(images_folder, txt_file, json_file, output_folder):
    """
    Main function to process images, save OCR results as a single text file, 
    then organize text into a single JSON file using Gemini, and finally combine JSON into an Excel file.
    """
    # Step 1: Process images and save OCR results to a single .txt file
    process_images(images_folder, txt_file)

    # Step 2: Process the .txt file and extract structured data using the Gemini API via Langchain
    processor = NLPProcessor()
    processor.process_txt_file(txt_file, json_file)

    # Step 3: Combine the single JSON file into an Excel file
    output_excel_file = os.path.join(output_folder, "combined_json_data.xlsx")
    combine_json_to_excel([json_file], output_excel_file)
    print(f"Excel file saved to {output_excel_file}")

    # Step 4: Convert the Excel file to an SQL database
    db_file = os.path.join(output_folder, "output_database.db")  # Path for the SQL database
    table_name = "ocr_data"  # Name of the SQL table to store data
    excel_to_sql(output_excel_file, db_file, table_name)
    print(f"SQL database created at {db_file}")

if __name__ == "__main__":
    # Paths to folders and files
    images_folder = 'Images/English'  # Path to folder with images
    txt_file = 'Output/Txt/Final.txt'  # Single text file for saving all extracted text
    json_file = 'Output/Json/Final.json'  # Single JSON file for saving all organized data
    output_folder = 'Output/Data'  # Path to folder for saving the final Excel output and the SQL database

    # Run the main process
    main(images_folder, txt_file, json_file, output_folder)
