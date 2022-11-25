from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json

try:
    url = r'https://egrul.nalog.ru/index.html'
    options = webdriver.ChromeOptions()
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")
    service = webdriver.chrome.service.Service(r'/home/ivan/.ssh/selenium_manual/chrom/chromedriver')
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(url=url)
    find_region = browser.find_element(by='name', value='query')
    name_orgs: str = input('Введите запрос на организации (например окология, хозяйство, буз): ')
    find_inn = browser.find_element(by='xpath', value='//*[@id="query"]').send_keys(name_orgs)
    browser.find_element(by='xpath', value='//*[@id="query"]').send_keys(Keys.ENTER)
    sleep(2)
    number: int = int(browser.find_elements(by='class name', value='lnk-page')[-2].text)
    punkt = 1

    for number_page in range(number):
        print(f'Делаем {punkt}/{number}')
        punkt += 1
        count = 0
        sleep(1)
        all_page = browser.find_elements(by='xpath', value='//div[@class="res-row"]')

        for org in all_page:
            name_org = org.find_element(by='class name', value='op-excerpt').text.strip()
            info_org_list = org.find_element(by='class name', value="res-text").text.split(',')
            adress = []
            Dct = {name_org: {}}
            count += 1

            for i in info_org_list:
                if ':' in i:
                    point = i.split(':')[0].strip()
                    vale = i.split(':')[1].strip()
                    Dct[name_org].setdefault(point, vale)
                else:
                    adress += [i]

            if adress:
                Dct[name_org]['Адрес'] = ' '.join(adress).replace('  ', ' ').strip()

            if 'Дата прекращения деятельности' not in Dct[name_org]:
                with open(f'{name_orgs}.json', 'a', encoding='utf-8') as file:
                    json.dump(Dct, file, indent=4, ensure_ascii=False)
            else:
                with open(f'{name_orgs}_ликвидированные.json', 'a', encoding='utf-8') as file:
                    json.dump(Dct, file, indent=4, ensure_ascii=False)
        browser.find_element(by='class name', value='lnk-page-next').click()
        sleep(2)
    print('Готово!')

except Exception as EX:
    print(EX)

finally:
    browser.close()
    browser.quit()
