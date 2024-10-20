import tkinter as tk
from tkinter import filedialog, scrolledtext
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def calculate_similarity(text1, text2):

    tokens1 = word_tokenize(text1)
    tokens2 = word_tokenize(text2)
    lemmatizer = WordNetLemmatizer()
    tokens1 = [lemmatizer.lemmatize(token) for token in tokens1]
    tokens2 = [lemmatizer.lemmatize(token) for token in tokens2]

    stop_words = set(stopwords.words('english'))
    tokens1 = [token for token in tokens1 if token.lower() not in stop_words]
    tokens2 = [token for token in tokens2 if token.lower() not in stop_words]

    vectorizer = TfidfVectorizer()
    vector1 = vectorizer.fit_transform([' '.join(tokens1)])
    vector2 = vectorizer.transform([' '.join(tokens2)])


    similarity = cosine_similarity(vector1, vector2)

    return similarity[0][0]

def select_file(text_area):
    file_path = filedialog.askopenfilename()
    if file_path:
        with open(file_path, 'r') as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

def compare_files():
    text1 = text_area1.get(1.0, tk.END).strip()
    text2 = text_area2.get(1.0, tk.END).strip()

    if text1 and text2:
        similarity = calculate_similarity(text1, text2)
        result_label.config(text=f"Similarity: {similarity:.2f}")
    else:
        result_label.config(text="Please select both files and ensure they contain text.")

def clear_text():
    text_area1.delete(1.0, tk.END)
    text_area2.delete(1.0, tk.END)
    result_label.config(text="")

root = tk.Tk()
root.title("Plagiarism Detection Tool")


frame1 = tk.Frame(root)
frame1.pack(pady=10)

select_button1 = tk.Button(frame1, text="Select Document 1", command=lambda: select_file(text_area1))
select_button1.pack(side=tk.LEFT)

text_area1 = scrolledtext.ScrolledText(frame1, width=50, height=10)
text_area1.pack(side=tk.LEFT, padx=5)

frame2 = tk.Frame(root)
frame2.pack(pady=10)

select_button2 = tk.Button(frame2, text="Select Document 2", command=lambda: select_file(text_area2))
select_button2.pack(side=tk.LEFT)

text_area2 = scrolledtext.ScrolledText(frame2, width=50, height=10)
text_area2.pack(side=tk.LEFT, padx=5)

frame3 = tk.Frame(root)
frame3.pack(pady=10)

compare_button = tk.Button(frame3, text="Compare Documents", command=compare_files)
compare_button.pack()

clear_button = tk.Button(frame3, text="Clear", command=clear_text)
clear_button.pack()

result_label = tk.Label(frame3, text="", font=("Helvetica", 14))
result_label.pack(pady=10)

root.mainloop()