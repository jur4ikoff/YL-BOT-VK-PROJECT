from data.users import User
from data import db_session

db_session.global_init("db/Vk_bot.db")
db_sess = db_session.create_session()

for user in db_sess.query(User).all():
    print(user.vk_id)
