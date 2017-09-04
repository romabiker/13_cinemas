from collections import Counter
import argparse
import random
import sys


from bs4 import BeautifulSoup
import requests


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
                        '-p', '--pop_level', type=int, default=10,
                        help='min number of cinemas where film is on'
                        )
    parser.add_argument(
                        '-c', '--count', default=10, type=int,
                        help='number of top rated movies'
                        )
    return parser


def count_cinemas(in_div):
    return len(in_div.find_next('table').find_all('tr'))


def compose_proxy_url(from_ip):
    if from_ip:
        return {
                'http': 'http://{}'.format(from_ip),
                }


def extract_rating(from_html):
    soup = BeautifulSoup(from_html, 'html.parser')
    ratings_tag = soup.find('div', class_='element most_wanted')
    if ratings_tag:
        ratings_tag = ratings_tag.find('div', class_='rating')
    if ratings_tag:
        return ratings_tag.text


def fetch_afisha_page(
        afisha_cinema_url='https://www.afisha.ru/msk/schedule_cinema/'
        ):
    response = requests.get(afisha_cinema_url)
    if not response.ok:
        response.raise_for_status()
    return response.text


def fetch_films_info(film_titles, from_url='https://www.kinopoisk.ru'):
    from_proxy_ips = fetch_proxy_ip_list()
    from_user_agents = make_useragents_list()
    films_with_ratings = Counter()
    for title in film_titles:
        rnd_proxy_url = compose_proxy_url(get_random(from_proxy_ips))
        rnd_header = produce_headers(get_random(from_user_agents))
        response = requests.get(
                    from_url,
                    params={'first': 'no', 'what': '', 'kp_query': title},
                    headers=rnd_header,
                    proxies=rnd_proxy_url,
        )
        if response.ok:
            rating = extract_rating(response.text)
        if rating:
            films_with_ratings[title] = rating
    return films_with_ratings


def find_film_tags(in_soup):
    return in_soup.find_all('div', class_='m-disp-table')


def find_title(in_div):
    return in_div.a.text


def make_useragents_list(from_file='user_agents.txt'):
    with open(from_file, 'r') as file_handler:
        return file_handler.read().splitlines()


def fetch_proxy_ip_list(
                provider='http://www.freeproxy-list.ru/api/proxy'
                ):
    response = requests.get(
                provider,
                params={'anonymity': 'false', 'token': 'demo'}
                )
    if response.ok:
        return response.text.splitlines()


def get_random(from_iterable):
    if from_iterable:
        return random.choice(from_iterable)


def obtain_args():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    return namespace


def produce_headers(user_agent):
    return {
            'User-Agent': user_agent
            }


def is_popular_by(cinemas_num, pop_level):
    return cinemas_num > pop_level


def parse_afisha_list(raw_html, pop_level):
    afisha_soup = BeautifulSoup(raw_html, 'html.parser')
    popular_films = []
    film_tags = find_film_tags(afisha_soup)
    for in_div in film_tags:
        film_title = find_title(in_div)
        cinemas_number = count_cinemas(in_div)
        if is_popular_by(cinemas_number, pop_level):
            popular_films.append(film_title)
    return popular_films


def output_movies_to_console(movies, count):
    print('\n{:<40}    {}\n'.format('Movie', 'Kinopoisk rating'))
    for movie, rating in movies.most_common(count):
        print('{:<40}  | {}'.format(movie, rating))
    print()


if __name__ == '__main__':
    args = obtain_args()
    afisha_page = fetch_afisha_page()
    popular_films = parse_afisha_list(afisha_page, args.pop_level)
    films_kinopoisk_ratings = fetch_films_info(popular_films)
    output_movies_to_console(films_kinopoisk_ratings, args.count)
