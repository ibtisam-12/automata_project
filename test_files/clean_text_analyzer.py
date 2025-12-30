"""
Clean Text Analyzer
A safe text analysis utility.
This file contains no malware signatures.
"""

import re
from collections import Counter
from typing import Dict, List, Tuple


class TextAnalyzer:
    """Analyze text content safely."""
    
    def __init__(self, text: str = ""):
        self.text = text
        self.words = []
        self.sentences = []
        if text:
            self.process_text()
    
    def set_text(self, text: str):
        """Set new text to analyze."""
        self.text = text
        self.process_text()
    
    def process_text(self):
        """Process text into words and sentences."""
        # Split into sentences
        self.sentences = [s.strip() for s in re.split(r'[.!?]+', self.text) if s.strip()]
        
        # Split into words (alphanumeric only)
        self.words = re.findall(r'\b[a-zA-Z]+\b', self.text.lower())
    
    def word_count(self) -> int:
        """Count total words."""
        return len(self.words)
    
    def sentence_count(self) -> int:
        """Count total sentences."""
        return len(self.sentences)
    
    def character_count(self, include_spaces: bool = True) -> int:
        """Count total characters."""
        if include_spaces:
            return len(self.text)
        return len(self.text.replace(' ', ''))
    
    def average_word_length(self) -> float:
        """Calculate average word length."""
        if not self.words:
            return 0.0
        total_length = sum(len(word) for word in self.words)
        return total_length / len(self.words)
    
    def most_common_words(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get the n most common words."""
        word_counts = Counter(self.words)
        return word_counts.most_common(n)
    
    def unique_words(self) -> int:
        """Count unique words."""
        return len(set(self.words))
    
    def word_frequency(self, word: str) -> int:
        """Get frequency of a specific word."""
        return self.words.count(word.lower())
    
    def longest_words(self, n: int = 5) -> List[str]:
        """Get the n longest words."""
        unique_words = set(self.words)
        sorted_words = sorted(unique_words, key=len, reverse=True)
        return sorted_words[:n]
    
    def get_statistics(self) -> Dict[str, any]:
        """Get comprehensive text statistics."""
        return {
            'total_characters': self.character_count(True),
            'total_characters_no_spaces': self.character_count(False),
            'total_words': self.word_count(),
            'unique_words': self.unique_words(),
            'total_sentences': self.sentence_count(),
            'average_word_length': round(self.average_word_length(), 2),
            'average_sentence_length': round(self.word_count() / max(self.sentence_count(), 1), 2)
        }
    
    def display_analysis(self):
        """Display complete text analysis."""
        stats = self.get_statistics()
        
        print("Text Analysis Results")
        print("=" * 60)
        print(f"Total Characters: {stats['total_characters']}")
        print(f"Characters (no spaces): {stats['total_characters_no_spaces']}")
        print(f"Total Words: {stats['total_words']}")
        print(f"Unique Words: {stats['unique_words']}")
        print(f"Total Sentences: {stats['total_sentences']}")
        print(f"Average Word Length: {stats['average_word_length']} characters")
        print(f"Average Sentence Length: {stats['average_sentence_length']} words")
        
        print("\nMost Common Words:")
        for word, count in self.most_common_words(5):
            print(f"  {word}: {count}")
        
        print("\nLongest Words:")
        for word in self.longest_words(5):
            print(f"  {word} ({len(word)} characters)")


def demo():
    """Demonstrate text analyzer functionality."""
    sample_text = """
    The quick brown fox jumps over the lazy dog. This is a classic pangram 
    used to demonstrate all letters of the alphabet. Text analysis is an 
    important tool in natural language processing. It helps us understand 
    patterns and statistics in written content. The analyzer can count words, 
    sentences, and characters efficiently.
    """
    
    analyzer = TextAnalyzer(sample_text)
    analyzer.display_analysis()
    
    # Search for specific word
    print("\nWord Frequency Search:")
    search_words = ["the", "text", "analysis"]
    for word in search_words:
        freq = analyzer.word_frequency(word)
        print(f"  '{word}' appears {freq} time(s)")


if __name__ == "__main__":
    demo()
