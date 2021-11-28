import csv
import random
import time

number_of_people = 50
number_of_stores = 3
max_number_of_transactions = 10
max_number_of_social_account = 3

user_names_list = ['Krystle Blas', 'Jeri Tardy', 'Clarinda Sappington', 'Jonas Parkerson', 'Florance Yaeger',
                   'Carlton Casaus', 'Nathanial Bridgers', 'Ivana Stmartin', 'Alethea Shedrick', 'Mirian Scarbrough',
                   'Randal Blackshire', 'Jean Mathena', 'Wally Zamzow', 'Vern Proto', 'Rodney Yale', 'Shari Damelio',
                   'Davis Calbert', 'Ozie Rowan', 'Dot Brautigam', 'Ileen Brungardt', 'Leslie Knope', 'Ann Perkins',
                   'Mark Brendanawicz', 'Tom Haverford', 'Ron Swanson', 'April Ludgate', 'Andy Dwyer', 'Ben Wyatt',
                   'Chris Traeger', 'Jerry Gergich', 'Donna Meagle', 'Craig Middlebrooks', 'Marlene Griggs-Knope',
                   'Jean-Ralphio Saperstein', 'Tammy Swanson', 'Philip J. Fry', 'Turanga Leela', 'Amy Wong', 'Hermes Conrad',
                   'Hubert J. Farnsworth', 'John Zoidberg', 'Zapp Brannigan', 'Kif Kroker', 'Cubert Farnsworth',
                   'Linda van Schoonhoven', 'Morbo the Annihilator', 'Barbados Slim']
number_of_user = len(user_names_list)

phone_model_list = ['Apple iPhone 12', 'iPhone 12 mini', 'Samsung Galaxy S20', 'Galaxy S20+', 'Galaxy S20 Ultra', 'Apple iPhone SE',
                    'Samsung Galaxy A21s', 'Apple iPhone 12 Pro Max', 'Samsung Galaxy A11', 'Xiaomi Redmi Note 9 Pro', 'Redmi 8A', 'Redmi 8', 'Oppo A5', 'Huawei P30']
number_of_phones = len(phone_model_list)


def random_timestamp(start="2020-01-01T00:00",
                     end="2021-01-01T00:00",
                     time_format='%Y-%m-%dT%H:%M'):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


fieldnames = ['userId', 'userName', 'productId', 'productName', 'rating', 'timestamp']
with open('product_ratings.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for user in user_names_list:
        phones_list = random.choices(phone_model_list, k=random.randint(1, 4))
        for phone in phones_list:
            writer.writerow({'userId': user_names_list.index(user),
                             'userName': user,
                             'productId': phone_model_list.index(phone),
                             'productName': phone,
                             'rating': random.randint(1, 5),
                             'timestamp': random_timestamp()})


fieldnames = ['userId', 'userName', 'productId', 'productName', 'timestamp']
with open('product_views.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for user in user_names_list:
        phones_list = random.choices(phone_model_list, k=random.randint(1, 4))
        for phone in phones_list:
            writer.writerow({'userId': user_names_list.index(user),
                             'userName': user,
                             'productId': phone_model_list.index(phone),
                             'productName': phone,
                             'timestamp': random_timestamp()})
