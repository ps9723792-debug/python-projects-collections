import re

def count_words(text):
    # Remove extra spaces and split words
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def count_characters(text):
    return len(text)

def count_sentences(text):
    sentences = re.split(r'[.!?]+', text)
    # Remove empty strings
    sentences = [s for s in sentences if s.strip()]
    return len(sentences)

def main():
    print("📝 Word Counter Tool")
    
    while True:
        text = input("\nEnter your text:\n")
        
        word_count = count_words(text)
        char_count = count_characters(text)
        sentence_count = count_sentences(text)
        
        print("\n📊 Analysis Results:")
        print(f"Words: {word_count}")
        print(f"Characters: {char_count}")
        print(f"Sentences: {sentence_count}")
        
        again = input("\nAnalyze another text? (y/n): ").lower()
        if again != 'y':
            print("Goodbye! 👋")
            break

if __name__ == "__main__":
    main()
