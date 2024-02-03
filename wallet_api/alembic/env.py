from environs import Env
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

env = Env()
env.read_env()

DJANGO_DEFAULT_MODELS = (
    # 'django_content_type',
    # 'auth_group',
    # 'auth_user',
    # 'auth_user_groups',
    # 'django_session',
    # 'auth_permission',
    # 'auth_user_user_permissions',
    # 'account_userprofile',
    # 'south_migrationhistory',
    # 'django_site',
)

USER = env('MYSQL_USER')
PASSWORD = env('MYSQL_PASSWORD')
HOST = env('MYSQL_HOST')
PORT = env('MYSQL_PORT')
DB_NAME = env('MYSQL_DATABASE')
DB_URL = f'mysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'


def include_object(object, name, type_, reflected, compare_to) -> bool:
    """Filter object to be considered in the autogenerate sweep."""
    if type_ == 'table' and name in DJANGO_DEFAULT_MODELS:
        return False
    return True

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option('sqlalchemy.url', DB_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
