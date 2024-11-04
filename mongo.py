from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://Paha123:9532@cluster1.hv0kp.mongodb.net/?retryWrites=true&w=majority&appName=DB_LMS")
db = cluster["DB_LMS"]

collections = db["Collection_1"]
collections_orders = db["orders"]


# Додавання продуктів
collections.insert_many([
    { "name": "Ноутбук", "price": 1200, "category": "Електроніка", "stock": 50 },
    { "name": "Смартфон", "price": 800, "category": "Електроніка", "stock": 100 },
    { "name": "Стіл", "price": 200, "category": "Меблі", "stock": 20 }
])

# Додавання замовлень
collections_orders.insert_many([
    { "orderNumber": 1, "client": "paha", "products": [{ "productId": "...", "quantity": 1 }], "totalAmount": 1200, "date": "2024-11-01" },
    { "orderNumber": 2, "client": "Джейн Сміт", "products": [{ "productId": "...", "quantity": 2 }], "totalAmount": 1600, "date": "2024-11-01" }
])

# Витягнення всіх замовлень за останні 30 днів
from datetime import datetime, timedelta

thirty_days_ago = datetime.now() - timedelta(days=30)
recent_orders = collections_orders.find({ "date": { "$gte": thirty_days_ago } })

# Оновлення кількості продукту на складі
collections.update_one(
    { "name": "Ноутбук" },
    { "$inc": { "stock": -1 } }
)

# Видалення продуктів, які більше не доступні для продажу
collections.delete_many({ "stock": 0 })

# Агрегація: підрахунок загальної кількості проданих продуктів
pipeline = [
    { "$unwind": "$products" },
    { "$group": { "_id": "$products.productId", "totalSold": { "$sum": "$products.quantity" } } }
]
total_sold_products = collections_orders.aggregate(pipeline)

# Агрегація: підрахунок загальної суми всіх замовлень клієнта
pipeline_spent = [
    { "$match": { "client": "Джон Доу" } },
    { "$group": { "_id": None, "totalSpent": { "$sum": "$totalAmount" } } }
]
total_spent_john_doe = collections_orders.aggregate(pipeline_spent)

# Додавання індексу для поля category в колекції Collection_1
collections.create_index([("category", 1)])