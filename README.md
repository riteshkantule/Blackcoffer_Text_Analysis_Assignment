# README

## Project Title: Data Extraction and NLP

### Objective
The objective of this assignment is to extract textual data articles from given URLs and perform text analysis to compute various linguistic variables. The results are saved in a structured format in an Excel file.

### Approach

#### Data Extraction
1. **Reading Input Data:**
   - The input data is read from `Input.xlsx`, which contains URLs of articles to be extracted.
   
2. **Extracting Articles:**
   - Each URL is processed using the `requests` library to fetch the web page content.
   - The `BeautifulSoup` library is used to parse the HTML content and extract the article title and text. The text is assumed to be within `<h1>` tags for the title and `<p>` tags for the content.
   - Extracted articles are saved as text files in the `articles` directory, named using the `URL_ID`.

#### Data Analysis
1. **Loading Dictionaries:**
   - Positive and negative word lists are loaded from `positive-words.txt` and `negative-words.txt` respectively.
   - Stop words are loaded from multiple files in the `StopWords` directory.

2. **Text Analysis:**
   - The `TextBlob` library is used for basic NLP tasks like tokenization and sentence splitting.
   - Various linguistic metrics are computed for each article:
     - **Positive Score**: Count of positive words.
     - **Negative Score**: Count of negative words.
     - **Polarity Score**: `(Positive Score - Negative Score) / (Positive Score + Negative Score)`.
     - **Subjectivity Score**: `(Positive Score + Negative Score) / Total Words`.
     - **Average Sentence Length**: Total words / Total sentences.
     - **Percentage of Complex Words**: Complex words (words with 3+ syllables) / Total words * 100.
     - **FOG Index**: 0.4 * (Average Sentence Length + Percentage of Complex Words).
     - **Average Number of Words Per Sentence**: Total words / Total sentences.
     - **Word Count**: Total words.
     - **Syllables Per Word**: Total syllables / Total words.
     - **Personal Pronouns**: Count of personal pronouns.
     - **Average Word Length**: Total characters in words / Total words.

3. **Saving Results:**
   - The results are compiled into a DataFrame and saved as an Excel file `Output_Data_Structure.xlsx`.

### How to Run the Code

#### Prerequisites
Ensure you have the following libraries installed:
- `pandas`
- `requests`
- `beautifulsoup4`
- `nltk`
- `textblob`
- `openpyxl` (for Excel file operations)

You can install these dependencies using:
```sh
pip install pandas requests beautifulsoup4 nltk textblob openpyxl
```

#### Execution Steps
1. **Download NLTK Data:**
   The script includes commands to download necessary NLTK data files. Ensure an internet connection for the initial run:
   ```python
   nltk.download('stopwords')
   nltk.download('punkt')
   ```

2. **Run the Script:**
   Execute the script using Python:
   ```sh
   python script.py
   ```
   Ensure the input file `Input.xlsx` and dictionary files are placed in the correct directories as specified in the script. Adjust the paths in the script if necessary.

3. **Check the Output:**
   After execution, the output file `Output_Data_Structure.xlsx` will be generated in the working directory, containing the analyzed data for each article.

### File Structure
- **script.py**: The Python script containing the code.
- **Input.xlsx**: The input Excel file with URLs.
- **positive-words.txt**: List of positive words.
- **negative-words.txt**: List of negative words.
- **StopWords**: Directory containing stop word files.
- **Output_Data_Structure.xlsx**: The generated output Excel file.

### Note
Ensure all paths in the script are correctly set to the locations of your input files and directories.
