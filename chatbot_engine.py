# --- chatbot_engine.py ---
from sklearn.feature_extraction.text import TfidfVectorizer

def chunk_text(text, chunk_size=100):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def vectorize_chunks(chunks, query):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(chunks + [query])
    return vectors

def get_best_chunk(chunks, query):
    vectors = vectorize_chunks(chunks, query)
    similarity = (vectors[-1] * vectors.T).toarray()[0][:-1]
    best_index = similarity.argmax()
    return chunks[best_index]

def generate_response(query, context_chunk):
    if "school" in query.lower():
        return "I remember those fun school days! Weren’t morning assemblies the best?"
    elif "friends" in query.lower():
        return "Playing with childhood friends is something we never forget!"
    elif "cartoon" in query.lower():
        return "Cartoons like Tom and Jerry or Dragon Ball Z were legendary!"
    elif "birthday" in query.lower():
        return "Birthday parties with balloons and cake were magical moments!"
    else:
        return f"That's a wonderful memory! {context_chunk.strip()} made it even more special."
