from models import Book
import re
from functools import lru_cache

# Global cache for book tokens to avoid recomputation
_book_tokens_cache = None
_books_cache = None
_indices_cache = None

def tokenize(text):
    """
    Tokenize text into a set of lowercase words.
    Removes punctuation and common stop words.
    """
    if not text:
        return set()
    
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Common English stop words
    stop_words = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how', 'all',
        'each', 'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
        'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
        'just', 'as', 'if', 'then', 'because', 'while', 'about', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'between',
        'under', 'again', 'further', 'once', 'here', 'there', 'any', 'its'
    }
    
    # Tokenize and filter stop words
    tokens = set(word for word in text.split() if word not in stop_words and len(word) > 1)
    return tokens


def jaccard_similarity(set1, set2):
    """
    Compute Jaccard similarity between two sets.
    Jaccard = |A intersection B| / |A union B|
    Returns a value between 0 and 1.
    """
    if not set1 or not set2:
        return 0.0
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    if union == 0:
        return 0.0
    
    return intersection / union


def _get_cached_data():
    """
    Get or create cached book data for faster recommendations.
    Returns (books, indices, book_tokens)
    """
    global _books_cache, _indices_cache, _book_tokens_cache
    
    if _books_cache is None:
        _books_cache = Book.query.all()
        _indices_cache = {book.id: i for i, book in enumerate(_books_cache)}
        _book_tokens_cache = []
        for book in _books_cache:
            # Content-based filtering: combine title, author, genre, and description
            content = f"{book.title} {book.author} {book.genre} {book.description or ''}"
            _book_tokens_cache.append(tokenize(content))
    
    return _books_cache, _indices_cache, _book_tokens_cache


def clear_cache():
    """
    Clear the recommendation cache.
    Call this when books are added/updated/deleted.
    """
    global _books_cache, _indices_cache, _book_tokens_cache
    _books_cache = None
    _indices_cache = None
    _book_tokens_cache = None


def get_recommendations(book_id, num_recommendations=4):
    """
    Returns a list of Book objects similar to the given book_id.
    Uses Jaccard Similarity on Title + Author + Genre + Description (Content-Based Filtering).
    
    Optimized with caching for fast performance even with 10,000+ books.
    """
    books, indices, book_tokens = _get_cached_data()
    
    if not books:
        return []

    if book_id not in indices:
        return []

    # Get the target book's index and tokens
    idx = indices[book_id]
    target_tokens = book_tokens[idx]

    # Compute Jaccard similarity scores with all other books
    sim_scores = []
    for i, tokens in enumerate(book_tokens):
        if i != idx:  # Exclude the book itself
            similarity = jaccard_similarity(target_tokens, tokens)
            if similarity > 0:  # Only include books with some similarity
                sim_scores.append((i, similarity))

    # Sort by similarity score (descending)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get top N recommendations
    sim_scores = sim_scores[:num_recommendations]

    # Get Book Indices
    book_indices = [i[0] for i in sim_scores]

    # Return Book objects
    recommended_books = [books[i] for i in book_indices]
    
    return recommended_books
