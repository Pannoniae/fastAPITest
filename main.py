from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlmodel import Session, select


from model import User, Role

app = FastAPI()

db_name = "users.db"
sqlite_conn_string = f"sqlite:///{db_name}"

engine = create_engine(sqlite_conn_string)

def get_session():
    with Session(engine) as session:
        yield session

@app.get("/users", response_model=list[User])
def list_users(session=Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
def create_user(user: User, session=Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: User, session=Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}