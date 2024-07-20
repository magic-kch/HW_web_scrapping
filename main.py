from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
import json


def write_data_to_file(result_list):
    with open("result.json", "w", encoding="utf-8") as file:
        json.dump(result_list, file, ensure_ascii=False, indent=4)
    print(f"Сформирован файл result.json с {len(result_list)} записями")


def wait_element(browser, delay_seconds=1, by=By.CLASS_NAME, value=None):
    return WebDriverWait(browser, delay_seconds).until(
        expected_conditions.presence_of_element_located((by, value))
    )


path = ChromeDriverManager().install()

main_link_search = r"https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"

browser_service = Service(executable_path=path)
browser = Chrome(service=browser_service)
browser.get(main_link_search)

vacancy_list_tag = browser.find_element(By.CLASS_NAME, "vacancy-serp-content")
vacancy_all_data = vacancy_list_tag.find_elements(By.CLASS_NAME, "vacancy-search-item__card")

parsed_data = []

for vacancy in vacancy_all_data:

    h2 = wait_element(vacancy, 1, By.TAG_NAME, "h2")
    title = h2.text.strip()

    a_tag = wait_element(h2, 1, By.TAG_NAME, "a")
    link = a_tag.get_attribute("href")

    cash = wait_element(vacancy, 1, By.CLASS_NAME, "fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni")
    if cash.text:
        cash = cash.text
    else:
        cash = "Зарплата не указана"

    company = wait_element(vacancy, 1, By.CLASS_NAME, "company-info-text--vgvZouLtf8jwBmaD1xgp")
    company = company.text

    city = wait_element(vacancy, 1, By.CSS_SELECTOR, 'span[data-qa="vacancy-serp__vacancy-address"]')
    city = city.text

    parsed_data.append(
        {
            "title": title,
            "link": link,
            "cash": cash.replace('\u202f', '').strip(),
            "company": company.strip(),
            "city": city
        }
    )


result_data = dict()

for item in parsed_data:
    browser.get(item["link"])
    try:
        vacancy_data = browser.find_element(By.CLASS_NAME, "g-user-content")
        vacancy_data = vacancy_data.text

        if "flask" in vacancy_data.lower() or "django" in vacancy_data.lower() :
            result_data[item["title"]] = {"Зарплата": item["cash"],
                                          "Название компании": item["company"],
                                          "Город": item["city"],
                                          "Ссылка": item["link"]}

    except:
        continue

pprint(result_data)
browser.close()
write_data_to_file(result_data)