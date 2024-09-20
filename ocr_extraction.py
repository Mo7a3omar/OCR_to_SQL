import os
from PIL import Image
import pytesseract

# Function to extract and structure text from an image using pytesseract
def extract_text_from_image(image_path):
    # Extract text from image using pytesseract in English
    extracted_text = pytesseract.image_to_string(Image.open(image_path), lang='eng')
    
    # Structuring the extracted text by adding separation between sections
    structured_text = "\n".join([line.strip() for line in extracted_text.splitlines() if line.strip()])

    return structured_text

# Process all images in a folder and save all structured text in one .txt file
def process_images(images_folder, txt_output_file):
    with open(txt_output_file, 'w', encoding='utf-8') as output_file:
        for image_filename in os.listdir(images_folder):
            if image_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(images_folder, image_filename)
                
                # Perform OCR and get structured text
                structured_text = extract_text_from_image(image_path)

                # Write structured text to a single file with a separator
                output_file.write(f"\n--- Extracted Text from {image_filename} ---\n")
                output_file.write(structured_text + "\n")

    print(f"All text saved to {txt_output_file}")

# Example usage
if __name__ == "__main__":
    images_folder = 'Images/English'  # Folder containing images
    txt_output_file = 'Output/Txt/all_extracted_text.txt'  # Single text file for all images

    # Run the process
    process_images(images_folder, txt_output_file)
