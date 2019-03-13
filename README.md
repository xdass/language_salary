# Programming vacancies compare

This project created to collect and analize programmers salary using HeadHunter and SuperJob API

### How to install

1. You need to create app on https://api.superjob.ru.
2. Create .env file and add:
    * login=superjob_login
    * password=superjob_password
    * client_id=your_client_id (you can get it on https://api.superjob.ru/info/)
    * client_secret=your_client_secret (you can get it on https://api.superjob.ru/info/)

3. Install dependencies (written below)

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Program output example
```
+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Java Script           | 40               | 19                  | 88263            |
| Python                | 11               | 8                   | 88625            |
| JAVA                  | 22               | 8                   | 129500           |
| C++                   | 27               | 13                  | 87038            |
| C                     | 10               | 5                   | 105000           |
| PHP                   | 64               | 30                  | 82620            |
| Go                    | 3                | 2                   | 114500           |
+-----------------------+------------------+---------------------+------------------+
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Java Script           | 2000             | 786                 | 132649           |
| Python                | 1364             | 374                 | 146946           |
| JAVA                  | 1761             | 484                 | 159306           |
| C++                   | 172              | 77                  | 127305           |
| C                     | 326              | 175                 | 120992           |
| PHP                   | 1138             | 564                 | 118352           |
| Go                    | 365              | 102                 | 172607           |
+-----------------------+------------------+---------------------+------------------+
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).