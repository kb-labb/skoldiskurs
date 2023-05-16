import re

def clean_text_file(input_file, output_file):
    # Open the input file for reading
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Remove non-Swedish letters and numbers
    cleaned_text = re.sub("[0-9]+", " ", text)
    cleaned_text = re.sub("[^A-Za-zåäöÖÅÄ\s]", " ", cleaned_text)
    
    # Open the output file for writing
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

    print("File cleaned and saved successfully.")

# Example usage:
input_file = 'big_corpus_lemma.txt'  # Replace with the actual input file name
output_file = 'cleaned_output_lemma.txt'  # Replace with the desired output file name

clean_text_file(input_file, output_file)