import os
from pypdf import PdfReader

def extract_first_page_text(pdf_path):
    """Extract text from the first page of a PDF file."""
    try:
        pdf = PdfReader(pdf_path)
        if len(pdf.pages) > 0:
            first_page = pdf.pages[0]  # Access the first page directly
            return first_page.extract_text() or "No text found on the first page."
        else:
            return "No pages found in the PDF."
    except Exception as e:
        return f"Error reading {pdf_path}: {str(e)}"

def list_and_sort_pdfs(directory_path):
    """List all PDF files in the directory and sort them chronologically by filename."""
    pdf_files = [f for f in os.listdir(directory_path) if f.lower().endswith('.pdf')]
    # Sort files by name
    pdf_files.sort()
    return pdf_files

def process_pdfs(directory_path):
    """Process all PDFs in the directory, extracting text from the first page and returning a dictionary of results."""
    pdf_files = list_and_sort_pdfs(directory_path)
    results = {}
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(directory_path, pdf_file)
        text = extract_first_page_text(pdf_path)
        results[pdf_file] = text
    
    return results

def save_results_to_txt(results, output_file_path):
    """Save the filenames and their corresponding extracted texts to a .txt file."""
    with open(output_file_path, 'a', encoding='utf-8') as file:
        for filename, text in results.items():
            file.write(f"Filename: {filename}\n")
            file.write(f"Text:\n{text}\n")
            file.write("="*40 + "\n")

def main(directory_paths, output_file_path):
    """Main function to process PDFs and save results."""
    total_files_processed = 0
    
    for directory_path in directory_paths:
        results = process_pdfs(directory_path)
        save_results_to_txt(results, output_file_path)
        total_files_processed += len(results)
        print(f"Results from {directory_path} successfully written to {output_file_path}")
    
    print(f"Total number of files processed: {total_files_processed}")

if __name__ == "__main__":
    # Define the list of directory paths
    root_directory = '/home/stefan/Desktop/zjzpa'
    directory_paths = [os.path.join(root_directory, d) for d in os.listdir(root_directory) if os.path.isdir(os.path.join(root_directory, d))]
    
    # Define the output file path
    output_file_path = '/home/stefan/Desktop/zjzpa-analiza-main/main/output.txt'
    
    # Call the main function
    main(directory_paths, output_file_path)

