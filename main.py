import os
import requests
from terminaltables import AsciiTable
from dotenv import load_dotenv


def fetch_hh_vacancies(language):
    api_url = f"https://api.hh.ru/vacancies"
    pages = None
    page = 0
    vacancies_list = []
    while page != pages:
        response = requests.get(
            api_url,
            params={
                "text": f"Программист {language}",
                "area": 1,
                "period": 30,
                "page": page,
            })
        pages = response.json().get('pages')
        vacancies_list.extend(response.json()['items'])
        page += 1
    return vacancies_list


def get_predict_rub_salary_hh(vacancy):
    if not vacancy.get('salary'):
        return None
    if vacancy['salary'].get('currency') != 'RUR':
        return None
    salary_from = vacancy['salary'].get('from')
    salary_to = vacancy['salary'].get('to')
    return get_predict_salary(salary_from, salary_to)


def get_avg_salary(vacancies_predicted_salary):
    vacancies_avg_salary = [predict_salary for predict_salary in vacancies_predicted_salary if predict_salary]
    language_avg_salary = int(sum(vacancies_avg_salary) / len(vacancies_avg_salary))
    return language_avg_salary, len(vacancies_avg_salary)


def get_superjob_acces_token():
    auth_url = "https://api.superjob.ru/2.0/oauth2/password/"
    params = {
        "login": os.getenv('login'),
        "password": os.getenv('password'),
        "client_id": os.getenv('client_id'),
        "client_secret": os.getenv('client_secret')
    }
    response = requests.get(auth_url, params=params)
    return response.json()['access_token']


def fetch_superjob_vacancies(language):
    api_url = "https://api.superjob.ru/2.0/vacancies/"
    token = get_superjob_acces_token()
    secret_key = os.getenv("client_secret")
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Api-App-Id": secret_key
    }

    more = True
    page = 0
    vacancies_list = []
    while more:
        response = requests.get(
            api_url,
            headers=headers,
            params={
                "keyword": f"Программист {language}",
                "town": 4,
                "catalogues": 48,
                "page": page
            })
        more = response.json().get('more')
        vacancies_list.extend(response.json()['objects'])
        page += 1
    return vacancies_list


def get_predict_rub_salary_sj(vacancy):
    if vacancy.get('currency') != 'rub':
        return None
    salary_from = vacancy.get('payment_from')
    salary_to = vacancy.get('payment_to')
    return get_predict_salary(salary_from, salary_to)


def get_predict_salary(salary_from, salary_to):
    if salary_to and salary_from:
        return (salary_from + salary_to) / 2
    if salary_from:
        return salary_from * 1.2
    if salary_to:
        return salary_to * 0.8


def generate_hh_vacancies_report(programming_languages):
    salary_report = dict()
    for language in programming_languages:
        vacancies = fetch_hh_vacancies(language)
        count = len(vacancies)
        vacancies_predict_salary = [get_predict_rub_salary_hh(vacancy) for vacancy in vacancies]
        avg_salary, vacancies_processed = get_avg_salary(vacancies_predict_salary)
        salary_report[language] = {
            "vacancies_found": count,
            "vacancies_processed": vacancies_processed,
            "average_salary": avg_salary
        }
    return salary_report


def generate_sj_vacancies_report(programming_languages):
    salary_report = dict()
    for language in programming_languages:
        vacancies = fetch_superjob_vacancies(language)
        vacancies_predict_salary = [get_predict_rub_salary_sj(vacancy) for vacancy in vacancies]
        count = len(vacancies)
        avg_salary, vacancies_processed = get_avg_salary(vacancies_predict_salary)
        salary_report[language] = {
            "vacancies_found": count,
            "vacancies_processed": vacancies_processed,
            "average_salary": avg_salary
        }
    return salary_report


def print_statistics(salary_report, report_title):
    table_data = [
        ["Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]
    ]
    for item in salary_report.items():
        language = item[0]
        vacancy_stats_info = [*item[1].values()]
        row_data = [language, *vacancy_stats_info]
        table_data.append(row_data)

    table = AsciiTable(table_data)
    table.title = report_title
    print(table.table)


if __name__ == '__main__':
    most_popular_languages = [
        "Java Script",
        "Python",
        "JAVA",
        "C++",
        "C",
        "PHP",
        "Go"
    ]
    load_dotenv()
    hh_salary_report = generate_hh_vacancies_report(most_popular_languages)
    sj_salary_report = generate_sj_vacancies_report(most_popular_languages)
    print_statistics(sj_salary_report, "SuperJob Moscow")
    print_statistics(hh_salary_report, "HeadHunter Moscow")