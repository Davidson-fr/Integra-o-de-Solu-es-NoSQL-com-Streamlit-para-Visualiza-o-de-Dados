import streamlit as st
from bson.objectid import ObjectId
from datetime import datetime
from db import get_collection, ensure_indexes
from pymongo import ASCENDING
from typing import Optional

st.set_page_config(page_title="E‑Shop Brasil — CRUD MongoDB", page_icon="🛒", layout="wide")

st.title("🛒 E‑Shop Brasil — CRUD com MongoDB")
st.caption("MongoDB + Streamlit + Docker | Dados sintéticos com Faker (1M+)")

with st.sidebar:
    st.header("⚙️ Configurações")
    collection_name = st.text_input("Coleção", value="customers")
    col = get_collection(collection_name)
    ensure_indexes(col)  # garante índices úteis
    st.success(f"Conectado à coleção: {collection_name}")

    st.header("🧭 Operações")
    action = st.radio("Escolha", ["Create", "Read", "Update", "Delete"], index=1)

# Helpers
def _to_objectid(id_str: str) -> Optional[ObjectId]:
    try:
        return ObjectId(id_str)
    except Exception:
        return None

# Create
if action == "Create":
    st.subheader("➕ Criar novo registro")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("Nome")
        email = st.text_input("Email")
        city = st.text_input("Cidade")
        state = st.text_input("Estado (UF)")
        country = st.text_input("País", value="Brasil")
        phone = st.text_input("Telefone")
        is_vip = st.checkbox("VIP?")
        lifetime_value = st.number_input("Lifetime Value (R$)", min_value=0.0, step=10.0)
        submitted = st.form_submit_button("Criar")

    if submitted:
        doc = {
            "name": name,
            "email": email,
            "city": city,
            "state": state,
            "country": country,
            "phone": phone,
            "is_vip": is_vip,
            "lifetime_value": float(lifetime_value),
            "created_at": datetime.utcnow()
        }
        result = col.insert_one(doc)
        st.success(f"Documento criado com _id: {result.inserted_id}")

# Read
elif action == "Read":
    st.subheader("📖 Consultar registros")

    with st.expander("Filtros", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            q_name = st.text_input("Nome contém")
        with c2:
            q_email = st.text_input("Email contém")
        with c3:
            q_city = st.text_input("Cidade contém")
        with c4:
            date_from = st.date_input("Criado a partir de", value=None)
        date_to = st.date_input("Até", value=None)

        query = {}
        if q_name:
            query["name"] = {"$regex": q_name, "$options": "i"}
        if q_email:
            query["email"] = {"$regex": q_email, "$options": "i"}
        if q_city:
            query["city"] = {"$regex": q_city, "$options": "i"}
        if date_from or date_to:
            rng = {}
            if date_from:
                rng["$gte"] = datetime.combine(date_from, datetime.min.time())
            if date_to:
                rng["$lte"] = datetime.combine(date_to, datetime.max.time())
            query["created_at"] = rng

    cpage, climit = st.columns(2)
    with cpage:
        page = st.number_input("Página", min_value=1, value=1, step=1)
    with climit:
        limit = st.selectbox("Limite", options=[10, 25, 50, 100, 200], index=3)

    skip = (page - 1) * limit
    cursor = col.find(query).sort("created_at", ASCENDING).skip(int(skip)).limit(int(limit))
    data = list(cursor)
    count = col.count_documents(query)

    st.write(f"Total: {count} | Página {page}")

    if data:
        # Mostra uma tabela simples
        def _format(doc):
            d = dict(doc)
            d["_id"] = str(d["_id"])
            return d
        st.dataframe([_format(d) for d in data], use_container_width=True)
    else:
        st.info("Nenhum registro encontrado.")

# Update
elif action == "Update":
    st.subheader("✏️ Atualizar registro")
    id_str = st.text_input("Informe o _id do documento")
    if id_str:
        oid = _to_objectid(id_str)
        if oid is None:
            st.error("ObjectId inválido")
        else:
            doc = col.find_one({"_id": oid})
            if not doc:
                st.warning("Documento não encontrado.")
            else:
                with st.form("update_form"):
                    name = st.text_input("Nome", value=doc.get("name",""))
                    email = st.text_input("Email", value=doc.get("email",""))
                    city = st.text_input("Cidade", value=doc.get("city",""))
                    state = st.text_input("Estado (UF)", value=doc.get("state",""))
                    country = st.text_input("País", value=doc.get("country",""))
                    phone = st.text_input("Telefone", value=doc.get("phone",""))
                    is_vip = st.checkbox("VIP?", value=doc.get("is_vip", False))
                    lifetime_value = st.number_input("Lifetime Value (R$)", min_value=0.0, value=float(doc.get("lifetime_value", 0.0)), step=10.0)
                    submitted = st.form_submit_button("Salvar alterações")
                if submitted:
                    updates = {
                        "name": name,
                        "email": email,
                        "city": city,
                        "state": state,
                        "country": country,
                        "phone": phone,
                        "is_vip": is_vip,
                        "lifetime_value": float(lifetime_value),
                    }
                    col.update_one({"_id": oid}, {"$set": updates})
                    st.success("Documento atualizado com sucesso!")

# Delete
elif action == "Delete":
    st.subheader("🗑️ Deletar registro")
    id_str = st.text_input("Informe o _id do documento para deletar")
    if id_str:
        oid = _to_objectid(id_str)
        if oid is None:
            st.error("ObjectId inválido")
        else:
            if st.button("Confirmar exclusão"):
                res = col.delete_one({"_id": oid})
                if res.deleted_count == 1:
                    st.success("Documento deletado com sucesso!")
                else:
                    st.warning("Nenhum documento deletado (verifique o _id).")
