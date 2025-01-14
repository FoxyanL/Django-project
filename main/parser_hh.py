import requests
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
}


def parse_vacancy(id):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
    }
    response = requests.get(f"https://spb.hh.ru/vacancy/{id}", headers=headers)
    
    #print(response.url)
    
    if response.status_code != 200:
        print("Бан")
        return {}
    
    vacancy_info = {}
    
    soup = BeautifulSoup(response.content, "lxml")
    
    #print(response.text)
    name = soup.find("h1")

    if name is None:
        return {}
    
    name = name.text

    description_blocks = soup.find(class_="vacancy-description").find_all(class_="vacancy-section")
    skills_block = []
    skills = []

    description = description_blocks[0].text
        
    for description_block in description_blocks:
        if description_block.find("h2") is not None and description_block.find("h2").text == "Ключевые навыки":
            skills_block = description_block.find("ul").find_all("li")

    if not skills_block:
        return {}

    
    for skill in skills_block:
        skills.append(skill.text)    
    
    company_name = soup.find("span", class_="vacancy-company-name").text

    salary = soup.find(attrs={"data-qa": "vacancy-salary"}).text

    vacancy_info["name"] = name
    vacancy_info["description"] = description
    vacancy_info["skills"] = ", ".join(skills)
    vacancy_info["company_name"] = company_name
    vacancy_info["salary"] = salary
    vacancy_info['publication_date'] = datetime.now().date()
    

    return vacancy_info


def get_all_vacancies(text):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 YaBrowser/24.12.0.0 Safari/537.36',
    }
    url = f"https://spb.hh.ru/search/vacancy?text={'+'.join(text.split())}&excluded_text=&salary=&currency_code=RUR&only_with_salary=true&experience=doesNotMatter&order_by=publication_time&search_period=1&items_on_page=50"

    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, "lxml")
        
    vacancy_cards = soup.find(
        attrs={"data-qa": "vacancy-serp__results"}).find_all(class_="magritte-redesign")
    
    vacancies_list = []
    
    for card_index in range(len(vacancy_cards)):
        vacancy_card = vacancy_cards[card_index]
        
        region_name = vacancy_card.find(
            attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
        
        vacancy_id = vacancy_card.find("h2").find("a").get("href").split("/")[-1].split("?")[0]
        
        vacancies_list.append([vacancy_id, region_name])
        
    return vacancies_list


