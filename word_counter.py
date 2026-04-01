"""
📊 WORD Count app """

import os
import string
from collections import Counter
from datetime import datetime
import json

# Enhanced Color Codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[35m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    END = '\033[0m'

def print_banner():
    
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════════╗
║  {Colors.BOLD}{Colors.YELLOW}📊 WORD COUNT PRO - Advanced Text Analysis Tool 📊{Colors.END}{Colors.CYAN}          ║
║  {Colors.WHITE}Analyze • Count • Discover • Visualize{Colors.END}{Colors.CYAN}                         ║
╚═══════════════════════════════════════════════════════════════════╝{Colors.END}
    """
    print(banner)

def create_sample_file():
    """Created a sample text file for demo"""
    sample_text = """Python is a high-level programming language. Python is widely used for web development, 
data analysis, artificial intelligence, and scientific computing. Python's syntax is clean and readable.
Many developers love Python because of its simplicity and versatility. Python has a vast ecosystem 
of libraries and frameworks. Machine learning with Python is very popular. Python is beginner-friendly.
The Python community is large and supportive. Python continues to grow in popularity every year.
Data science and Python go hand in hand. Python is the future of programming."""
    
    filename = "sample_text.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(sample_text)
    return filename

def get_file_input():
    
    print(f"\n{Colors.YELLOW}📁 File Selection Options:{Colors.END}")
    print(f"{Colors.CYAN}   1. Use sample file (auto-generated)")
    print(f"   2. Enter your own file path")
    print(f"   3. Type/paste text directly{Colors.END}\n")
    
    choice = input(f"{Colors.GREEN}➜ Choose option (1/2/3): {Colors.END}").strip()
    
    if choice == '1':
        filename = create_sample_file()
        print(f"{Colors.GREEN}✅ Sample file created: {filename}{Colors.END}")
        return filename, 'file'
    elif choice == '2':
        while True:
            filepath = input(f"\n{Colors.GREEN}➜ Enter file path: {Colors.END}").strip().strip('"')
            if os.path.exists(filepath):
                return filepath, 'file'
            else:
                print(f"{Colors.RED}❌ File not found! Try again.{Colors.END}")
    elif choice == '3':
        print(f"\n{Colors.YELLOW}📝 Enter your text (type 'END' on a new line to finish):{Colors.END}")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        text = '\n'.join(lines)
        
        temp_file = "temp_input.txt"
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(text)
        return temp_file, 'text'
    else:
        print(f"{Colors.RED}❌ Invalid choice! Using sample file.{Colors.END}")
        return create_sample_file(), 'file'

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"{Colors.RED}❌ Error reading file: {str(e)}{Colors.END}")
        return None

def analyze_text(content):
    

    lines = content.split('\n')
    total_lines = len(lines)
    non_empty_lines = len([line for line in lines if line.strip()])
    
    total_chars = len(content)
    chars_no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
   
    words = content.lower().split()
    words_cleaned = []
    
    for word in words:
        
        cleaned = word.strip(string.punctuation)
        if cleaned:
            words_cleaned.append(cleaned)
    
    total_words = len(words_cleaned)
    unique_words = len(set(words_cleaned))
   
    word_freq = Counter(words_cleaned)
    
    sentence_terminators = ['.', '!', '?']
    sentences = sum(content.count(term) for term in sentence_terminators)
    
    avg_word_length = sum(len(word) for word in words_cleaned) / total_words if total_words > 0 else 0
    avg_words_per_line = total_words / non_empty_lines if non_empty_lines > 0 else 0
    
    longest_word = max(words_cleaned, key=len) if words_cleaned else ""
    shortest_word = min(words_cleaned, key=len) if words_cleaned else ""
    
    return {
        'total_lines': total_lines,
        'non_empty_lines': non_empty_lines,
        'total_chars': total_chars,
        'chars_no_spaces': chars_no_spaces,
        'total_words': total_words,
        'unique_words': unique_words,
        'word_freq': word_freq,
        'sentences': sentences,
        'avg_word_length': avg_word_length,
        'avg_words_per_line': avg_words_per_line,
        'longest_word': longest_word,
        'shortest_word': shortest_word
    }

def create_bar_chart(value, max_value, width=30):
   
   
    filled = int((value / max_value) * width) if max_value > 0 else 0
    bar = '█' * filled + '░' * (width - filled)
    return bar

def display_results(analysis, content):
    print(f"\n{Colors.CYAN}{'═' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.HEADER}📊 TEXT ANALYSIS RESULTS{Colors.END}")
    print(f"{Colors.CYAN}{'═' * 70}{Colors.END}\n")
    
    
    print(f"{Colors.BOLD}{Colors.BLUE}📈 BASIC STATISTICS{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 70}{Colors.END}")
    
    stats = [
        ("Total Lines", analysis['total_lines'], Colors.YELLOW),
        ("Non-Empty Lines", analysis['non_empty_lines'], Colors.GREEN),
        ("Total Characters", analysis['total_chars'], Colors.CYAN),
        ("Characters (no spaces)", analysis['chars_no_spaces'], Colors.MAGENTA),
        ("Total Words", analysis['total_words'], Colors.YELLOW),
        ("Unique Words", analysis['unique_words'], Colors.GREEN),
        ("Sentences (approx)", analysis['sentences'], Colors.CYAN),
    ]
    
    for label, value, color in stats:
        print(f"  {color}▪{Colors.END} {label:<25} {Colors.BOLD}{color}{value:>10}{Colors.END}")
    
   
    print(f"\n{Colors.BOLD}{Colors.BLUE}🎯 ADVANCED METRICS{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 70}{Colors.END}")
    
    print(f"  {Colors.YELLOW}▪{Colors.END} Average Word Length        {Colors.BOLD}{Colors.YELLOW}{analysis['avg_word_length']:.2f} characters{Colors.END}")
    print(f"  {Colors.GREEN}▪{Colors.END} Average Words per Line     {Colors.BOLD}{Colors.GREEN}{analysis['avg_words_per_line']:.2f} words{Colors.END}")
    print(f"  {Colors.CYAN}▪{Colors.END} Longest Word               {Colors.BOLD}{Colors.CYAN}{analysis['longest_word']} ({len(analysis['longest_word'])} chars){Colors.END}")
    print(f"  {Colors.MAGENTA}▪{Colors.END} Shortest Word              {Colors.BOLD}{Colors.MAGENTA}{analysis['shortest_word']} ({len(analysis['shortest_word'])} chars){Colors.END}")
    print(f"  {Colors.YELLOW}▪{Colors.END} Vocabulary Richness        {Colors.BOLD}{Colors.YELLOW}{(analysis['unique_words']/analysis['total_words']*100):.1f}%{Colors.END}")
   
    print(f"\n{Colors.BOLD}{Colors.BLUE}🏆 TOP 15 MOST FREQUENT WORDS{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 70}{Colors.END}\n")
    
    top_words = analysis['word_freq'].most_common(15)
    max_count = top_words[0][1] if top_words else 1
    
    for rank, (word, count) in enumerate(top_words, 1):
        bar = create_bar_chart(count, max_count, 30)
        percentage = (count / analysis['total_words']) * 100
        
       

        if rank <= 3:
            rank_color = Colors.YELLOW
            emoji = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
        elif rank <= 5:
            rank_color = Colors.GREEN
            emoji = "⭐"
        else:
            rank_color = Colors.CYAN
            emoji = "▪"
        
        print(f"  {emoji} {rank_color}{rank:2d}.{Colors.END} {Colors.BOLD}{word:<15}{Colors.END} "
              f"{Colors.GREEN}{bar}{Colors.END} "
              f"{Colors.YELLOW}{count:>3}{Colors.END} "
              f"{Colors.CYAN}({percentage:.1f}%){Colors.END}")
    
   
    print(f"\n{Colors.BOLD}{Colors.BLUE}📏 WORD LENGTH DISTRIBUTION{Colors.END}")
    print(f"{Colors.CYAN}{'─' * 70}{Colors.END}\n")
    
    word_lengths = {}
    for word in content.lower().split():
        cleaned = word.strip(string.punctuation)
        if cleaned:
            length = len(cleaned)
            word_lengths[length] = word_lengths.get(length, 0) + 1
    
    max_length_count = max(word_lengths.values()) if word_lengths else 1
    
    for length in sorted(word_lengths.keys())[:10]:  # Show first 10
        count = word_lengths[length]
        bar = create_bar_chart(count, max_length_count, 25)
        percentage = (count / analysis['total_words']) * 100
        
        print(f"  {Colors.YELLOW}{length:2d} chars:{Colors.END} "
              f"{Colors.CYAN}{bar}{Colors.END} "
              f"{Colors.GREEN}{count:>4} words{Colors.END} "
              f"{Colors.MAGENTA}({percentage:.1f}%){Colors.END}")
    
    print(f"\n{Colors.CYAN}{'═' * 70}{Colors.END}")

def save_report(analysis, content, filename):
   

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"analysis_report_{timestamp}.json"
    
    report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'source_file': filename,
        'statistics': {
            'total_lines': analysis['total_lines'],
            'non_empty_lines': analysis['non_empty_lines'],
            'total_characters': analysis['total_chars'],
            'characters_no_spaces': analysis['chars_no_spaces'],
            'total_words': analysis['total_words'],
            'unique_words': analysis['unique_words'],
            'sentences': analysis['sentences'],
            'avg_word_length': round(analysis['avg_word_length'], 2),
            'avg_words_per_line': round(analysis['avg_words_per_line'], 2),
            'longest_word': analysis['longest_word'],
            'shortest_word': analysis['shortest_word']
        },
        'top_20_words': dict(analysis['word_freq'].most_common(20)),
        'text_preview': content[:200] + '...' if len(content) > 200 else content
    }
    
    try:
        with open(report_filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n{Colors.GREEN}✅ Detailed report saved: {report_filename}{Colors.END}")
        return True
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error saving report: {str(e)}{Colors.END}")
        return False

def main():
    print_banner()
    
   
    filepath, input_type = get_file_input()
    
    print(f"\n{Colors.BLUE}🔄 Reading file...{Colors.END}")
    content = read_file(filepath)
    
    if not content:
        print(f"{Colors.RED}❌ Failed to read file!{Colors.END}")
        return
    
    print(f"{Colors.GREEN}✅ File loaded successfully!{Colors.END}")
    print(f"{Colors.CYAN}📄 File size: {len(content)} bytes{Colors.END}")
    
    print(f"{Colors.BLUE}🔍 Analyzing text...{Colors.END}")
    analysis = analyze_text(content)
    print(f"{Colors.GREEN}✅ Analysis complete!{Colors.END}")
    display_results(analysis, content)
    

    save_choice = input(f"\n{Colors.YELLOW}💾 Save detailed JSON report? (y/n): {Colors.END}").lower()
    if save_choice == 'y':
        save_report(analysis, content, filepath)
    
    print(f"\n{Colors.CYAN}{'═' * 70}{Colors.END}")
    another = input(f"\n{Colors.YELLOW}🔄 Analyze another file? (y/n): {Colors.END}").lower()
    if another == 'y':
        print("\n" * 2)
        main()
    else:
        print(f"\n{Colors.GREEN}{'═' * 70}")
        print(f"{Colors.BOLD}{Colors.YELLOW}   🎉 Thank you for using Word Count Pro! 🎉{Colors.END}")
        print(f"{Colors.GREEN}{'═' * 70}{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Program interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ An error occurred: {str(e)}{Colors.END}\n")