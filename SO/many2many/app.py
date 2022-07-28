from fastapi import Depends, FastAPI
from sqlalchemy import Column, ForeignKey, Integer, create_engine, String, Integer, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
 
SQLALCHEMY_DATABASE_URL = "sqlite:///sql_app.db"
 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
children_parents = Table("children_parents", Base.metadata,
    Column("child_id", ForeignKey("children.id"), primary_key=True),
    Column("parent_id", ForeignKey("parents.id"), primary_key=True)
)
 
 
class Parent(Base):
    __tablename__ = "parents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    children = relationship("Child", secondary=children_parents, backref="parents")
 
class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
 
 
app = FastAPI()
 
Base.metadata.create_all(bind=engine)

 
@app.get("/")
async def root(db: SessionLocal = Depends(get_db)):
    child_1 = db.query(Child).filter(Child.id==1).first()
    if not child_1:
        child_1 = Child(id=1, name="Child name")

    parent = Parent(name="Parent name", children=[
        child_1])
 
    db.add(parent)
    db.commit()
    db.refresh(parent)
    return parent

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)