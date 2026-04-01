import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os
from urllib.parse import urljoin, urlparse

# Color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"{Colors.BOLD}{Colors.HEADER}    🌐 WEB SCRAPER PRO - NEWS & DATA EXTRACTOR 🌐{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")

def get_user_input():
   
    while True:
        print(f"{Colors.YELLOW}📌 Enter website URL to scrape:{Colors.END}")
        print(f"{Colors.CYAN}   Examples:")
        print(f"   1. https://www.bbc.com/news")
        print(f"   2. https://www.theguardian.com/international")
        print(f"   3. https://www.ycombinator.com/")
        print(f"   4. https://www.reddit.com/{Colors.END}\n")
        
        url = input(f"{Colors.GREEN}➜ URL: {Colors.END}").strip()
        
        if not url:
            print(f"{Colors.RED}❌ Please enter a valid URL!{Colors.END}\n")
            continue
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url

def fetch_webpage(url):
   
    print(f"\n{Colors.BLUE}🔄 Fetching webpage...{Colors.END}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        print(f"{Colors.GREEN}✅ Webpage fetched successfully!{Colors.END}")
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}❌ Error fetching webpage: {str(e)}{Colors.END}")
        return None

def extract_articles(soup, base_url):
    
    articles = []
    
    # Common article selectors
    article_selectors = [
        {'tag': 'article'},
        {'class_': 'article'},
        {'class_': 'post'},
        {'class_': 'story'},
        {'class_': 'news-item'},
        {'tag': 'div', 'class_': 'athing'},  # Hacker News
        {'class_': 'thing'},  # Reddit
    ]
    
    
    for selector in article_selectors:
        found = soup.find_all(**selector, limit=15)
        if found:
            for item in found:
                article = extract_article_data(item, base_url)
                if article and article['headline']:
                    articles.append(article)
            if articles:
                break
    
   
    if not articles:
        headings = soup.find_all(['h1', 'h2', 'h3'], limit=15)
        for heading in headings:
            link_tag = heading.find('a') or heading.find_parent('a')
            if link_tag and link_tag.get('href'):
                article = {
                    'headline': heading.get_text(strip=True),
                    'link': urljoin(base_url, link_tag['href']),
                    'summary': '',
                    'date': '',
                    'category': ''
                }
                articles.append(article)
    
    return articles

def extract_article_data(element, base_url):
   
    article = {
        'headline': '',
        'link': '',
        'summary': '',
        'date': '',
        'category': ''
    }
    
    heading = element.find(['h1', 'h2', 'h3', 'h4', 'a'])
    if heading:
        article['headline'] = heading.get_text(strip=True)
    
    

    link = element.find('a')
    if link and link.get('href'):
        article['link'] = urljoin(base_url, link['href'])
    
   
    summary = element.find('p')
    if summary:
        article['summary'] = summary.get_text(strip=True)[:200]
    
    
    date_tag = element.find(['time', 'span'], class_=lambda x: x and ('date' in str(x).lower() or 'time' in str(x).lower()))
    if date_tag:
        article['date'] = date_tag.get_text(strip=True)
    
    category = element.find(['span', 'a'], class_=lambda x: x and ('category' in str(x).lower() or 'tag' in str(x).lower()))
    if category:
        article['category'] = category.get_text(strip=True)
    
    return article

def display_results(results):


    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"{Colors.BOLD}{Colors.HEADER}📰 SCRAPED RESULTS{Colors.END}")
    print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
    
    print(f"{Colors.YELLOW}Website: {Colors.END}{results['title']}")
    print(f"{Colors.YELLOW}Scraped at: {Colors.END}{results['scraped_at']}")
    print(f"{Colors.YELLOW}Total articles found: {Colors.END}{Colors.GREEN}{results['total_found']}{Colors.END}\n")
    
    for idx, article in enumerate(results['articles'], 1):
        print(f"{Colors.BOLD}{Colors.BLUE}[{idx}] {article['headline']}{Colors.END}")
        
        if article['summary']:
            print(f"    {Colors.CYAN}📝 {article['summary'][:150]}...{Colors.END}")
        
        if article['link']:
            print(f"    {Colors.GREEN}🔗 {article['link']}{Colors.END}")
        
        if article['date']:
            print(f"    {Colors.YELLOW}📅 {article['date']}{Colors.END}")
        
        if article['category']:
            print(f"    {Colors.HEADER}🏷️  {article['category']}{Colors.END}")
        
        print()

def save_to_json(results, filename):
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"{Colors.GREEN}✅ Results saved to: {filename}{Colors.END}")
        return True
    except Exception as e:
        print(f"{Colors.RED}❌ Error saving file: {str(e)}{Colors.END}")
        return False

def main():
    

    print_banner()
    
    url = get_user_input()
    
   
    html_content = fetch_webpage(url)
    if not html_content:
        return
    
   
    print(f"{Colors.BLUE}🔍 Parsing HTML content...{Colors.END}")
    soup = BeautifulSoup(html_content, 'html.parser')
    
    
    title_tag = soup.find('title')
    website_title = title_tag.get_text(strip=True) if title_tag else urlparse(url).netloc
    
    
    print(f"{Colors.BLUE}📊 Extracting articles...{Colors.END}")
    articles = extract_articles(soup, url)
    
    if not articles:
        print(f"{Colors.RED}❌ No articles found! The website structure might be different.{Colors.END}")
        return
    
   

    results = {
        'title': website_title,
        'url': url,
        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_found': len(articles),
        'articles': articles
    }
    
    
    display_results(results)
    
    save_choice = input(f"\n{Colors.YELLOW}💾 Do you want to save results to JSON? (y/n): {Colors.END}").lower()
    if save_choice == 'y':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"scraped_data_{timestamp}.json"
        save_to_json(results, filename)
    
   
    print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
    another = input(f"\n{Colors.YELLOW}🔄 Scrape another website? (y/n): {Colors.END}").lower()
    if another == 'y':
        print("\n" * 2)
        main()
    else:
        print(f"\n{Colors.GREEN}👋 Thank you for using Web Scraper Pro!{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Program interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}👋 Goodbye!{Colors.END}\n")
    except Exception as e:
        print(f"\n{Colors.RED}❌ An error occurred: {str(e)}{Colors.END}\n")