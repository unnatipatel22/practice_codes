"""
📁 FILE HANDLER PRO Advanced File Managemnt
"""
import os
import shutil
from datetime import datetime
import re

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    MAGENTA = '\033[35m'

class FileHandlerPro:
    def __init__(self):
        self.current_file = None
        self.file_content = ""
        self.backup_folder = "backups"
        self.operation_history = []
        
        
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)
    
    def clear_screen(self):
       
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        
        banner = f"""
{Colors.BOLD}{Colors.CYAN}╔════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║                  📁  FILE HANDLER PRO  📁                             ║
║                                                                        ║
║            Advanced File Management & Text Processing                  ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(banner)
    
    def print_status(self):
        
        if self.current_file:
            file_size = len(self.file_content)
            word_count = len(self.file_content.split())
            line_count = len(self.file_content.splitlines())
            
            print(f"\n{Colors.BOLD}{Colors.GREEN}📊 CURRENT FILE STATUS:{Colors.ENDC}")
            print(f"{Colors.CYAN}┌{'─'*70}┐")
            print(f"│ 📄 File: {Colors.YELLOW}{self.current_file:<58}{Colors.CYAN}│")
            print(f"│ 📏 Size: {file_size} characters | 📝 Words: {word_count} | 📃 Lines: {line_count}{' '*(18-len(str(file_size))-len(str(word_count))-len(str(line_count)))}│")
            print(f"│ ⏱️  Operations: {len(self.operation_history)}{' '*(55-len(str(len(self.operation_history))))}│")
            print(f"└{'─'*70}┘{Colors.ENDC}\n")
        else:
            print(f"\n{Colors.YELLOW}ℹ️  No file loaded. Please create or open a file first.{Colors.ENDC}\n")
    
    def create_file(self):
       
        print(f"\n{Colors.BOLD}{Colors.GREEN}📝 CREATE NEW FILE{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        filename = input(f"{Colors.CYAN}Enter filename (with .txt extension): {Colors.ENDC}").strip()
        
        if not filename:
            print(f"{Colors.RED}✗ Filename cannot be empty!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
       
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        


        if os.path.exists(filename):
            overwrite = input(f"{Colors.YELLOW}⚠️  File already exists! Overwrite? (yes/no): {Colors.ENDC}").lower()
            if overwrite not in ['yes', 'y']:
                print(f"{Colors.YELLOW}Operation cancelled.{Colors.ENDC}")
                input("\nPress Enter to continue...")
                return
        
        try:
            print(f"\n{Colors.CYAN}Enter your content (Type 'END' on a new line to finish):{Colors.ENDC}\n")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            
            content = '\n'.join(lines)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.current_file = filename
            self.file_content = content
            self.operation_history.append(f"Created file: {filename}")
            
            print(f"\n{Colors.GREEN}✓ File '{filename}' created successfully!{Colors.ENDC}")
            print(f"{Colors.CYAN}Written {len(content)} characters, {len(content.split())} words.{Colors.ENDC}")
            
        except Exception as e:
            print(f"{Colors.RED}✗ Error creating file: {str(e)}{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def open_file(self):
        

        print(f"\n{Colors.BOLD}{Colors.GREEN}📂 OPEN FILE{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
        
        if txt_files:
            print(f"{Colors.BOLD}Available text files:{Colors.ENDC}")
            for idx, file in enumerate(txt_files, 1):
                size = os.path.getsize(file)
                print(f"  [{idx}] {Colors.CYAN}{file}{Colors.ENDC} ({size} bytes)")
            print()
        
        filename = input(f"{Colors.CYAN}Enter filename to open: {Colors.ENDC}").strip()
        
        if not filename:
            print(f"{Colors.RED}✗ Filename cannot be empty!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.current_file = filename
            self.file_content = content
            self.operation_history.append(f"Opened file: {filename}")
            
            print(f"\n{Colors.GREEN}✓ File '{filename}' opened successfully!{Colors.ENDC}")
            print(f"{Colors.CYAN}Loaded {len(content)} characters, {len(content.split())} words.{Colors.ENDC}")
            
        except FileNotFoundError:
            print(f"{Colors.RED}✗ Error: File '{filename}' not found!{Colors.ENDC}")
        except PermissionError:
            print(f"{Colors.RED}✗ Error: Permission denied to read '{filename}'!{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}✗ Error opening file: {str(e)}{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def view_content(self):
        

        if not self.current_file:
            print(f"\n{Colors.YELLOW}⚠️  No file loaded!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}📄 FILE CONTENT{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        print(f"{Colors.BOLD}File: {Colors.YELLOW}{self.current_file}{Colors.ENDC}\n")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}")
        
        if self.file_content:
        
            lines = self.file_content.splitlines()
            for idx, line in enumerate(lines, 1):
                print(f"{Colors.YELLOW}{idx:3d}{Colors.ENDC} | {line}")
        else:
            print(f"{Colors.YELLOW}(Empty file){Colors.ENDC}")
        
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}")
        input("\n\nPress Enter to continue...")
    
    def find_and_replace(self):
       
        if not self.current_file:
            print(f"\n{Colors.YELLOW}⚠️  No file loaded!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🔍 FIND & REPLACE{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        find_text = input(f"{Colors.CYAN}Enter text to find: {Colors.ENDC}")
        
        if not find_text:
            print(f"{Colors.RED}✗ Search text cannot be empty!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        
        count = self.file_content.count(find_text)
        
        if count == 0:
            print(f"\n{Colors.YELLOW}ℹ️  Text '{find_text}' not found in file.{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.GREEN}✓ Found {count} occurrence(s) of '{find_text}'.{Colors.ENDC}")
        
        
        print(f"\n{Colors.BOLD}Preview of occurrences:{Colors.ENDC}")
        lines = self.file_content.splitlines()
        preview_count = 0
        for idx, line in enumerate(lines, 1):
            if find_text in line:
                highlighted = line.replace(find_text, f"{Colors.YELLOW}{Colors.BOLD}{find_text}{Colors.ENDC}")
                print(f"  Line {idx}: {highlighted}")
                preview_count += 1
                if preview_count >= 5:
                    print(f"  {Colors.CYAN}(Showing first 5 matches...){Colors.ENDC}")
                    break
        
        replace_text = input(f"\n{Colors.CYAN}Enter replacement text: {Colors.ENDC}")
        
        confirm = input(f"\n{Colors.YELLOW}Replace all {count} occurrence(s)? (yes/no): {Colors.ENDC}").lower()
        
        if confirm in ['yes', 'y']:
            

            self.create_backup()
            
            self.file_content = self.file_content.replace(find_text, replace_text)
            
            try:
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.file_content)
                
                self.operation_history.append(f"Replaced '{find_text}' with '{replace_text}' ({count} times)")
                
                print(f"\n{Colors.GREEN}✓ Successfully replaced {count} occurrence(s)!{Colors.ENDC}")
                print(f"{Colors.CYAN}ℹ️  Backup created in '{self.backup_folder}' folder.{Colors.ENDC}")
                
            except Exception as e:
                print(f"{Colors.RED}✗ Error saving file: {str(e)}{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}Operation cancelled.{Colors.ENDC}")
        

        input("\nPress Enter to continue...")
    
    def find_text(self):
        
        if not self.current_file:
            print(f"\n{Colors.YELLOW}⚠️  No file loaded!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🔎 SEARCH TEXT{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        search_text = input(f"{Colors.CYAN}Enter text to search: {Colors.ENDC}")
        
        if not search_text:
            print(f"{Colors.RED}✗ Search text cannot be empty!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        
        case_sensitive = input(f"{Colors.CYAN}Case-sensitive search? (yes/no) [no]: {Colors.ENDC}").lower()
        
        lines = self.file_content.splitlines()
        matches = []
        
        for idx, line in enumerate(lines, 1):
            if case_sensitive in ['yes', 'y']:
                if search_text in line:
                    matches.append((idx, line))
            else:
                if search_text.lower() in line.lower():
                    matches.append((idx, line))
        
        print(f"\n{Colors.CYAN}{'─'*72}{Colors.ENDC}")
        
        if matches:
            print(f"\n{Colors.GREEN}✓ Found {len(matches)} match(es):{Colors.ENDC}\n")
            
            for line_num, line in matches:
                
                if case_sensitive in ['yes', 'y']:
                    highlighted = line.replace(search_text, f"{Colors.YELLOW}{Colors.BOLD}{search_text}{Colors.ENDC}")
                else:
                   
                    pattern = re.compile(re.escape(search_text), re.IGNORECASE)
                    highlighted = pattern.sub(lambda m: f"{Colors.YELLOW}{Colors.BOLD}{m.group()}{Colors.ENDC}", line)
                
                print(f"  {Colors.CYAN}Line {line_num}:{Colors.ENDC} {highlighted}")
        else:
            print(f"\n{Colors.YELLOW}ℹ️  No matches found for '{search_text}'.{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}{'─'*72}{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def word_statistics(self):
        
        if not self.current_file:
            print(f"\n{Colors.YELLOW}⚠️  No file loaded!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}📊 WORD STATISTICS{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        


        char_count = len(self.file_content)
        char_no_spaces = len(self.file_content.replace(' ', '').replace('\n', ''))
        words = self.file_content.split()
        word_count = len(words)
        line_count = len(self.file_content.splitlines())
        
        print(f"{Colors.CYAN}┌{'─'*70}┐")
        print(f"│ {Colors.BOLD}Total Characters:{Colors.ENDC} {char_count:<52} │")
        print(f"│ {Colors.BOLD}Characters (no spaces):{Colors.ENDC} {char_no_spaces:<43} │")
        print(f"│ {Colors.BOLD}Total Words:{Colors.ENDC} {word_count:<55} │")
        print(f"│ {Colors.BOLD}Total Lines:{Colors.ENDC} {line_count:<55} │")
        print(f"│ {Colors.BOLD}Average Word Length:{Colors.ENDC} {(char_no_spaces/word_count if word_count > 0 else 0):.2f} characters{' '*35} │")
        print(f"└{'─'*70}┘{Colors.ENDC}\n")
        
        
        if word_count > 0:
            word_freq = {}
            for word in words:
                clean_word = word.lower().strip('.,!?;:"\'')
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
            
            # Top 10 most comon words
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            print(f"{Colors.BOLD}🔥 Top 10 Most Common Words:{Colors.ENDC}\n")
            for idx, (word, count) in enumerate(sorted_words, 1):
                bar = '█' * min(count, 30)
                print(f"  {idx:2d}. {Colors.YELLOW}{word:<15}{Colors.ENDC} {Colors.GREEN}{bar}{Colors.ENDC} {count}")
        
        input("\n\nPress Enter to continue...")
    
    def append_text(self):
        
        if not self.current_file:
            print(f"\n{Colors.YELLOW}⚠️  No file loaded!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}➕ APPEND TEXT{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        print(f"{Colors.CYAN}Enter text to append (Type 'END' on a new line to finish):{Colors.ENDC}\n")
        
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        
        new_content = '\n'.join(lines)
        
        if not new_content.strip():
            print(f"{Colors.YELLOW}No content entered. Operation cancelled.{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        try:
           
            self.create_backup()
            
            
            with open(self.current_file, 'a', encoding='utf-8') as f:
                f.write('\n' + new_content)
            
            
            self.file_content += '\n' + new_content
            self.operation_history.append(f"Appended text to file")
            
            print(f"\n{Colors.GREEN}✓ Text appended successfully!{Colors.ENDC}")
            print(f"{Colors.CYAN}Added {len(new_content)} characters.{Colors.ENDC}")
            
        except Exception as e:
            print(f"{Colors.RED}✗ Error appending to file: {str(e)}{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def delete_lines(self):
        
        if not self.current_file:
            print(f"\n{Colors.YELLOW}⚠️  No file loaded!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🗑️  DELETE LINES{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        lines = self.file_content.splitlines()
        total_lines = len(lines)
        
        print(f"{Colors.CYAN}Total lines in file: {total_lines}{Colors.ENDC}\n")
        
        delete_input = input(f"{Colors.CYAN}Enter line numbers to delete (e.g., 1,3,5-7): {Colors.ENDC}").strip()
        
        if not delete_input:
            print(f"{Colors.YELLOW}Operation cancelled.{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        try:
            
            lines_to_delete = set()
            for part in delete_input.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    lines_to_delete.update(range(start, end + 1))
                else:
                    lines_to_delete.add(int(part))
            
    

            invalid = [l for l in lines_to_delete if l < 1 or l > total_lines]
            if invalid:
                print(f"{Colors.RED}✗ Invalid line numbers: {invalid}{Colors.ENDC}")
                input("\nPress Enter to continue...")
                return
            
            print(f"\n{Colors.YELLOW}Lines to be deleted: {sorted(lines_to_delete)}{Colors.ENDC}")
            confirm = input(f"{Colors.YELLOW}Confirm deletion? (yes/no): {Colors.ENDC}").lower()
            
            if confirm in ['yes', 'y']:
                
                self.create_backup()
                
                new_lines = [line for idx, line in enumerate(lines, 1) if idx not in lines_to_delete]
                self.file_content = '\n'.join(new_lines)
                
                
                with open(self.current_file, 'w', encoding='utf-8') as f:
                    f.write(self.file_content)
                
                self.operation_history.append(f"Deleted {len(lines_to_delete)} line(s)")
                
                print(f"\n{Colors.GREEN}✓ Successfully deleted {len(lines_to_delete)} line(s)!{Colors.ENDC}")
            else:
                print(f"{Colors.YELLOW}Operation cancelled.{Colors.ENDC}")
        
        except ValueError:
            print(f"{Colors.RED}✗ Invalid input format!{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}✗ Error: {str(e)}{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def create_backup(self):
        if self.current_file and os.path.exists(self.current_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{self.backup_folder}/{os.path.splitext(self.current_file)[0]}_{timestamp}.txt"
            
            try:
                shutil.copy2(self.current_file, backup_name)
            except Exception as e:
                print(f"{Colors.RED}Warning: Could not create backup: {str(e)}{Colors.ENDC}")
    
    def view_history(self):
        


        print(f"\n{Colors.BOLD}{Colors.GREEN}📜 OPERATION HISTORY{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
        
        if not self.operation_history:
            print(f"{Colors.YELLOW}No operations performed yet.{Colors.ENDC}")
        else:
            for idx, operation in enumerate(self.operation_history, 1):
                print(f"  {Colors.CYAN}{idx:2d}.{Colors.ENDC} {operation}")
        
        print(f"\n{Colors.CYAN}{'─'*72}{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_status()
            
            print(f"{Colors.BOLD}{Colors.CYAN}📋 MAIN MENU{Colors.ENDC}")
            print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}")
            print(f"  {Colors.GREEN}[1]{Colors.ENDC}  📝 Create New File")
            print(f"  {Colors.GREEN}[2]{Colors.ENDC}  📂 Open Existing File")
            print(f"  {Colors.GREEN}[3]{Colors.ENDC}  📄 View File Content")
            print(f"  {Colors.GREEN}[4]{Colors.ENDC}  🔍 Find & Replace")
            print(f"  {Colors.GREEN}[5]{Colors.ENDC}  🔎 Search Text")
            print(f"  {Colors.GREEN}[6]{Colors.ENDC}  ➕ Append Text")
            print(f"  {Colors.GREEN}[7]{Colors.ENDC}  🗑️  Delete Lines")
            print(f"  {Colors.GREEN}[8]{Colors.ENDC}  📊 Word Statistics")
            print(f"  {Colors.GREEN}[9]{Colors.ENDC}  📜 View History")
            print(f"  {Colors.RED}[0]{Colors.ENDC}  🚪 Exit")
            print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}")
            
            choice = input(f"\n{Colors.BOLD}{Colors.MAGENTA}Enter your choice (0-9): {Colors.ENDC}").strip()
            
            if choice == '1':
                self.create_file()
            elif choice == '2':
                self.open_file()
            elif choice == '3':
                self.view_content()
            elif choice == '4':
                self.find_and_replace()
            elif choice == '5':
                self.find_text()
            elif choice == '6':
                self.append_text()
            elif choice == '7':
                self.delete_lines()
            elif choice == '8':
                self.word_statistics()
            elif choice == '9':
                self.view_history()
            elif choice == '0':
                self.clear_screen()
                print(f"\n{Colors.CYAN}{'─'*72}")
                print(f"{Colors.BOLD}{Colors.GREEN}Thanks for using File Handler Pro! 👋{Colors.ENDC}")
                print(f"{Colors.CYAN}All your files are safe and sound! 📁{Colors.ENDC}")
                print(f"{Colors.CYAN}{'─'*72}{Colors.ENDC}\n")
                break
            else:
                print(f"\n{Colors.RED}✗ Invalid choice! Please select 0-9.{Colors.ENDC}")
                input("\nPress Enter to continue...")

def main():
    
    
    app = FileHandlerPro()
    app.main_menu()

if __name__ == "__main__":
    main()