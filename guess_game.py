import random
import os
import time
from datetime import datetime
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

class NumberGuessingGame:
    def __init__(self):
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.difficulty = ""
        self.min_range = 0
        self.max_range = 0
        self.game_history = []
        self.best_score = float('inf')
        self.total_games = 0
        self.total_wins = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = f"""
{Colors.BOLD}{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║          🎮  GUESS THE NUMBER GAME  🎮                              ║
║                                                                      ║
║              Test Your Luck & Logic Skills!                          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        print(banner)
    
    def print_stats(self):
        
        if self.total_games > 0:
            win_rate = (self.total_wins / self.total_games) * 100
            print(f"\n{Colors.BOLD}{Colors.YELLOW}📊 YOUR STATS:{Colors.ENDC}")
            print(f"{Colors.CYAN}┌{'─'*68}┐")
            print(f"│ Games Played: {self.total_games:<10} │ Wins: {self.total_wins:<10} │ Win Rate: {win_rate:.1f}%{' '*(10-len(f'{win_rate:.1f}'))} │")
            if self.best_score != float('inf'):
                print(f"│ Best Score: {self.best_score} attempts{' '*(46-len(str(self.best_score)))} │")
            print(f"└{'─'*68}┘{Colors.ENDC}\n")
    
    def select_difficulty(self):
       
        self.clear_screen()
        self.print_banner()
        
        print(f"{Colors.BOLD}{Colors.GREEN}🎯 SELECT DIFFICULTY LEVEL{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}\n")
        
        difficulties = {
            '1': {
                'name': 'Easy',
                'range': (1, 50),
                'attempts': 10,
                'emoji': '😊',
                'color': Colors.GREEN,
                'desc': 'Perfect for beginners! Range: 1-50'
            },
            '2': {
                'name': 'Medium',
                'range': (1, 100),
                'attempts': 7,
                'emoji': '😐',
                'color': Colors.YELLOW,
                'desc': 'Moderate challenge! Range: 1-100'
            },
            '3': {
                'name': 'Hard',
                'range': (1, 200),
                'attempts': 8,
                'emoji': '😰',
                'color': Colors.RED,
                'desc': 'For experts only! Range: 1-200'
            },
            '4': {
                'name': 'Extreme',
                'range': (1, 500),
                'attempts': 10,
                'emoji': '💀',
                'color': Colors.MAGENTA,
                'desc': 'Insane difficulty! Range: 1-500'
            }
        }
        
        for key, diff in difficulties.items():
            print(f"  {diff['color']}[{key}] {diff['emoji']} {diff['name']:<10}{Colors.ENDC} - {diff['desc']}")
            print(f"      {Colors.CYAN}Max Attempts: {diff['attempts']}{Colors.ENDC}\n")
        
        while True:
            choice = input(f"{Colors.BOLD}Choose difficulty (1-4): {Colors.ENDC}").strip()
            
            if choice in difficulties:
                selected = difficulties[choice]
                self.difficulty = selected['name']
                self.min_range, self.max_range = selected['range']
                self.max_attempts = selected['attempts']
                
                print(f"\n{Colors.GREEN}✓ {selected['emoji']} {selected['name']} mode selected!{Colors.ENDC}")
                time.sleep(1)
                return
            else:
                print(f"{Colors.RED}✗ Invalid choice! Please select 1-4.{Colors.ENDC}")
    
    def generate_number(self):
        
        self.secret_number = random.randint(self.min_range, self.max_range)
        self.attempts = 0
        self.game_history = []
    
    def get_hint(self, guess):
       
        difference = abs(guess - self.secret_number)
        
        if difference == 0:
            return f"{Colors.GREEN}🎉 PERFECT! You got it!{Colors.ENDC}"
        elif difference <= 5:
            return f"{Colors.RED}🔥 ON FIRE! Super close!{Colors.ENDC}"
        elif difference <= 10:
            return f"{Colors.YELLOW}🌡️  Getting HOT!{Colors.ENDC}"
        elif difference <= 20:
            return f"{Colors.CYAN}❄️  Getting warm...{Colors.ENDC}"
        elif difference <= 50:
            return f"{Colors.BLUE}🧊 Still cold!{Colors.ENDC}"
        else:
            return f"{Colors.MAGENTA}🥶 Freezing cold!{Colors.ENDC}"
    
    def display_progress_bar(self):
       
        remaining = self.max_attempts - self.attempts
        filled = int((self.attempts / self.max_attempts) * 20)
        bar = '█' * filled + '░' * (20 - filled)
        
        if remaining <= 2:
            color = Colors.RED
        elif remaining <= 4:
            color = Colors.YELLOW
        else:
            color = Colors.GREEN
        
        print(f"\n{Colors.BOLD}Attempts Used: {color}{self.attempts}/{self.max_attempts}{Colors.ENDC}")
        print(f"{Colors.CYAN}[{bar}] {color}{remaining} attempts left{Colors.ENDC}\n")
    
    def display_guess_history(self):
       
        if self.game_history:
            print(f"{Colors.BOLD}{Colors.YELLOW}📝 Your Guess History:{Colors.ENDC}")
            history_str = " → ".join([f"{Colors.CYAN}{g}{Colors.ENDC}" for g in self.game_history[-5:]])
            print(f"{history_str}\n")
    
    def play_game(self):
        
        self.generate_number()
        self.clear_screen()
        self.print_banner()
        
        print(f"{Colors.BOLD}{Colors.GREEN}🎮 GAME STARTED!{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}Difficulty: {Colors.YELLOW}{self.difficulty}{Colors.ENDC}")
        print(f"{Colors.BOLD}Range: {Colors.CYAN}{self.min_range} - {self.max_range}{Colors.ENDC}")
        print(f"{Colors.BOLD}Max Attempts: {Colors.GREEN}{self.max_attempts}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}\n")
        
        game_won = False
        
        while self.attempts < self.max_attempts:
            try:
                
                self.display_progress_bar()
                self.display_guess_history()
                
                
                guess = int(input(f"{Colors.BOLD}{Colors.MAGENTA}🎯 Enter your guess ({self.min_range}-{self.max_range}): {Colors.ENDC}"))
                
                
                if guess < self.min_range or guess > self.max_range:
                    print(f"{Colors.RED}✗ Please enter a number between {self.min_range} and {self.max_range}!{Colors.ENDC}\n")
                    continue
                
                self.attempts += 1
                self.game_history.append(guess)
                
                if guess == self.secret_number:
                    game_won = True
                    break
               
                print(f"\n{Colors.BOLD}{'─'*70}{Colors.ENDC}")
                print(f"{Colors.BOLD}Attempt #{self.attempts}:{Colors.ENDC} {guess}")
                
                if guess < self.secret_number:
                    print(f"{Colors.YELLOW}📈 Too LOW! Try a HIGHER number!{Colors.ENDC}")
                else:
                    print(f"{Colors.YELLOW}📉 Too HIGH! Try a LOWER number!{Colors.ENDC}")
                
                print(self.get_hint(guess))
                print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}\n")
                
            except ValueError:
                print(f"{Colors.RED}✗ Invalid input! Please enter a valid number.{Colors.ENDC}\n")
                continue
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Game interrupted!{Colors.ENDC}")
                return False
        
        self.clear_screen()
        self.print_banner()
        
        self.total_games += 1
        
        if game_won:
            self.total_wins += 1
            if self.attempts < self.best_score:
                self.best_score = self.attempts
            
            print(f"\n{Colors.GREEN}{Colors.BOLD}{'='*70}")
            print(f"{'🎉 ' * 17}")
            print(f"           CONGRATULATIONS! YOU WON! 🏆")
            print(f"{'🎉 ' * 17}")
            print(f"{'='*70}{Colors.ENDC}\n")
            
            print(f"{Colors.CYAN}┌{'─'*68}┐")
            print(f"│ {Colors.BOLD}Secret Number:{Colors.ENDC} {Colors.GREEN}{self.secret_number}{Colors.ENDC}{' '*(52-len(str(self.secret_number)))} │")
            print(f"│ {Colors.BOLD}Attempts Used:{Colors.ENDC} {Colors.YELLOW}{self.attempts}{Colors.ENDC}/{self.max_attempts}{' '*(50-len(str(self.attempts))-len(str(self.max_attempts)))} │")
            print(f"│ {Colors.BOLD}Difficulty:{Colors.ENDC} {Colors.MAGENTA}{self.difficulty}{Colors.ENDC}{' '*(56-len(self.difficulty))} │")
            
            if self.attempts <= 3:
                rating = "🌟🌟🌟 GENIUS!"
            elif self.attempts <= 5:
                rating = "🌟🌟 EXCELLENT!"
            elif self.attempts <= 7:
                rating = "🌟 GOOD JOB!"
            else:
                rating = "✓ WELL DONE!"
            
            print(f"│ {Colors.BOLD}Rating:{Colors.ENDC} {Colors.GREEN}{rating}{Colors.ENDC}{' '*(61-len(rating))} │")
            print(f"└{'─'*68}┘{Colors.ENDC}\n")
            
        else:
            # Game lostt
            print(f"\n{Colors.RED}{Colors.BOLD}{'='*70}")
            print(f"           💔 GAME OVER! Better luck next time! 💔")
            print(f"{'='*70}{Colors.ENDC}\n")
            
            print(f"{Colors.CYAN}┌{'─'*68}┐")
            print(f"│ {Colors.BOLD}Secret Number was:{Colors.ENDC} {Colors.GREEN}{self.secret_number}{Colors.ENDC}{' '*(45-len(str(self.secret_number)))} │")
            print(f"│ {Colors.BOLD}You used all {self.max_attempts} attempts!{Colors.ENDC}{' '*(42-len(str(self.max_attempts)))} │")
            print(f"└{'─'*68}┘{Colors.ENDC}\n")
            
            print(f"{Colors.YELLOW}💡 Tip: Try using a binary search strategy!{Colors.ENDC}\n")
        
        return True
    
    def show_instructions(self):

        self.clear_screen()
        self.print_banner()
        
        print(f"{Colors.BOLD}{Colors.CYAN}📖 HOW TO PLAY{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}\n")
        
        instructions = [
            "1️⃣  Choose your difficulty level (Easy, Medium, Hard, or Extreme)",
            "2️⃣  The computer will pick a secret number in the selected range",
            "3️⃣  You have limited attempts to guess the correct numbr",
            "4️⃣  After each guess, you'll receive helpful hints:",
            "   • 📈 Higher or 📉 Lower direction hints",
            "   • 🔥 Temperature hints (hot = close, cold = far)",
            "5️⃣  Try to guess the number in as few attempts as possible!",
            "6️⃣  Your best scores and statistics are tracked",
        ]
        
        for instruction in instructions:
            print(f"  {Colors.GREEN}{instruction}{Colors.ENDC}")
        
        print(f"\n{Colors.YELLOW}🎯 PRO TIPS:{Colors.ENDC}")
        tips = [
            "• Use binary search: Start with the middle number",
            "• Pay attention to temperature hints for faster results",
            "• Keep track of your previous guesses",
            "• Practice makes perfect!"
        ]
        
        for tip in tips:
            print(f"  {Colors.CYAN}{tip}{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}{'─'*70}{Colors.ENDC}")
        input(f"\n{Colors.BOLD}Press Enter to return to menu...{Colors.ENDC}")
    
    def show_leaderboard(self):

        self.clear_screen()
        self.print_banner()
        
        print(f"{Colors.BOLD}{Colors.YELLOW}🏆 YOUR ACHIEVEMENTS{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}\n")
        
        if self.total_games == 0:
            print(f"{Colors.YELLOW}No games played yet! Start playing to see your stats here.{Colors.ENDC}\n")
        else:
            win_rate = (self.total_wins / self.total_games) * 100
            
            print(f"{Colors.GREEN}Total Games Played:{Colors.ENDC} {self.total_games}")
            print(f"{Colors.GREEN}Total Wins:{Colors.ENDC} {self.total_wins}")
            print(f"{Colors.GREEN}Win Rate:{Colors.ENDC} {win_rate:.1f}%")
            
            if self.best_score != float('inf'):
                print(f"{Colors.GREEN}Best Score:{Colors.ENDC} {self.best_score} attempts")
            
            print()
            
            if self.total_wins >= 10:
                print(f"{Colors.YELLOW}🏆 MASTER PLAYER - Won 10+ games!{Colors.ENDC}")
            if self.total_wins >= 5:
                print(f"{Colors.YELLOW}🥇 EXPERT - Won 5+ games!{Colors.ENDC}")
            if self.best_score <= 3:
                print(f"{Colors.YELLOW}🧠 GENIUS - Won a game in 3 attempts or less!{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}{'─'*70}{Colors.ENDC}")
        input(f"\n{Colors.BOLD}Press Enter to return to menu...{Colors.ENDC}")
    
    def main_menu(self):
    
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_stats()
            
            print(f"{Colors.BOLD}{Colors.CYAN}🎮 MAIN MENU{Colors.ENDC}")
            print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}")
            print(f"  {Colors.GREEN}[1]{Colors.ENDC} 🎯 Play Game")
            print(f"  {Colors.GREEN}[2]{Colors.ENDC} 📖 How to Play")
            print(f"  {Colors.GREEN}[3]{Colors.ENDC} 🏆 View Achievements")
            print(f"  {Colors.RED}[4]{Colors.ENDC} 🚪 Exit Game")
            print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}")
            
            choice = input(f"\n{Colors.BOLD}{Colors.MAGENTA}Enter your choice (1-4): {Colors.ENDC}").strip()
            
            if choice == '1':
                self.select_difficulty()
                if self.play_game():
                    play_again = input(f"\n{Colors.BOLD}Play again? (yes/no): {Colors.ENDC}").strip().lower()
                    if play_again not in ['yes', 'y']:
                        continue
                    else:
                        self.select_difficulty()
                        self.play_game()
            
            elif choice == '2':
                self.show_instructions()
            
            elif choice == '3':
                self.show_leaderboard()
            
            elif choice == '4':
                self.clear_screen()
                print(f"\n{Colors.CYAN}{'─'*70}")
                print(f"{Colors.BOLD}{Colors.GREEN}Thanks for playing! Come back soon! 👋{Colors.ENDC}")
                print(f"{Colors.CYAN}{'─'*70}{Colors.ENDC}\n")
                break
            
            else:
                print(f"\n{Colors.RED}✗ Invalid choice! Please select 1-4.{Colors.ENDC}")
                time.sleep(1)

def main():
    game = NumberGuessingGame()
    game.main_menu()

if __name__ == "__main__":
    main()