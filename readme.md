# Лохматова Алиса - "Cryptogramm"


### Группа: 10 - И - 3
### Электронная почта: aalokhmatova@edu.hse.ru
### Tg: jiguli_san


[ НАЗВАНИЕ ПРОЕКТА ]

“Cryptogramm - мессенджер с шифрованием”

[ ПРОБЛЕМНОЕ ПОЛЕ ]

На данный момент пользователям доступно множество разнообразных мессенджеров с разными фишками. но, к сожалению такие сервисы не могут гарантировать конфиденциальность данных, т.к. никому не известно что на самом деле происходит на серверах. мой мессенджер шифрует все сообщения на стороне клиента, полностью независимо от сервера, и по итогу на нём оказываются только зашифрованные сообщения, за счет чего человек может не беспокоиться о своей конфиденциальность.

[ ЗАКАЗЧИК / ПОТЕНЦИАЛЬНАЯ АУДИТОРИЯ ]

* Люди, которым важна анонимность, приватность и конфиденциальность
* Люди, заинтересованные в надежном хранении личных файлов

[ АППАРАТНЫЕ / ПРОГРАММНЫЕ ТРЕБОВАНИЯ ] 

1. Доступ к интернету
2. Операционная система Windows 8+

[ ФУНКЦИОНАЛЬНЫЕ ТРЕБОВАНИЯ ]

Программный продукт будет предоставлять следующие возможности:
1. Регистрация/вход в аккаунт;
2. Создание чатов и возможность отправлять сообщения (с шифрованием);
3. Экспорт сообщений;
4. Возможность включить spam tracker bot в чате;
5. Алгоритм рекомендации друзей для знакомств на основе кластеризации;
6. Возможность сохранять фото/видео/музыку на сервере и потом его просматривать;
7. Суммаризация содержания непрочитанных сообщений;
8. Автоответы на сообщения при длительном отсутствии в сети;
9. Кастомизация интерфейса.


[ ПОХОЖИЕ / АНАЛОГИЧНЫЕ ПРОДУКТЫ ]

Анализ 3 продуктов, которые максимально приближены к заданному функционалу, показал, что:

* Whatsapp - частые утечки данных
* Discord - проблематично находить других людей, нет алгоритмов рекомендации собеседников
* Telegram - не известно, что сервер делает с информацией и сообщениями

[ ИНСТРУМЕНТЫ РАЗРАБОТКИ, ИНФОРМАЦИЯ О БД ]

1. PyCharm/VS Code
2. Git/Github
3. FastAPI
4. Dear PyGui
5. Шифрование ассимитричное RSA
6. PostgreSQL
7. Alembic

[ ЭТАПЫ РАЗРАБОТКИ ]

1. Планирование - разработка архитектуры клиента, сервера, БД, передаваемых сообщений и т.д. -- до 15 февраля 
2. Создание контейнеров базы данных и настройка репликации для обеспечения отказоустойчивости. -- до 15 марта
3. Создание сервера, API для клиента и его реализация - приём и выполнение запросов от клиента (передача сообщения, сохранение данных и т.п.) -- до 15 апреля 
4. Разработка алгоритма рекомендации (работает на стороне сервера). -- до 10 мая
5. Создание GUI клиента и добавление возможности его кастомизации. -- до 25 мая
6. Добавление в клиент возможности входа/регистрации. -- до 10 июня
7. Добавление в клиент возможности создания чатов (включая обмен секретными ключами между собеседниками). -- до 25 июля
8. Добавление в клиент возможности отправки сообщений (включая шифрование сообщений). --  до 10 августа
9. Добавление в клиент возможности экспорта сообщений. -- до 20 августа 
10. Добавление в клиент возможности загрузки и просмотра фото/видео/музыки. -- до 10 сентября 
11. Разработка spam tracker bot и включение его в клиент. -- до 5 октября
12. Разработка суммаризации непрочитанных сообщений. -- до 1 ноября
13. Разработка автоответчика на непрочитанные сообщения -- до 30 ноября

[ ВОЗМОЖНЫЕ РИСКИ ]

- База данных не справится с нагрузкой - больше контейнеров в Docker и горизонтальное масштабирование
- На данный может оказаться мало знаний в области ML - курсы/статьи различного авторства (Т-Образование, Stepik, Яндекс образование, Яндекс Хендбуки, etc)