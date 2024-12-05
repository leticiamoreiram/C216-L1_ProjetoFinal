from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

# Função para obter a conexão com o banco de dados PostgreSQL
async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/roupas")
    return await asyncpg.connect(DATABASE_URL)

# Inicializar a aplicação FastAPI
app = FastAPI()

# Modelos para itens e vendas
class Roupa(BaseModel):
    id: Optional[int] = None
    categoria: str  # Ex.: camisetas, calças
    marca: str
    tamanho: str  # Ex.: P, M, G, GG
    cor: str
    quantidade: int
    valor_unitario: float

class RoupaBase(BaseModel):
    categoria: str
    marca: str
    tamanho: str
    cor: str
    quantidade: int
    valor_unitario: float

class VendaRoupa(BaseModel):
    quantidade: int

class AtualizarRoupa(BaseModel):
    categoria: Optional[str] = None
    marca: Optional[str] = None
    tamanho: Optional[str] = None
    quantidade: Optional[int] = None
    valor_unitario: Optional[float] = None

# Middleware para logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

# 1. Adicionar um novo item
@app.post("/api/v1/roupas/", status_code=201)
async def adicionar_roupa(roupa: RoupaBase):
    conn = await get_database()
    try:
        query = """
            INSERT INTO roupas (categoria, marca, tamanho, cor, quantidade, valor_unitario)
            VALUES ($1, $2, $3, $4, $5, $6)
        """
        async with conn.transaction():
            # Aqui você está passando 6 valores, que são os parâmetros de acordo com a ordem das colunas
            await conn.execute(query, roupa.categoria, roupa.marca, roupa.tamanho, roupa.cor, roupa.quantidade, roupa.valor_unitario)
            return {"message": "Roupa adicionada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar a roupa: {str(e)}")
    finally:
        await conn.close()

# 2. Listar todas as roupas
@app.get("/api/v1/roupas/", response_model=List[Roupa])
async def listar_roupas():
    conn = await get_database()
    try:
        query = "SELECT * FROM roupas"
        rows = await conn.fetch(query)
        roupas = [dict(row) for row in rows]
        return roupas
    finally:
        await conn.close()

# 3. Buscar roupa por ID
@app.get("/api/v1/roupas/{roupa_id}")
async def listar_roupa_por_id(roupa_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM roupas WHERE id = $1"
        roupa = await conn.fetchrow(query, roupa_id)
        if roupa is None:
            raise HTTPException(status_code=404, detail="Roupa não encontrada.")
        return dict(roupa)
    finally:
        await conn.close()

# 4. Vender uma roupa
@app.put("/api/v1/roupas/{roupa_id}/vender/")
async def vender_roupa(roupa_id: int, venda: VendaRoupa):
    conn = await get_database()
    try:
        query = "SELECT * FROM roupas WHERE id = $1"
        roupa = await conn.fetchrow(query, roupa_id)
        if roupa is None:
            raise HTTPException(status_code=404, detail="Roupa não encontrada.")

        if roupa['quantidade'] < venda.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")
        
        nova_quantidade = roupa['quantidade'] - venda.quantidade
        update_query = "UPDATE roupas SET quantidade = $1 WHERE id = $2"
        await conn.execute(update_query, nova_quantidade, roupa_id)

        valor_venda = roupa['valor_unitario'] * venda.quantidade
        insert_venda_query = """
            INSERT INTO vendas (roupa_id, quantidade_vendida, valor_venda) 
            VALUES ($1, $2, $3)
        """
        await conn.execute(insert_venda_query, roupa_id, venda.quantidade, valor_venda)

        roupa_atualizada = dict(roupa)
        roupa_atualizada['quantidade'] = nova_quantidade

        return {"message": "Venda realizada com sucesso!", "roupa": roupa_atualizada}
    finally:
        await conn.close()

# 5. Atualizar atributos de uma roupa pelo ID
@app.patch("/api/v1/roupas/{roupa_id}")
async def atualizar_roupa(roupa_id: int, roupa_atualizacao: AtualizarRoupa):
    conn = await get_database()
    try:
        query = "SELECT * FROM roupas WHERE id = $1"
        roupa = await conn.fetchrow(query, roupa_id)
        if roupa is None:
            raise HTTPException(status_code=404, detail="Roupa não encontrada.")

        update_query = """
            UPDATE roupas
            SET categoria = COALESCE($1, categoria),
                marca = COALESCE($2, marca),
                tamanho = COALESCE($3, tamanho),
                quantidade = COALESCE($4, quantidade),
                valor_unitario = COALESCE($5, valor_unitario)
            WHERE id = $6
        """
        await conn.execute(
            update_query,
            roupa_atualizacao.categoria,
            roupa_atualizacao.marca,
            roupa_atualizacao.tamanho,
            roupa_atualizacao.quantidade,
            roupa_atualizacao.valor_unitario,
            roupa_id
        )
        return {"message": "Roupa atualizada com sucesso!"}
    finally:
        await conn.close()

# 6. Remover uma roupa pelo ID
@app.delete("/api/v1/roupas/{roupa_id}")
async def remover_roupa(roupa_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM roupas WHERE id = $1"
        roupa = await conn.fetchrow(query, roupa_id)
        if roupa is None:
            raise HTTPException(status_code=404, detail="Roupa não encontrada.")
        
        delete_query = "DELETE FROM roupas WHERE id = $1"
        await conn.execute(delete_query, roupa_id)
        return {"message": "Roupa removida com sucesso!"}
    finally:
        await conn.close()

# 7. Resetar banco de dados de roupas
@app.delete("/api/v1/roupas/")
async def resetar_roupas():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Estoque de roupas resetado com sucesso!"}
    finally:
        await conn.close()

# 8. Listar vendas
@app.get("/api/v1/vendas/")
async def listar_vendas():
    conn = await get_database()
    try:
        query = """
            SELECT vendas.id, roupas.categoria, roupas.marca, roupas.tamanho, vendas.quantidade_vendida, vendas.valor_venda, vendas.data_venda
            FROM vendas
            JOIN roupas ON vendas.roupa_id = roupas.id
        """
        rows = await conn.fetch(query)
        vendas = [dict(row) for row in rows]
        return vendas
    finally:
        await conn.close()
