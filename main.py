"""
<h2 data-qa="bloko-header-2" class="bloko-header-section-2"><span class="serp-item__title-link-wrapper"><a class="bloko-link" target="_blank" href="https://adsrv.hh.ru/click?b=1113510&amp;place=36&amp;meta=snmtHY9qhZMHQ3i9ISgr6krh8X2QB1TED5rORo5dgR0XJa6sEf9O_dK2VxUCd4V1cMpmoKmAMGp87gWPZysud4B5ofhcQzIJLZRlFnIcY6mkAbrs8oJF_babJQCRcy0Y1JhrvPJBNg5051WsNhzl-B47eCNZ1cyarVcKD07khlax_O9m-r0ceCpbyzz5z8Vu1lHf7zsc2p3IUHm_5MK5qSTi5W1WmL5cm09pgYnwnvbpuK0t3Urxp8Clohb_foBKzSWj_87Z34DIe4fenzkAcs2fai0hVUqDZ5er3oGfZTgsxfa9EUmL99mtQi6wjwm-FWuNe6cLv-CznM7aEI0D4aXIla0-7HoquUd6Kqn3cRCPpfaAkiqphUwS-ynPsUQqvo0SmW3KO1YB_lBrlas-f_4OiNbQprIzWQIrilYo5Mblb9LLYmyjx9PnJOyb5IY-46BAVe7jaQm1QmlEKX_o7p7FRx0zk2TlSihv521uR6wXdgxeedCW3CFhdvul19UBfUZBD7qMgg85ho03oUTGKg%3D%3D&amp;clickType=link_to_vacancy"><span class="vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link" data-qa="serp-item__title">Инженер-программист</span></a></span></h2>
<div class="g-user-content" data-qa="vacancy-description"><p><span>USMall — крупнейший маркетплейс американских магазинов в России, работает с 2019 года и активно развивается. На нашей витрине представлено более 1.5 млн товаров в категориях одежда, обувь, здоровье, товары для дома, игрушки и электроника. Мы постоянно развиваем новые магазины и категории. Вся наша команда распределенная, и мы предлагаем возможность удаленной работы из любой точки мира с гибкой оплатой.</span></p> <p><strong><span>Обязанности:</span></strong></p> <ul> <li><span>Разработка и поддержка веб-приложений на </span><span class="highlighted">Python</span><span>.</span></li> <li><span>Разработка и поддержка автоматизации бизнес и технических процессов.</span></li> <li><span>Проектирование архитектуры баз данных и сервисов.</span></li> <li><span>Интеграция с внешними сервисами через REST API.</span></li> <li><span>Участие в планировании и оценке задач.</span></li> </ul> <p><strong><span>Технологический стек:</span></strong></p> <ul> <li><span>FastAPI, SQLAlchemy, Pydantic (v1/v2)</span></li> <li><span>Scrapy</span></li> <li><span>Docker, Airflow, Celery, Redis</span></li> <li><span>Postgres</span></li> </ul> <p><strong><span>Требования:</span></strong></p> <ul> <li><span>Опыт работы с </span><span class="highlighted">Python</span><span> от 3 лет.</span></li> <li><span>Опыт разработки с использованием FastAPI.</span></li> <li><span>Уверенные знания SQLAlchemy.</span></li> <li><span>Опыт проектирования архитектуры сервисов.</span></li> <li><span>Умение писать чистый и поддерживаемый код.</span></li> <li><span>Опыт работы с системами контроля версий (Git).</span></li> </ul> <p><strong><span>Будет плюсом:</span></strong></p> <ul> <li><span>Знание и опыт работы с Airflow и Celery.</span></li> <li><span>Опыт работы с Kafka.</span></li> <li><span>Опыт работы с Docker и Kubernetes.</span></li> <li><span>Опыт работы с облачными платформами (AWS, GCP, Azure).</span></li> <li><span>Знание других языков программирования и технологий.</span></li> <li><span>Опыт работы с Mindbox.</span></li> </ul></div>
"""
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint


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

for vacancy in vacancy_all_data[]:

    h2 = wait_element(vacancy, 1, By.TAG_NAME, "h2")
    title = h2.text.strip()

    a_tag = wait_element(h2, 1, By.TAG_NAME, "a")
    link = a_tag.get_attribute("href")

    cash = wait_element(vacancy, 1, By.CLASS_NAME, "fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni")
    cash = cash.text

    company = wait_element(vacancy, 1, By.CLASS_NAME, "company-info-text--vgvZouLtf8jwBmaD1xgp")
    company = company.text

    # city = wait_element(vacancy, 1, By.CSS_SELECTOR, 'data-qa="vacancy-serp__vacancy-address"')
    city = ""
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

    vacancy_data = browser.find_element(By.CLASS_NAME, "g-user-content")
    vacancy_data = vacancy_data.text

    if "flask" in vacancy_data.lower() or "django" in vacancy_data.lower() :
        result_data[item["title"]] = {"Ссылка": item["link"],
                                      "Зарплата": item["cash"],
                                      "Название компании": item["company"],
                                      "Город": item["city"]}





# pprint(parsed_data)
pprint(result_data)
browser.close()
