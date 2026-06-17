from collections import Counter

def analyze_text(text):
    words = text.split()
    total_words = len(words)
    total_chars = len(text)
    total_no_spaces = len(text.replace(" ", ""))
    
    most_common_word = Counter(words).most_common(1)[0]
    
    print("\n📊 Text Analysis Results:")
    print(f"➡️ Total words: {total_words}")
    print(f"➡️ Total characters (with spaces): {total_chars}")
    print(f"➡️ Total characters (without spaces): {total_no_spaces}")
    print(f"➡️ Most used word: '{most_common_word[0]}' ({most_common_word[1]}x)")

def main():
    print("🧠 Text Analyzer — Python Project")
    text = input("Enter or paste the text you want to analyze:\n\n")
    analyze_text(text)

if __name__ == "__main__":
    main()