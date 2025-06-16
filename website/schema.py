# type: ignore

from sqllex.constants import TEXT, DATE
from sqllex.types import DBTemplateType

content: DBTemplateType = {
    "posts": {
        "title": TEXT,
        "content": TEXT,
        "author": TEXT,
        "date": DATE,
        "tags": TEXT,
    },
}
