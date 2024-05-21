from model import User, Role
from main import engine

User.metadata.create_all(engine)
Role.metadata.create_all(engine)