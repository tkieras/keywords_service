import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from keywords_service.adapters import orm


@pytest.fixture
def in_memory_db():
	engine = create_engine('sqlite:///:memory:')

	orm.metadata.create_all(engine)

	return engine

@pytest.fixture
def session_factory(in_memory_db):
	orm.start_mappers()
	yield sessionmaker(bind=in_memory_db)
	clear_mappers()


@pytest.fixture
def session(session_factory):
	return session_factory()	



# def wait_for_webapp_to_come_up():
#     deadline = time.time() + 10
#     url = config.get_api_url()
#     while time.time() < deadline:
#         try:
#             return requests.get(url)
#         except ConnectionError:
#             time.sleep(0.5)
#     pytest.fail('API never came up')


# def wait_for_postgres_to_come_up(engine):
#     deadline = time.time() + 10
#     while time.time() < deadline:
#         try:
#             return engine.connect()
#         except OperationalError:
#             time.sleep(0.5)
#     pytest.fail('Postgres never came up')


# @pytest.fixture(scope='session')
# def postgres_db():
#     engine = create_engine(config.get_postgres_uri())
#     wait_for_postgres_to_come_up(engine)
#     metadata.create_all(engine)
#     return engine


# @pytest.fixture
# def postgres_session(postgres_db):
#     start_mappers()
#     yield sessionmaker(bind=postgres_db)()
#     clear_mappers()