from multiprocessing import Process
import argparse
import csv
import os
import apache_pulsar
import redpanda

REDPANDA_IP = os.getenv('REDPANDA_IP', 'localhost')
REDPANDA_PORT = os.getenv('REDPANDA_PORT', '29092')
REDPANDA_TOPIC = os.getenv('REDPANDA_TOPIC', 'ratings')
PULSAR_IP = os.getenv('PULSAR_IP', 'localhost')
PULSAR_PORT = os.getenv('PULSAR_PORT', '6650')
PULSAR_TOPIC = os.getenv('PULSAR_TOPIC', 'views')

RATINGS_DATA = "data/product_ratings.csv"
VIEWS_DATA = "data/product_views.csv"


def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise argparse.ArgumentTypeError("%r not a floating-point literal" % (x,))
    if x < 0.0 or x > 3.0:
        raise argparse.ArgumentTypeError("%r not in range [0.0, 3.0]" % (x,))
    return x


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--stream-delay', type=restricted_float, default=2.0,
                        help='Seconds to wait before producing a new message (MIN=0.0, MAX=3.0)')
    value = parser.parse_args()
    return value


def generate_ratings():
    while True:
        with open(RATINGS_DATA) as file:
            csvReader = csv.DictReader(file)
            for rows in csvReader:
                data = {
                    'userId': rows['userId'],
                    'userName': rows['userName'],
                    'productId': rows['productId'],
                    'productName': rows['productName'],
                    'rating': rows['rating'],
                    'timestamp': rows['timestamp']
                }
                yield data


def generate_views():
    while True:
        with open(VIEWS_DATA) as file:
            csvReader = csv.DictReader(file)
            for rows in csvReader:
                data = {
                    'userId': rows['userId'],
                    'userName': rows['userName'],
                    'productId': rows['productId'],
                    'productName': rows['productName'],
                    'timestamp': rows['timestamp']
                }
                yield data


def main():
    args = parse_arguments()
    process_list = list()

    p3 = Process(target=lambda: redpanda.producer(
        REDPANDA_IP, REDPANDA_PORT, REDPANDA_TOPIC, generate_ratings, args.stream_delay))
    p3.start()
    process_list.append(p3)
    p4 = Process(target=lambda: redpanda.consumer(
        REDPANDA_IP, REDPANDA_PORT, REDPANDA_TOPIC, "Redpanda"))
    p4.start()
    process_list.append(p4)

    p7 = Process(target=lambda: apache_pulsar.producer(
        PULSAR_IP, PULSAR_PORT, PULSAR_TOPIC, generate_views, args.stream_delay))
    p7.start()
    process_list.append(p7)
    p8 = Process(target=lambda: apache_pulsar.consumer(
        PULSAR_IP, PULSAR_PORT, PULSAR_TOPIC, "Pulsar"))
    p8.start()
    process_list.append(p8)

    for process in process_list:
        process.join()


if __name__ == "__main__":
    main()
