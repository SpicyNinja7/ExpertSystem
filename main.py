import os
import PyPDF2
import spacy


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Loading Database...")
    # Load the English language model in spaCy (there are small, medium, and large)
    #nlp = spacy.load('en_core_web_sm')
    #nlp = spacy.load('en_core_web_md')
    nlp = spacy.load('en_core_web_lg')

    # Set the path to the folder containing the PDF articles
    pdf_folder_path = 'Datasource\PDF'

    # Get a list of the PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]

    # Create a dictionary to store the text of each article
    articles = {}

    # Loop through each PDF file in the folder
    for pdf_file in pdf_files:
        # Open the PDF file in read-binary mode
        with open(os.path.join(pdf_folder_path, pdf_file), 'rb') as f:
            # Read the PDF file with PyPDF2
            pdf_reader = PyPDF2.PdfReader(f)
            # Combine all pages of the article into one string
            article_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                article_text += page.extract_text()
            # Add the article text to the dictionary with the PDF file name as the key
            articles[pdf_file] = article_text

    # Ask the user to enter a question
    question = input("Please enter a question about the articles: ")

    # Define a threshold similarity score for a sentence to be considered a match
    threshold = 0.5

    # Create a list to store the candidate answers and their similarity scores
    candidate_answers = []

    # Loop through each PDF file and its associated text
    for pdf_file, article_text in articles.items():
        # Process the article text with spaCy
        doc = nlp(article_text)
        # Loop through each sentence in the text
        for sent in doc.sents:
            # Calculate the similarity score between the sentence and the user's question
            sim_score = sent.similarity(nlp(question))
            # Check if the similarity score is above the threshold
            if sim_score > threshold:
                # Append the sentence, its similarity score, and the PDF file name to the candidate answers list
                candidate_answers.append((sent.text, sim_score, pdf_file))

    # Sort the candidate answers by their similarity score in descending order
    sorted_answers = sorted(candidate_answers, key=lambda x: x[1], reverse=True)

    # Print the top 3 most relevant answers with their associated PDF file names
    num_answers = min(3, len(sorted_answers))
    for i in range(num_answers):
        print(f"Answer {i + 1} (from {sorted_answers[i][2]}): {sorted_answers[i][0]}")
