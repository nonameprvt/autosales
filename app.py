import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template

# К покупке рассматриваем только бензиновые и дизельные машины.
# Да, за электромобилями будущее, да, они могут разгоняться гораздо быстрее
# и во многом прикольнее, но в электромобиле никогда не будет чувствоваться
# жизнь автомобиля, его душа. Никогда не будет услышан дерзкий и красивый рёв
# мощного V8 или же рядной шестерки баварских гениев автомобилестроения.
# Вообщем без лишних слов понятно, что я любитель настоящих машин, большой
# поклонник старых немецких машин. Поэтому предлагаю клиентам своего приложения
# к просмотру исключительно живые бензиновые и дизельные агрегаты. Но если быть
# честным полностью, то я за бензиновые машины. Единственный дизель, который я
# рекомендую к покупке - трехлитровые BMW. Они действительно надежные.


# Извиняюсь за столь долгое вступление, я просто должен был объяснить, почему
# выбрал именно такой проект.


# Ну а если кратко: зачем жто нужно? Вот вы захотели купить себе новую машину.
# Куда вы пойдете смотреть на объявления? На Авто.ру и Дром. Не ехать в салон же
# во время пандемии! Ну а почему бы не объединить эти два ресурса и не упростить
# себе жизнь! Получайте удовольствие от быстрого поиска автомобилей на наиболее
# популярных площадках России!


# Помимо самих автомобилей вы можете указать в поиске коэффициент крутости авто.
# Конечно, это мое субъективное мнение, но все же это может быть полезно.


page_end = 3
response_id = 200
car_names = []
car_prices = []
car_engine = []
car_kpp = []
car_kuzov = []
car_privod = []
car_complectation = []
car_options = []
car_probeg = []
car_link = []
car_price_status = []
car_characteristics = []
checkup = []
for page_id in range(1, page_end):
    try:
        response = requests.get(
            f'https://auto.ru/moskva/cars/new/?engine_group=DIESEL&engine_group'
            f'=GASOLINE&sort=fresh_relevance_1-desc&output_type=list&page='
            f'{page_id}', timeout=20)
    except IndexError:
        break
    if response.status_code != response_id:
        break
    soup = BeautifulSoup(response.content, "html.parser")
    for car in soup.find_all('h3',
                             'ListingItemTitle ListingItem-module__title'):
        car_names.append(car.text)
    for car in soup.find_all('div', 'ListingItemPrice-module__content'):
        car_prices.append(
            car.text.replace('\xa0', '').replace('от ', '').replace('₽', ''))
    for car in soup.find_all('div', 'ListingItemTechSummaryDesktop__cell'):
        car_characteristics.append(car.text)
    for car in soup.find_all('div', 'ListingItem-module__kmAge'):
        car_probeg.append(car.text.replace('\xa0', '.'))
    for car in soup.find_all('a', 'Link ListingItemTitle__link'):
        car_link.append(car['href'])
    counter = 0
    while counter < len(car_characteristics):
        if counter % 6 == 0:
            car_engine.append(
                car_characteristics[counter].replace('\xa0', ' ').replace(
                    '\u2009', ' '))
        elif counter % 6 == 1:
            car_kpp.append(car_characteristics[counter])
        elif counter % 6 == 2:
            car_kuzov.append(car_characteristics[counter])
        elif counter % 6 == 3:
            car_privod.append(car_characteristics[counter])
        elif counter % 6 == 4:
            car_complectation.append(car_characteristics[counter])
        else:
            car_options.append(
                car_characteristics[counter].replace('\xa0', ' '))
        counter += 1
    car_characteristics.clear()
count_prices = len(car_prices)
i = 0
while i < count_prices:
    if car_prices[i][0] == 'д':
        car_prices.pop(i)
        count_prices -= 1
    i += 1

auto = len(car_names)

for page_id in range(1, page_end):
    try:
        response = requests.get(f'https://moscow.drom.ru/auto/new/all/page'
                                f'{page_id}/?fueltype=1', timeout=20)
    except IndexError:
        break
    if response.status_code != response_id:
        break
    drom = BeautifulSoup(response.content, "html.parser")
    for car in drom.find_all('div', 'css-1svsmzw e1vivdbi2'):
        car_names.append(car.text[:len(car.text) - 6])
    for car in drom.find_all('div', 'css-1dv8s3l e1lt6hpz1'):
        car_prices.append(car.text.replace('\xa0₽', '').replace(' ', ''))
    for car in drom.find_all('a', 'css-1psewqh ewrty961'):
        car_link.append(car['href'])
    for car in drom.find_all('div', 'css-3xai0o e162wx9x0'):
        checkup.append(car.text)

for page_id in range(1, page_end):
    try:
        response = requests.get(f'https://moscow.drom.ru/auto/new/all/page'
                                f'{page_id}/?fueltype=2', timeout=20)
    except IndexError:
        break
    if response.status_code != response_id:
        break
    drom = BeautifulSoup(response.content, "html.parser")
    for car in drom.find_all('div', 'css-1svsmzw e1vivdbi2'):
        car_names.append(car.text[:len(car.text) - 6])
    for car in drom.find_all('div', 'css-1dv8s3l e1lt6hpz1'):
        car_prices.append(car.text.replace('\xa0₽', '').replace(' ', ''))
    for car in drom.find_all('a', 'css-1psewqh ewrty961'):
        car_link.append(car['href'])
    for car in drom.find_all('div', 'css-3xai0o e162wx9x0'):
        checkup.append(car.text)

counter = len(checkup)
for i in range(counter - 1, -1, -1):
    if i % 20 == 0 or i % 20 == 1:
        car_names.pop(auto + i)
        car_prices.pop(auto + i)
        car_link.pop(auto + i)
        checkup.pop(i)
        i -= 1
for elem in checkup:
    elements = [str(x) for x in elem.split(',')]
    if len(elements) >= 4:
        if elements[0].find('(') == -1:
            elements[0] = (elements[0][:3] + "л (199 л.c)")
        else:
            if elements[1] == ' бензин':
                elements[1] = ' Бензин'
            elif elements[1] == ' дизель':
                elements[1] = ' Дизель'
            car_engine.append(
                elements[0].replace('(', '/ ').replace(')', ' /') + elements[1])
        if elements[2] == ' АКПП':
            elements[2] = 'Автомат'
        elif elements[2] == ' механика':
            elements[2] = 'Механика'
        elif elements[2] == ' автомат':
            elements[2] = 'Автомат'
        elif elements[2] == ' робот':
            elements[2] = 'Робот'
        else:
            elements[2] = 'Вариатор'
        car_kpp.append(elements[2])
        if elements[3] == ' 4WD':
            elements[3] = 'Полный'
        elif elements[3] == ' передний':
            elements[3] = 'Передний'
        else:
            elements[3] = 'Задний'
        car_privod.append(elements[3])
    else:
        car_engine.append("1.3 л / 150 л.c. / Бензин")
        car_kpp.append("Робот")
        car_privod.append("Передний")

car_coolness = []

for i in range(len(car_names)):
    cool = 0
    if 'BMW' in car_names[i] or 'Mercedes' in car_names[i] or 'Audi' in \
            car_names[i] or 'Ferrari' in car_names[i] or 'Lamborghini' in \
            car_names[i] or 'Brabus' in car_names[i] or 'Skoda' in car_names[i]\
            or 'Porsche' in car_names[i] or 'Lexus' in car_names[i]:
        cool += 2
    elif 'Volkswagen' in car_names[i] or 'Kia' in car_names[i] \
            or 'Mitsubishi' in car_names[i] or 'Toyota' in car_names[i] \
            or 'Nissan' in car_names[i]:
        cool += 1
    if int(car_engine[i][0]) >= 3:
        cool += 2
    elif int(car_engine[i][0]) >= 2:
        cool += 1
    if int(car_engine[i][8:11]) >= 300:
        cool += 2
    elif int(car_engine[i][8:11]) >= 200:
        cool += 1
    if car_kpp[i] == 'автомат' or car_kpp[i] == 'робот':
        cool += 2
    elif car_kpp[i] == 'вариатор':
        cool += 1
    if car_privod[i] == 'полный':
        cool += 2
    elif car_privod[i] == 'задний':
        cool += 1
    car_coolness.append(cool)

df = pd.DataFrame(
    {
        'Name': car_names,
        'Engine': car_engine,
        'Price': car_prices,
        'KPP': car_kpp,
        'Privod': car_privod,
        'Link': car_link,
        'Cool': car_coolness
    }
)

app = Flask(__name__)


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/data", methods=["POST", "GET"])
def data():
    if request.method == "GET":
        return (
            f"The URL /data is accessed directly."
            f"Try going to '/form' to submit form"
        )
    if request.method == "POST":
        return render_template("data.html", df=df)


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
