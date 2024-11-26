# Общие сведения

<b>«library-console-app»</b> представляет из себя пример реализации тестового задания от компании <b>«Effective Mobile»</b>.

## Задание

### Описание

> Необходимо разработать консольное приложение для управления библиотекой книг. Приложение должно позволять добавлять, удалять, искать и отображать книги. Каждая книга должна содержать следующие поля:
> - `id` (уникальный идентификатор, генерируется автоматически)
> - `title` (название книги)
> - `author` (автор книги)
> - `year` (год издания)
> - `status` (статус книги: “в наличии”, “выдана”)

### Требования

> - Добавление книги: Пользователь вводит `title`, `author` и `year`, после чего книга добавляется в библиотеку
> с уникальным `id` и статусом “в наличии”.
> - Удаление книги: Пользователь вводит `id` книги, которую нужно удалить.
> - Поиск книги: Пользователь может искать книги по `title`, `author` или `year`.
> - Отображение всех книг: Приложение выводит список всех книг с их `id`, `title`, `author`, `year` и `status`.
> - Изменение статуса книги: Пользователь вводит `id` книги и новый статус (“в наличии” или “выдана”).

### Дополнительные требования

> - Реализовать хранение данных в текстовом или json формате.
> - Обеспечить корректную обработку ошибок (например, попытка удалить несуществующую книгу).
> - Написать функции для каждой операции (добавление, удаление, поиск, отображение, изменение статуса).
> - Не использовать сторонние библиотеки.

### Критерии оценки

> - Корректность и полнота реализации функционала.
> - Чистота и читаемость кода.
> - Обработка ошибок и исключений.
> - Удобство использования интерфейса командной строки.
> - Структура проекта.

### Будет плюсом

> - Аннотации: Аннотирование функций и переменных в коде. 
> - Документация: Наличие документации к функциям и основным блокам кода. 
> - Описание функционала: Подробное описание функционала приложения в README файле. 
> - Тестирование. 
> - Объектно-ориентированный подход программирования.

## Принцип реализации

В проекте используется архитектурный подход [`DDD`](https://en.wikipedia.org/wiki/Domain-driven_design) и [`EDD`](https://en.wikipedia.org/wiki/Event-driven_programming).
За счет чего данное приложение можно с легкостью интегрировать с [`FastAPI`](https://fastapi.tiangolo.com/), [`Flask`](https://flask.palletsprojects.com/en/stable/), так как логика кода построена на ванильном [`Python 3.12`](https://www.python.org/doc/).

# Зависимости

В проекте используются следующие зависимости: 
- [`poetry`](https://python-poetry.org/)
- [`pytest`](https://docs.pytest.org/en/stable/)
- [`mypy`](https://www.mypy-lang.org/)
- [`ruff`](https://docs.astral.sh/ruff/linter/)
- [`isort`](https://pycqa.github.io/isort/)

> [!IMPORTANT]
> Все зависимости можно найти в [`pyproject.toml`](pyproject.toml)

# Структура проекта

Сама логика приложения находится в `app`. Внутри данной директории есть 5 модулей.

- [`application`](app/application)
- [`domain`](app/domain)
- [`infrastructure`](app/infrastructure)
- [`logic`](app/logic)
- [`settings`](app/settings)

Рассмотрим каждый модуль по отдельности зачем он нужен за что отвечает. 

## Что такое `domain`? 

В основе `DDD` - Домен (Domain). Это модель предмета и его задач, под которые строится приложение. Счет, который оплачиваем, Сообщение, которое отправляем, или Пользователь, которому выставляем оценку. Домены строятся на сущностях из реального мира и ложатся в центр приложения. 

> [!NOTE]
> Например, по заданию у нас библиотека, где нужно оперировать книгами, поэтому `domain` - это книга. 
> Если добавится сервис регистрации, то появится новый `domain` - это человек.

### Что там находится внутри директории `domain`?

Там Вы найдете 2 директории, которые Вас должны заинтересовать `entities` и `values`. 

- [`entities`](https://blog.jannikwempe.com/domain-driven-design-entities-value-objects) - это и есть наши домены, про которые я говорил выше. Пример домена книги можете увидеть [здесь](app/domain/entities/books.py)
- [`values`](https://blog.jannikwempe.com/domain-driven-design-entities-value-objects) - здесь находятся, так называемые, `value objects`. Грубо говоря, это характеристики нашего домена, т.е поля (атрибуты) `domain`. Почему делается так? Все очень просто: для валидации данных. Пример value objects для книги [здесь](https://github.com/C3EQUALZz/library-console-app/blob/master/app/domain/values/books.py)

> [!NOTE]
> Если Вы хотите добавить новый `domain`, то создайте `Python` файл, который описывает его. Например, `peoples.py`. Ваш класс должен наследоваться от [`BaseEntity`](app/domain/entities/base.py). Пример прилагаю ниже: 

```python
@dataclass(eq=False)
class Human:
  """
  Domain which associated with the real human
  """
  nickname: NickName
  email: Email
  is_active: bool
```

> [!NOTE]
> Если Вы хотите добавить новый `value object`, то создайте `Python` файл, который описывает его. Например, `surname.py`. Ваш класс должен наследоваться от [`BaseValueObject`](app/domain/values/base.py). Пример прилагаю ниже:

```python
@dataclass(frozen=True)
class NickName(BaseValueObject[str]):
    """
    Value object which associated with the book name
    """
    value: str

    @override
    def validate(self) -> None:
        if not self.value:
            raise EmptyTextException()

        if len(self.value) > 15:
            raise ValueTooLongException(self.value)

    @override
    def as_generic_type(self) -> str:
        return self.value
```

## Что такое `application`?

Здесь обычно содержится `api` для работы с приложением. Различные [backend endpoints](https://dev.to/apidna/api-endpoints-a-beginners-guide-ief), [sockets](https://ru.wikipedia.org/wiki/%D0%A1%D0%BE%D0%BA%D0%B5%D1%82_(%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D1%8B%D0%B9_%D0%B8%D0%BD%D1%82%D0%B5%D1%80%D1%84%D0%B5%D0%B9%D1%81)) и т.п. 
Каждая директория в `api` - это handlers для сущности (домен), с которой мы работаем.

> [!NOTE]
> Например, по заданию у нас библиотека, где нужно оперировать книгами, поэтому директория называется `books`. 
> Если бы нужно было добавить функционал для работы с пользователем, то в `application/api` появилась бы директория `people`.

### Что за файлы в `application/api/{domain}`?

- `dependencies.py` - здесь находится логика, к которой должны обращаться `handlers`, чтобы выполнить определенные бизнес задачи. Делается с той целью, чтобы было минимальное количество кода в handlers. Пример для книги [`dependencies.py`](app/application/api/books/dependecies.py)
- `handlers.py` - здесь находится та часть, которая выступает "мордой" нашего приложения. В данном случае здесь находятся функции, которые запрашивают данные от пользователя и запускают определенные функции из `dependencies.py`. Например, здесь могут уже находиться ручки `FastAPI`, которые в свою очередь вызывают через [`Depends`](https://fastapi.tiangolo.com/tutorial/dependencies/) определенные функции из `dependencies.py`. Пример для книги [`handlers.py`](app/application/api/books/handlers.py)
- `schemas.py` - здесь находятся схемы валидации данных или просто [`DTO`](https://ru.wikipedia.org/wiki/DTO). В реальных кейсах используются [`pydantic BaseModel`](https://docs.pydantic.dev/latest/api/base_model/) для валидации данных. Пример для книги [`schemas.py`](app/application/api/books/schemas.py)

## Что такое `infrastrucutre`?

На данном слое архитектуры реализована логика работы с данными посредством следующих паттернов:
 
- [`Unit Of Work`](https://qna.habr.com/q/574561)
- [`Repository`](https://www.cosmicpython.com/book/chapter_02_repository.html), 
- [`Service`](https://lyz-code.github.io/blue-book/architecture/service_layer_pattern/)
- [`Message Bus`](https://dev.to/billy_de_cartel/a-beginners-guide-to-understanding-message-bus-architecture-22ec)
- [`Dependecy Injection`](https://thinhdanggroup.github.io/python-dependency-injection/)

### Что там находится внутри директории `infrastrucutre`?

Здесь вы найдете директории и `Python` файлы для описания работ. Каждая директория также называется, как и паттерн, которые я указал выше. Давайте рассмотрим каждый из них по отдельности.  

#### Repository

Здесь реализована логика работы с базой данных на уровне объектов. Репозиторий управляет коллекцией доменов (моделей).
В случае данного тестового задания написана одна имплементация для работы с [книгами относительно JSON](app/infrastructure/repositories/books/jsonr.py).

Как можно написать свой репозиторий? Все очень просто: Вам нужно унаследоваться от интерфейса, который описывает ваш домен.
Пример интерфейса для репозитория управления с книгами можете увидеть [здесь](app/infrastructure/repositories/books/base.py).

Например, я приведу реализацию `SQLAlchemyBookRepository`, где используется библиотека [`SQLAlchemy`](https://www.sqlalchemy.org/).
Создайте [здесь] файл `alchemy.py`, вписав код, который ниже. 

```python
class SQLAlchemyUsersRepository(SQLAlchemyAbstractRepository[Book], BooksRepository):

    def get(self, id: int) -> Optional[Book]:
        result: Result = self._session.execute(select(Book).filter_by(id=id))
        return result.scalar_one_or_none()

    def get_by_title(self, title: str) -> Optional[Book]:
        result: Result = self._session.execute(select(Book).filter_by(title=title))
        return result.scalar_one_or_none()

    def add(self, model: Book) -> Book:
        result: Result = self._session.execute(
            insert(Book).values(**await model.to_dict(exclude={'oid'})).returning(Book)
        )

        return result.scalar_one()
```

#### Unit Of Work

Название паттерна `Unit of Work` намекает на его задачу управлять атомарностью операций. 
В моем случае относительного тестового у меня есть [`JsonAbstractUnitOfWork`](app/infrastructure/uow/books/jsonr.py), который описывает логику работы `Unit Of Work` для сохранения в `json`.

> [!IMPORTANT]
> Автор осведомлен об отсутствии транзакций для сохранения в файлы `json`, `csv`. Такой подход был выбран с той целью, чтобы можно было с легкостью заменить на `SQL` БД в будущем.

Приведу пример того, как написать свой `Unit of Work` для книг, используя [`SQLAlchemy`](https://www.sqlalchemy.org/). Создайте файл в [данной директории](app/infrastructure/uow/books), назвав его, например, `alchemy.py`

```python
class SQLAlchemyAbstractUnitOfWork(AbstractUnitOfWork):
    """
    Unit of work interface for SQLAlchemy, from which should be inherited all other units of work,
    which would be based on SQLAlchemy logics.
    """

    def __init__(self, session_factory: async_sessionmaker = default_session_factory) -> None:
        super().__init__()
        self._session_factory: async_sessionmaker = session_factory

    def __enter__(self) -> Self:
        self._session: AsyncSession = self._session_factory()
        return await super().__aenter__()

    def __exit__(self, *args, **kwargs) -> None:
        super().__exit__(*args, **kwargs)
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.expunge_all()
        self._session.rollback()


class SQLAlchemyBooksUnitOfWork(SQLAlchemyAbstractUnitOfWork, BooksUnitOfWork):

    async def __aenter__(self) -> Self:
        uow = super().__enter__()
        self.books: BooksRepository = SQLAlchemyBooksRepository(session=self._session)
        return uow
```

### Service

Здесь агрегируется логика `UoW` и `Repository`. Именно из-под данного слоя идет работа с данными уже для обращения в командах.
Сервисы всегда пишутся на ванильном Python (как я вижу в примерах), так что здесь имеет смысл писать новый сервис, если добавилась новая сущность в проект.  
Пример сервиса для книг можете увидеть [здесь](app/infrastructure/services). 

Приведу пример того, как написать новый сервис, если появилась сущность (домен) `Human`

```python
class PeopleService:
    """
    Service layer core according to DDD, which using a unit of work, will perform operations on the domain model.
    """

    def __init__(self, uow: PeopleUnitOfWork) -> None:
        self._uow = uow

    def add(self, book: Human) -> Human:
        with self._uow as uow:
            new_human = uow.people.add(model=human)
            uow.commit()
            return new_human

    def check_existence(self, oid: Optional[str] = None, email: Optional[str] = None) -> bool:
        if not (oid or email):
            return False

        with self._uow as uow:
            if oid and uow.people.get(oid):
                return True

            if title and uow.books.get_by_email(email):
                return True

        return False
```

## Что такое `logic`?

Здесь на данном слое собрана вся бизнес логика, где требуется реализовать наш функционал по тз. 
В `logic` у нас есть `commands` и `events`. 



