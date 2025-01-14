from django.shortcuts import render
from main.statistics_page import calculate_statistics
from main.demand import calculate_demand
from main.geography import calculate_geography
from main.skills import calculate_skills
from main.models import *
from main.parser_hh import get_all_vacancies, parse_vacancy

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {})

def statistics_page(request):
    stats = (calculate_statistics())
    return render(request, 'main/statistics.html', stats)

def demand_page(request):
    stats = calculate_demand()
    return render(request, 'main/demand.html', stats)

def geography_page(request):
    stats = calculate_geography()
    return render(request, 'main/geography.html', stats) 

def skills_page(request):
    stats = calculate_skills()
    return render(request, 'main/skills.html', stats)  

def latest_vacancies(request):
    vacancies = get_all_vacancies("Python-разработчик")
    vacancy_info_list = []
    for vacancy in vacancies:
        vacancy_info = parse_vacancy(vacancy[0])
        
        if not vacancy_info:
            continue
        
        vacancy_info["region_name"] = vacancy[1]

        vacancy_info_list.append(vacancy_info)
        
        if len(vacancy_info) == 10:
            break
    return render(request, 'main/latest_vacancies.html', {"vacancy_info_list":vacancy_info_list[:10]})

