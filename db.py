"module to use or create databases for your cascada project"

from sqllex.types import DBTemplateType  # type: ignore
from sqllex import SQLite3x  # type: ignore

from src.config import CascadaWebsiteConfig, get_config
from src.util import getobjfrmfile

# load the configuration
config: CascadaWebsiteConfig = get_config()

# loading the default database

## loading the database schema
db_schema: DBTemplateType = getobjfrmfile(str(config.dbschema), "content")
## connecting to the database


def makedb(name: str, schema: DBTemplateType):
    "create a database and return a connection"
    return SQLite3x(str(config.database / f"{name}.db"), schema)


content = makedb("content", db_schema)
"the default database"
