import requests
from bs4 import BeautifulSoup
from datetime import datetime

def download_html(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print("Ошибка при загрузке веб-страницы:", str(e))
        return None

def parse_schedule(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    schedule_dict = {}

    for li in soup.find_all('li'):
        a = li.find('a')
        if a:
            link = a['href']
            text_span = a.find('span', class_='text')
            if text_span:
                text = text_span.get_text(strip=True)
                day = text.split()[-1].lower()
                schedule_dict[day] = link

    return schedule_dict


def is_file_up_to_date(file_name):
    today = datetime.now()
    try:
        file_date = datetime.strptime(file_name.split('.')[0], '%d.%m')
        return file_date >= today
    except ValueError:
        return False

url = 'https://xn--85-6kc3bfr2e.xn--80acgfbsl1azdqr.xn--p1ai/?section_id=13'
html_content = download_html(url)

if html_content:
    schedule_dict = parse_schedule(html_content)
    for day, link in schedule_dict.items():
        if is_file_up_to_date(day + ".pdf"):
            print(f"{day}: {link} - актуально")
        else:
            print(f"{day}: {link} - неактуально")
          
