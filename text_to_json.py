import json
import time
from tqdm import tqdm  # Progress tracking library
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from google.api_core.exceptions import ResourceExhausted  # Import ResourceExhausted exception

# Define the LLM using GoogleGenerativeAI
llm = GoogleGenerativeAI(google_api_key="AIzaSyAb4J9QUnpptQh74JOMxL1X8VPk1y20CWY", model="gemini-1.5-flash")

# Define the prompt template
template = """
Extract the following information from the text provided:
- Name
- Overall Score
- Reading Score
- Writing Score
- Listening Score
- Speaking Score
- Date of Examination

Please handle potential misspellings, such as:
- "Writing" may be spelled as "riting" or similar variations.
- "Reading" may appear as "reding" or other variations.
- "Listening" may appear as "listning" or other variations.
- "Speaking" may appear as "spaking" or other variations.

If you find a combined value for Reading and Writing, please apply the same score to both fields.

Ignore any occurrences of "Use of English" and its associated score. Do not include it in the final extracted data.

Most of the scores for Reading, Writing, Listening, and Speaking might be sequential and listed one under the other. Use this pattern to help locate and extract the values correctly.

Ensure that if any data is not available in the text, return "N/A". Also, make sure that the extracted scores and values are accurate based on the text context.

Text to extract from:
{input_text}
"""

# Create a PromptTemplate object
prompt_template = PromptTemplate(input_variables=["input_text"], template=template)

# Create an LLMChain object using the prompt and the LLM
llm_chain = LLMChain(llm=llm, prompt=prompt_template)

class NLPProcessor:
    """
    A class to handle text processing and data extraction using GoogleGenerativeAI and Langchain.
    """

    def __init__(self):
        self.extracted_data = {}

    def extract_data_from_text(self, input_text, retries=5, initial_delay=10):
        """
        Use GoogleGenerativeAI to extract structured data from a given input text.
        Implements retry logic with exponential backoff in case of resource exhaustion (429 error).
        """
        delay = initial_delay

        for attempt in tqdm(range(retries), desc="Retrying LLM Request"):
            try:
                # Attempt to run the LLMChain to extract data
                result = llm_chain.run(input_text)
                return result
            except ResourceExhausted as e:
                print(f"Resource exhausted. Attempt {attempt + 1} of {retries}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait for the specified delay before retrying
                delay *= 2  # Exponential backoff - double the delay after each retry
            except Exception as e:
                print(f"An error occurred: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait for the specified delay before retrying
                delay *= 2  # Exponential backoff

        raise Exception("Max retries exceeded. Could not extract data due to resource exhaustion.")

    def process_txt_file(self, txt_file, json_output_file):
        """
        Read a .txt file, extract structured data using the GoogleGenerativeAI model, and save it to a JSON file.
        """
        all_data = []

        # Read the .txt file
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        # Split the content of the text file by sections if needed
        sections = []
        current_section = []

        for line in lines:
            if line.startswith("--- Extracted Text from"):
                # If a new section starts, save the current section
                if current_section:
                    sections.append(current_section)
                    current_section = []
            current_section.append(line)

        # Append the last section
        if current_section:
            sections.append(current_section)

        # Process each section separately
        for section in tqdm(sections, desc="Processing Sections"):
            # Join the section content into a single string for LLM input
            input_text = "\n".join(section)

            # Extract structured data using the GoogleGenerativeAI model with retry
            extracted_data = self.extract_data_from_text(input_text)

            # Convert the extracted data into a structured format
            structured_data = self.format_extracted_data(extracted_data)

            # Add the structured data to the list
            all_data.append(structured_data)

        # Save all structured data to a JSON file
        with open(json_output_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        print(f"Organized data saved to {json_output_file}")

    def format_extracted_data(self, extracted_text):
        """
        Convert the raw extracted text into a structured format for JSON output.
        """

        # Default structure in case data is missing
        structured_data = {
            "Name": "N/A",
            "Overall Score": "N/A",
            "Reading Score": "N/A",
            "Writing Score": "N/A",
            "Listening Score": "N/A",
            "Speaking Score": "N/A",
            "Date of Examination": "N/A",
            "Date of Issue": "N/A"
        }

        # Extract information from the result (you can adjust parsing based on the actual output)
        for line in extracted_text.split('\n'):
            if "Name" in line:
                structured_data["Name"] = line.split(":")[1].strip()
            elif "Overall Score" in line:
                structured_data["Overall Score"] = line.split(":")[1].strip()
            elif "Reading Score" in line:
                structured_data["Reading Score"] = line.split(":")[1].strip()
            elif "Writing Score" in line:
                structured_data["Writing Score"] = line.split(":")[1].strip()
            elif "Listening Score" in line:
                structured_data["Listening Score"] = line.split(":")[1].strip()
            elif "Speaking Score" in line:
                structured_data["Speaking Score"] = line.split(":")[1].strip()
            elif "Date of Examination" in line:
                structured_data["Date of Examination"] = line.split(":")[1].strip()
            elif "Date of Issue" in line:
                structured_data["Date of Issue"] = line.split(":")[1].strip()

        return structured_data
