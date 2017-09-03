# Cinemas

Sometimes you want to know the coolest films that are going on at the moment, but when you go to the [afisha](https://www.afisha.ru/msk/schedule_cinema/) it is difficult to determine which of them has a higher rating at [kinopoisk](https://www.kinopoisk.ru)

The script displays to the console the most popular films currently being watched, sorted by rating.


## Quickstart

Example of script launch on Linux, Python 3.5:

```
$ pip install -r requirements.txt # alternatively try pip3

$ python3 cinemas.py -h
usage: cinemas.py [-h] [-p POP_LEVEL] [-c COUNT]

optional arguments:
  -h, --help            show this help message and exit
  -p POP_LEVEL, --pop_level POP_LEVEL
                        min number of cinemas where film is on
  -c COUNT, --count COUNT
                        number of top rated movies

$ python3 cinemas.py 

Movie                                       Kinopoisk rating

Твое имя                                  | 8.3
Терминатор-2: Судный день                 | 8.3
Квест                                     | 7.7
Малыш на драйве                           | 7.6
Мистер Штайн идет в онлайн                | 7.5
Телохранитель киллера                     | 7.0
Про любовь. Только для взрослых           | 6.9
Валериан и город тысячи планет            | 6.8
Тайна 7 сестер                            | 6.6
Тюльпанная лихорадка                      | 6.5

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
