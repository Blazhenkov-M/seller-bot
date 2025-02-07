from settings.config import settings
from app.database.models import Base

# print(settings.bot_token)
# print(settings.db_host)
# print(settings.db_port)
# print(settings.db_user)
# print(settings.db_pass)
# print(settings.db_name)
#
print(settings.sqlalchemy_database_url)
#
# print(Base.metadata.tables)

print(settings)
