import redis
from datetime import datetime

# Підключення до Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def create_session(user_id, session_token):
    """Створити нову сесію для користувача."""
    session_data = {
        'session_token': session_token,
        'login_time': datetime.now().isoformat()
    }
    r.hset(f"user_session:{user_id}", mapping=session_data)
    r.expire(f"user_session:{user_id}", 1800)
    print(f"Сесія для користувача {user_id} створена.")

def get_session(user_id):
    """Отримати активну сесію для користувача."""
    session_data = r.hgetall(f"user_session:{user_id}")
    if session_data:
        session_data = {key.decode(): value.decode() for key, value in session_data.items()}
        print(f"Активна сесія для користувача {user_id}: {session_data}")
        return session_data
    else:
        print(f"Сесія для користувача {user_id} не знайдена.")
        return None

def update_session_activity(user_id):
    """Оновити час останньої активності користувача."""
    if r.exists(f"user_session:{user_id}"):
        r.hset(f"user_session:{user_id}", 'last_activity', datetime.now().isoformat())
        r.expire(f"user_session:{user_id}", 1800)
        print(f"Час активності для користувача {user_id} оновлено.")
    else:
        print(f"Неможливо оновити час активності: сесія для користувача {user_id} не існує.")

def delete_session(user_id):
    """Видалити сесію для користувача."""
    r.delete(f"user_session:{user_id}")
    print(f"Сесія для користувача {user_id} видалена.")

# Приклади використання
create_session("user123", "token_abc123")
get_session("user123")
update_session_activity("user123")
delete_session("user123")