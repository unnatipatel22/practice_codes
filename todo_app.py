import json
import os
from datetime import datetime, date
from typing import List, Dict

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

class Task:
    def __init__(self, title: str, category: str, priority: str, due_date: str, 
                 completed: bool = False, created_at: str = None, tags: List[str] = None):
        self.title = title
        self.category = category
        self.priority = priority
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.tags = tags or []
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'category': self.category,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'tags': self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        return cls(**data)

class TodoApp:
    def __init__(self):
        self.tasks: List[Task] = []
        self.filename = "tasks.json"
        self.categories = {
            'Work': '💼',
            'Personal': '👤',
            'Health': '❤️',
            'Study': '📚',
            'Others': '📁'
        }
        self.load_tasks()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        
        self.clear_screen()
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}                    ✨ ToDo - TASK MANAGER ✨{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}                   Stay Organized, Stay Productive{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.ENDC}\n")
    
    def print_stats(self):
       
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        
        cat_stats = {}
        for task in self.tasks:
            if not task.completed:
                cat_stats[task.category] = cat_stats.get(task.category, 0) + 1
        
        print(f"{Colors.BOLD}📊 STATISTICS:{Colors.ENDC}")
        print(f"┌{'─'*66}┐")
        print(f"│ {Colors.GREEN}Total Tasks: {total:<5}{Colors.ENDC} │ {Colors.YELLOW}Pending: {pending:<5}{Colors.ENDC} │ {Colors.CYAN}Completed: {completed:<5}{Colors.ENDC} │")
        print(f"└{'─'*66}┘")
        
        if cat_stats:
            print(f"\n{Colors.BOLD}📁 BY CATEGORY (Pending):{Colors.ENDC}")
            for cat, count in cat_stats.items():
                emoji = self.categories.get(cat, '📁')
                print(f"  {emoji} {cat}: {count}")
        print()
    
    def display_tasks(self, tasks: List[Task] = None):
        
        if tasks is None:
            tasks = self.tasks
        
        if not tasks:
            print(f"{Colors.YELLOW}📭 No tasks found! Create your first task to get started.{Colors.ENDC}\n")
            return
        
        print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}")
        
        for idx, task in enumerate(tasks, 1):
            
            status = f"{Colors.GREEN}✓{Colors.ENDC}" if task.completed else f"{Colors.YELLOW}○{Colors.ENDC}"
            
            
            if task.priority == 'High':
                priority_color = Colors.RED
            elif task.priority == 'Medium':
                priority_color = Colors.YELLOW
            else:
                priority_color = Colors.GREEN
            
            
            cat_emoji = self.categories.get(task.category, '📁')
            
            
            if task.completed:
                title = f"{Colors.BLUE}[DONE] {task.title}{Colors.ENDC}"
            else:
                title = f"{Colors.BOLD}{task.title}{Colors.ENDC}"
            
            
            print(f"\n{Colors.BOLD}[{idx}]{Colors.ENDC} {status} {title}")
            print(f"    {cat_emoji} {task.category} | {priority_color}{task.priority}{Colors.ENDC} Priority | 📅 Due: {task.due_date}")
            
            if task.tags:
                tags_str = ' '.join([f"{Colors.PURPLE}#{tag}{Colors.ENDC}" for tag in task.tags])
                print(f"    {tags_str}")
            
            print(f"    {Colors.CYAN}Created: {task.created_at}{Colors.ENDC}")
            print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}")
    
    def add_task(self):
       
        print(f"\n{Colors.BOLD}{Colors.GREEN}➕ ADD NEW TASK{Colors.ENDC}")
        print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}\n")
        
        title = input(f"{Colors.CYAN}Task Title: {Colors.ENDC}").strip()
        if not title:
            print(f"{Colors.RED}✗ Task title cannot be empty!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        
        print(f"\n{Colors.BOLD}Select Category:{Colors.ENDC}")
        for idx, (cat, emoji) in enumerate(self.categories.items(), 1):
            print(f"  [{idx}] {emoji} {cat}")
        
        cat_choice = input(f"\n{Colors.CYAN}Enter choice (1-{len(self.categories)}) [1]: {Colors.ENDC}").strip() or "1"
        try:
            category = list(self.categories.keys())[int(cat_choice) - 1]
        except:
            category = "Work"
        
        
        print(f"\n{Colors.BOLD}Select Priority:{Colors.ENDC}")
        print(f"  [1] {Colors.RED}High{Colors.ENDC}")
        print(f"  [2] {Colors.YELLOW}Medium{Colors.ENDC}")
        print(f"  [3] {Colors.GREEN}Low{Colors.ENDC}")
        
        priority_choice = input(f"\n{Colors.CYAN}Enter choice (1-3) [2]: {Colors.ENDC}").strip() or "2"
        priority_map = {"1": "High", "2": "Medium", "3": "Low"}
        priority = priority_map.get(priority_choice, "Medium")
        
        
        due_date = input(f"\n{Colors.CYAN}Due Date (YYYY-MM-DD) [{date.today()}]: {Colors.ENDC}").strip() or str(date.today())
        
        
        tags_input = input(f"\n{Colors.CYAN}Tags (comma-separated, optional): {Colors.ENDC}").strip()
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        task = Task(
            title=title,
            category=category,
            priority=priority,
            due_date=due_date,
            tags=tags
        )
        
        self.tasks.append(task)
        self.save_tasks()
        
        print(f"\n{Colors.GREEN}✓ Task added successfully!{Colors.ENDC}")
        input("\nPress Enter to continue...")
    
    def mark_complete(self):
        
        if not self.tasks:
            print(f"{Colors.YELLOW}No tasks available!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        self.display_tasks()
        
        try:
            task_num = int(input(f"\n{Colors.CYAN}Enter task number to mark complete: {Colors.ENDC}"))
            if 1 <= task_num <= len(self.tasks):
                self.tasks[task_num - 1].completed = not self.tasks[task_num - 1].completed
                status = "completed" if self.tasks[task_num - 1].completed else "pending"
                self.save_tasks()
                print(f"\n{Colors.GREEN}✓ Task marked as {status}!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}✗ Invalid task number!{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}✗ Please enter a valid number!{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def delete_task(self):
        
        if not self.tasks:
            print(f"{Colors.YELLOW}No tasks available!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        self.display_tasks()
        
        try:
            task_num = int(input(f"\n{Colors.CYAN}Enter task number to delete: {Colors.ENDC}"))
            if 1 <= task_num <= len(self.tasks):
                confirm = input(f"{Colors.RED}Are you sure? (yes/no): {Colors.ENDC}").lower()
                if confirm in ['yes', 'y']:
                    deleted = self.tasks.pop(task_num - 1)
                    self.save_tasks()
                    print(f"\n{Colors.GREEN}✓ Task '{deleted.title}' deleted!{Colors.ENDC}")
            else:
                print(f"{Colors.RED}✗ Invalid task number!{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}✗ Please enter a valid number!{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def filter_tasks(self):
        
        print(f"\n{Colors.BOLD}🔍 FILTER TASKS{Colors.ENDC}")
        print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}\n")
        print(f"  [1] All Tasks")
        print(f"  [2] Pending Only")
        print(f"  [3] Completed Only")
        print(f"  [4] High Priority")
        print(f"  [5] Due Today")
        print(f"  [6] By Category")
        
        choice = input(f"\n{Colors.CYAN}Enter choice: {Colors.ENDC}").strip()
        
        filtered_tasks = []
        
        if choice == "1":
            filtered_tasks = self.tasks
        elif choice == "2":
            filtered_tasks = [t for t in self.tasks if not t.completed]
        elif choice == "3":
            filtered_tasks = [t for t in self.tasks if t.completed]
        elif choice == "4":
            filtered_tasks = [t for t in self.tasks if t.priority == "High"]
        elif choice == "5":
            today = str(date.today())
            filtered_tasks = [t for t in self.tasks if t.due_date == today]
        elif choice == "6":
            print(f"\n{Colors.BOLD}Select Category:{Colors.ENDC}")
            for idx, (cat, emoji) in enumerate(self.categories.items(), 1):
                count = sum(1 for t in self.tasks if t.category == cat)
                print(f"  [{idx}] {emoji} {cat} ({count})")
            
            cat_choice = input(f"\n{Colors.CYAN}Enter choice: {Colors.ENDC}").strip()
            try:
                category = list(self.categories.keys())[int(cat_choice) - 1]
                filtered_tasks = [t for t in self.tasks if t.category == category]
            except:
                print(f"{Colors.RED}✗ Invalid choice!{Colors.ENDC}")
                input("\nPress Enter to continue...")
                return
        else:
            print(f"{Colors.RED}✗ Invalid choice!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        self.clear_screen()
        self.print_header()
        print(f"{Colors.BOLD}Filtered Tasks ({len(filtered_tasks)} found){Colors.ENDC}\n")
        self.display_tasks(filtered_tasks)
        input("\n\nPress Enter to continue...")
    
    def search_tasks(self):
        keyword = input(f"\n{Colors.CYAN}🔍 Search keyword: {Colors.ENDC}").strip().lower()
        
        if not keyword:
            print(f"{Colors.RED}✗ Please enter a keyword!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        results = [t for t in self.tasks if keyword in t.title.lower() or 
                   keyword in t.category.lower() or 
                   any(keyword in tag.lower() for tag in t.tags)]
        
        self.clear_screen()
        self.print_header()
        print(f"{Colors.BOLD}Search Results for '{keyword}' ({len(results)} found){Colors.ENDC}\n")
        self.display_tasks(results)
        input("\n\nPress Enter to continue...")
    
    def clear_completed(self):
        completed_count = sum(1 for t in self.tasks if t.completed)
        
        if completed_count == 0:
            print(f"\n{Colors.YELLOW}No completed tasks to clear!{Colors.ENDC}")
            input("\nPress Enter to continue...")
            return
        
        confirm = input(f"\n{Colors.RED}Clear {completed_count} completed task(s)? (yes/no): {Colors.ENDC}").lower()
        
        if confirm in ['yes', 'y']:
            self.tasks = [t for t in self.tasks if not t.completed]
            self.save_tasks()
            print(f"\n{Colors.GREEN}✓ Cleared {completed_count} completed task(s)!{Colors.ENDC}")
        
        input("\nPress Enter to continue...")
    
    def save_tasks(self):
       
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([task.to_dict() for task in self.tasks], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"{Colors.RED}Error saving tasks: {e}{Colors.ENDC}")
    
    def load_tasks(self):
       
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
            except Exception as e:
                print(f"{Colors.RED}Error loading tasks: {e}{Colors.ENDC}")
                self.tasks = []
    
    def show_menu(self):
        print(f"\n{Colors.BOLD}{Colors.CYAN}MAIN MENU{Colors.ENDC}")
        print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}")
        print(f"  {Colors.GREEN}[1]{Colors.ENDC} ➕ Add New Task")
        print(f"  {Colors.GREEN}[2]{Colors.ENDC} 📋 View All Tasks")
        print(f"  {Colors.GREEN}[3]{Colors.ENDC} ✓  Mark Task Complete/Incomplete")
        print(f"  {Colors.GREEN}[4]{Colors.ENDC} 🗑️  Delete Task")
        print(f"  {Colors.GREEN}[5]{Colors.ENDC} 🔍 Filter Tasks")
        print(f"  {Colors.GREEN}[6]{Colors.ENDC} 🔎 Search Tasks")
        print(f"  {Colors.GREEN}[7]{Colors.ENDC} 🧹 Clear Completed Tasks")
        print(f"  {Colors.RED}[8]{Colors.ENDC} 🚪 Exit")
        print(f"{Colors.BOLD}{'─'*70}{Colors.ENDC}")
    
    def run(self):
        
        while True:
            self.print_header()
            self.print_stats()
            self.show_menu()
            
            choice = input(f"\n{Colors.CYAN}Enter your choice (1-8): {Colors.ENDC}").strip()
            
            if choice == '1':
                self.add_task()
            elif choice == '2':
                self.clear_screen()
                self.print_header()
                print(f"{Colors.BOLD}ALL TASKS ({len(self.tasks)}){Colors.ENDC}\n")
                self.display_tasks()
                input("\n\nPress Enter to continue...")
            elif choice == '3':
                self.mark_complete()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.filter_tasks()
            elif choice == '6':
                self.search_tasks()
            elif choice == '7':
                self.clear_completed()
            elif choice == '8':
                print(f"\n{Colors.CYAN}👋 Thank you for using TodoMaster!{Colors.ENDC}")
                print(f"{Colors.GREEN}✓ All tasks saved successfully!{Colors.ENDC}\n")
                break
            else:
                print(f"\n{Colors.RED}✗ Invalid choice! Please try again.{Colors.ENDC}")
                input("\nPress Enter to continue...")

def main():
    app = TodoApp()
    app.run()

if __name__ == "__main__":
    main()