import argparse
from faker import Faker
from datetime import datetime, timedelta
from db import get_collection, ensure_indexes
from pymongo import InsertOne

def generate_docs(fake: Faker, n: int):
    # Gera documentos de clientes com campos variados
    base_date = datetime.now()
    for i in range(n):
        # Para distribuir datas ao longo dos últimos ~3 anos
        created_at = base_date - timedelta(days=fake.random_int(min=0, max=365*3))
        yield {
            "name": fake.name(),
            "email": fake.unique.email(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "country": fake.current_country(),
            "phone": fake.phone_number(),
            "created_at": created_at,
            "is_vip": fake.boolean(chance_of_getting_true=10),
            "lifetime_value": round(fake.pyfloat(left_digits=5, right_digits=2, positive=True), 2)
        }

def bulk_insert(n: int, batch_size: int, collection_name: str):
    fake = Faker("pt_BR")
    col = get_collection(collection_name)

    # Inserção em lotes
    to_insert = []
    total = 0

    # Melhor performance definindo unique só após seed massivo; aqui usamos email unique=False
    for doc in generate_docs(fake, n):
        to_insert.append(InsertOne(doc))
        if len(to_insert) >= batch_size:
            col.bulk_write(to_insert, ordered=False)
            total += len(to_insert)
            print(f"Inserted {total}/{n}")
            to_insert = []

    if to_insert:
        col.bulk_write(to_insert, ordered=False)
        total += len(to_insert)
        print(f"Inserted {total}/{n}")

    # Cria índices ao final (evita custo durante carga massiva)
    ensure_indexes(col)
    print("Indexes ensured: email, city, created_at")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MongoDB with massive fake data")
    parser.add_argument("--n", type=int, default=1_000_000, help="Total documents to insert")
    parser.add_argument("--batch", type=int, default=50_000, help="Batch size for bulk insert")
    parser.add_argument("--collection", type=str, default="customers", help="Collection name")
    args = parser.parse_args()

    bulk_insert(args.n, args.batch, args.collection)
