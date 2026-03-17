"""
I chose to use Alice's Adventures in Wonderland, by Lewis Carrol for my text.
I have no reason for choosing it besides it being the first book to catch my eye as I was scrolling through the Gutenberg website. I used the Project Gutenberg website to fetch the book.
The only modifications that were made to the code were to ensure that the only text referenced was Alice in Wonderland, and not Pride & Prejudice. I also needed to tweak it a little bit to only pull from the first 1500 words or so, instead of the entire book.
"""


"""
Text Processing and Word Frequency Analysiscear

We will fetch the first two chapters of Lewis Carroll's Alice in Wonderland from [Project Gutenberg](https://www.gutenberg.org/files/11/11-0.txt)
"""

import operator

# Function to fetch data
def fetch_text(raw_url):
  """
  Fetch and cache UTF-8 text from a URL.

  Downloads the text at the given URL with a 10-second timeout and caches it locally.
  If a cached file exists for the URL, its contents are returned without performing
  a network request. The cache directory is created automatically if it does not exist.

  Parameters:
      raw_url (str): The URL of the text resource to fetch.

  Returns:
      str: The UTF-8 text content from cache or freshly fetched from the URL.
      On error, prints an error message and returns an empty string.

  Notes:
      - Cache files are stored in `cs_110_content/text_cache/` directory.
      - Cache filenames use the first 12 hex characters of the SHA-1 hash of the URL.
      - Prints "✅ Text fetched." on success or "❌ Failed to fetch text." on failure.
      - HTTP errors and other exceptions are caught; the function does not raise them.
  """
  import requests
  from pathlib import Path
  import hashlib

  CACHE_DIR = Path("cs_110_content/text_cache")
  CACHE_DIR.mkdir(parents=True, exist_ok=True)

  def _url_to_filename(url):
    url_hash = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return CACHE_DIR / f"{url_hash}.txt"

  cache_path = _url_to_filename(raw_url)

  SUCCESS_MSG = "✅ Text fetched."
  FAILURE_MSG = "❌ Failed to fetch text."
  try:
    if not cache_path.exists():
      response = requests.get(raw_url, timeout=10)
      response.raise_for_status()
      text_data = response.text
      cache_path.write_text(text_data, encoding="utf-8")
    print(SUCCESS_MSG)
    return cache_path.read_text(encoding="utf-8")

  except Exception as e:
    print(FAILURE_MSG)
    print(f"Error: {e}")
    return ""

# Save the URL in a variable
ALICE_WONDERLAND_URL = "https://www.gutenberg.org/files/11/11-0.txt"

# Fetch the text
alice_wonderland_text = fetch_text(ALICE_WONDERLAND_URL)

# Instead of slicing by chapter headers
words = alice_wonderland_text.split()
alice_wonderland_text = " ".join(words[:1500])

# Statistics about the data
def print_text_stats(text):
  """
  Print statistics about the given text.

  Calculates and prints the total number of characters, lines, and words
  contained in the provided text string.

  Parameters:
      text (str): The text string to analyze.

  Returns:
      None. Prints statistics to stdout in the format:
      - Number of characters: <int>
      - Number of lines: <int>
      - Number of words: <int>
  """
  num_chars = len(text)

  lines = text.splitlines()
  num_lines = len(lines)

  num_words = 0
  for line in lines:
    words_in_line = line.split()
    num_words_in_line = len(words_in_line)
    num_words += num_words_in_line

  print(f"Number of characters: {num_chars}")
  print(f"Number of lines: {num_lines}")
  print(f"Number of words: {num_words}")

# Function to get word counts
def get_word_counts(text):
  """
  Count the frequency of each word in the given text.

  Splits the text into lines and words, converts each word to lowercase,
  and returns a dictionary mapping words to their frequency counts.

  Parameters:
      text (str): The text string to analyze for word frequencies.

  Returns:
      dict: A dictionary where keys are lowercase words (str) and values are
      the frequency counts (int) representing how many times each word appears.
  """
  word_counts = {}
  lines = text.splitlines()
  for line in lines:
    words = line.split()
    for word in words:
      word = word.lower()
      if word in word_counts:
        word_counts[word] += 1
      else:
        word_counts[word] = 1
  return word_counts

# the print_top_10_frequent_words will call the above get_word_counts() and print only the top 10 frequent words.
def print_top_10_frequent_words(text):
    """
    Print the top 10 most frequent words in the text.

    Counts word frequencies in the given text, sorts words by frequency in
    descending order, and prints the top 10 words along with their occurrence counts.

    Parameters:
        text (str): The text string to analyze.

    Returns:
        None. Prints the top 10 most frequent words and their counts to stdout,
        one per line in the format "word: count".
    """
    word_counts = get_word_counts(text)
    sorted_word_counts = dict(sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True))
    top_10_words = list(sorted_word_counts.items())[:10]  # Get the top 10 words and counts
    for word, count in top_10_words:
        print(f"{word}: {count}")


# this is a test print
print_text_stats(alice_wonderland_text)

# get the word counts
word_counts = get_word_counts(alice_wonderland_text)
print(word_counts)

# print the top 10 frequent words
print_top_10_frequent_words(alice_wonderland_text)

# Using spaCy for advanced text processing

import spacy

nlp = spacy.load('en_core_web_sm')

def word_tokenization_normalization(text):
    """
    Tokenize, normalize, and lemmatize text using spaCy.

    Converts text to lowercase, processes it with spaCy's language model,
    and filters to return only meaningful lemmatized words. Excludes stop words,
    punctuation, numbers, newlines, and words shorter than 3 characters after stripping.

    Parameters:
        text (str): The text string to tokenize and normalize.

    Returns:
        list: A list of lemmatized word strings (str), filtered and normalized.

    Notes:
        - Uses the global `nlp` spaCy model loaded with 'en_core_web_sm'.
        - Stop words and punctuation are excluded.
        - All words are lemmatized to their base form.
        - Only words with more than 2 characters (after stripping) are included.
    """

    text = text.lower() # lowercase
    doc = nlp(text)     # loading text into model

    words_normalized = []
    for word in doc:
        if word.text != '\n' \
        and not word.is_stop \
        and not word.is_punct \
        and not word.like_num \
        and len(word.text.strip()) > 2:
            word_lemmatized = str(word.lemma_)
            words_normalized.append(word_lemmatized)

    return words_normalized


def word_count(word_list):
    """
    Count the frequency of each word in a list of words.

    Takes a list of word strings, converts each to lowercase, and returns a dictionary
    mapping words to their frequency counts.

    Parameters:
        word_list (list): A list of word strings to count.

    Returns:
        dict: A dictionary where keys are lowercase words (str) and values are
        the frequency counts (int) representing how many times each word appears.
    """
    word_counts = {}
    for word in word_list:
      word = word.lower()
      if word in word_counts:
        word_counts[word] += 1
      else:
        word_counts[word] = 1
    return word_counts


def print_top_15_frequent_words(word_counts):
    """
    Print the top 15 most frequent words from a word count dictionary.

    Sorts the given word counts by frequency in descending order and prints
    the top 15 most frequent words along with their occurrence counts.

    Parameters:
        word_counts (dict): A dictionary with words (str) as keys and their
        frequency counts (int) as values.

    Returns:
        None. Prints the top 15 most frequent words and their counts to stdout,
        one per line in the format "word: count".
    """
    sorted_word_counts = dict(sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True))
    top_15_words = list(sorted_word_counts.items())[:15]  # Get the top 15 words and counts
    for word, count in top_15_words:
        print(f"{word}: {count}")

def get_top_verbs(text, top_n=15):
    doc = nlp(text.lower())
    verb_counts = {}

    for token in doc:
        if token.pos_ == "VERB" and not token.is_stop:
            verb = token.lemma_
            if verb in verb_counts:
                verb_counts[verb] += 1
            else:
                verb_counts[verb] = 1

    sorted_verbs = sorted(verb_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_verbs[:top_n]


def print_top_verbs(text, top_n=15):
    """
    Print the top N most frequent verbs in the text.

    Parameters:
        text (str): The text string to analyze.
        top_n (int): The number of top verbs to print. Default is 15.

    Returns:
        None. Prints the top verbs and their counts.
    """
    top_verbs = get_top_verbs(text, top_n)
    for verb, count in top_verbs:
        print(f"{verb}: {count}")


doc_tokenized = word_tokenization_normalization(alice_wonderland_text)

print(doc_tokenized)

new_counts = word_count(doc_tokenized)
print(new_counts)

print_top_15_frequent_words(new_counts)

print("\nTop 15 verbs:")
print_top_verbs(alice_wonderland_text)

"""
Top 15 Words in the first 2 chapters of Alice in Wonderland:
alice: 20
think: 16
chapter: 13
rabbit: 11
fall: 10
time: 8
little: 7
begin: 7
wonder: 7
go: 7
way: 6
look: 6
like: 6
come: 6
bat: 6

Yes, I do think that the top 15 words accuratly reflect the text's main themes and topics. It covers most of the main characters and events in vague detail. 
To me, among the most common words, chapter is the most suprising, but mainly because I expect it to only show up a few times as a lable for the actual chapters, and not as a topic within the content of the story.
While I do know what happens within the first two chapters, the top words point to a sptry that is very active with a lot of different characters and animals, that said, I don't think these words actually point to very much of the specific story and what is happening, and it would be difficult to guess the plot of the story just from these words.
All in all, the word frequency analysis does give us a little insight into the text's essence, but it is not enough to fully understand the story or plot.

Top 10 verbs:
think: 16
fall: 8
begin: 7
wonder: 7
go: 7
look: 6
come: 6
eat: 5
get: 4
see: 4

I chose to find out the top 10 verbs solely because I felt like verbs would provide. astronger insight into the story and its plot than adjectives. I actually ended up writing the code to extract the top 15 verbs, but upon rereading the instructions, I saw that it was 10, and that a lot of the last verbs were repeated the same number of times, and thought that it wouldn't hurt too bad to cut them out of the final product.
My findings show that within the first two chapters, Alice falls quite a lot, and judging by the use of "think" and "wonder," it leads to a surprising experience. Overall, the first two chapters do not have a lot of verbs used.

"""