from sqlalchemy.orm import declarative_base

Base = declarative_base()

import app.models

print(Base.metadata.tables.keys())
