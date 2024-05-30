# -*- coding: utf-8 -*-
"""BlackCoffer_Test_Assignment

Name: Ritesh Kantule
BTech(2025) BSBE IIT Kanpur

"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import nltk
from textblob import TextBlob
import re

# Ensure the necessary NLTK data files are downloaded
nltk.download('stopwords')
nltk.download('punkt')

# Read the input Excel file
input_df = pd.read_excel('/kaggle/input/dataandstop/20211030 Test Assignment/Input.xlsx')  # I am using kaggle -> Change to actual path

# Create a directory to save the articles
os.makedirs('/kaggle/working/articles', exist_ok=True)

# Load positive and negative words
with open('/kaggle/input/dataandstop/20211030 Test Assignment/MasterDictionary/positive-words.txt', 'r', encoding='latin-1') as file:  # Change to actual path
    positive_words = set(file.read().split())
with open('/kaggle/input/dataandstop/20211030 Test Assignment/MasterDictionary/negative-words.txt', 'r', encoding='latin-1') as file:  # Change to actual path
    negative_words = set(file.read().split())

# Load stop words
stop_words = set()
for file_name in os.listdir('/kaggle/input/dataandstop/20211030 Test Assignment/StopWords/'):  # Change to actual path
    with open(f'/kaggle/input/dataandstop/20211030 Test Assignment/StopWords/{file_name}', 'r', encoding='latin-1') as file:  # Change to actual path
        stop_words.update(file.read().split())

# Function to extract article title and text with retry mechanism
def extract_article(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Assuming the title is in <h1> and the content in <p> tags
            title = soup.find('h1').get_text()
            paragraphs = soup.find_all('p')
            text = ' '.join([para.get_text() for para in paragraphs])

            return title, text
        except Exception as e:
            print(f"Error extracting {url} on attempt {attempt + 1}: {e}")
            time.sleep(2)
    return None, None

# Function to calculate syllables in a word
def count_syllables(word):
    word = word.lower()
    count = 0
    vowels = "aeiou"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

# Function to calculate text analysis variables
def analyze_text(text):
    blob = TextBlob(text)

    # Tokenize and remove stop words
    words = [word for word in blob.words if word.lower() not in stop_words]

    positive_score = sum(1 for word in words if word.lower() in positive_words)
    negative_score = sum(1 for word in words if word.lower() in negative_words)

    # POLARITY SCORE
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)

    # SUBJECTIVITY SCORE
    subjectivity_score = (positive_score + negative_score) / (len(words) + 0.000001)

    # AVG SENTENCE LENGTH
    sentences = blob.sentences
    avg_sentence_length = sum(len(sentence.words) for sentence in sentences) / len(sentences)

    # PERCENTAGE OF COMPLEX WORDS and COMPLEX WORD COUNT
    complex_words = [word for word in words if count_syllables(word) >= 3]
    complex_word_count = len(complex_words)
    percentage_of_complex_words = complex_word_count / len(words) * 100

    # FOG INDEX
    fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)

    # AVG NUMBER OF WORDS PER SENTENCE
    avg_number_of_words_per_sentence = avg_sentence_length

    # WORD COUNT
    word_count = len(words)

    # SYLLABLE PER WORD
    syllable_per_word = sum(count_syllables(word) for word in words) / word_count

    # PERSONAL PRONOUNS
    personal_pronouns = len(re.findall(r'\b(I|we|my|ours|us)\b', text, re.I))

    # AVG WORD LENGTH
    avg_word_length = sum(len(word) for word in words) / word_count

    return {
        'POSITIVE SCORE': positive_score,
        'NEGATIVE SCORE': negative_score,
        'POLARITY SCORE': polarity_score,
        'SUBJECTIVITY SCORE': subjectivity_score,
        'AVG SENTENCE LENGTH': avg_sentence_length,
        'PERCENTAGE OF COMPLEX WORDS': percentage_of_complex_words,
        'FOG INDEX': fog_index,
        'AVG NUMBER OF WORDS PER SENTENCE': avg_number_of_words_per_sentence,
        'COMPLEX WORD COUNT': complex_word_count,
        'WORD COUNT': word_count,
        'SYLLABLE PER WORD': syllable_per_word,
        'PERSONAL PRONOUNS': personal_pronouns,
        'AVG WORD LENGTH': avg_word_length
    }

# Iterate through each URL and save the article text
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    title, text = extract_article(url)
    if title and text:
        with open(f'/kaggle/working/articles/{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(title + '\n' + text)
    else:
        print(f"Failed to extract {url} after multiple attempts.")

output_data = []

for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    try:
        with open(f'/kaggle/working/articles/{url_id}.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            analysis = analyze_text(text)
            output_data.append({**row, **analysis})
    except Exception as e:
        print(f"Error processing {url_id}: {e}")

# Convert the results to a DataFrame
output_df = pd.DataFrame(output_data)

# Save the results to an Excel file
output_df.to_excel('/kaggle/working/Output_Data_Structure.xlsx', index=False)
