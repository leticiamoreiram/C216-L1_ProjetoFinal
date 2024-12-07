DROP TABLE IF EXISTS "vendas";
DROP TABLE IF EXISTS "roupas";

CREATE TABLE "roupas" (
    "id" SERIAL PRIMARY KEY,
    "categoria" VARCHAR(255) NOT NULL, 
    "marca" VARCHAR(255) NOT NULL,
    "tamanho" VARCHAR(10) NOT NULL,    
    "cor" VARCHAR(50) NOT NULL,        
    "quantidade" INTEGER NOT NULL,
    "valor_unitario" FLOAT NOT NULL
);

CREATE TABLE "vendas" (
    "id" SERIAL PRIMARY KEY,
    "roupa_id" INTEGER REFERENCES roupas(id) ON DELETE CASCADE,
    "quantidade_vendida" INTEGER NOT NULL,
    "valor_venda" FLOAT NOT NULL,
    "data_venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "roupas" ("categoria", "marca", "tamanho", "cor", "quantidade", "valor_unitario") 
VALUES ('Camiseta', 'Nike', 'M', 'Preto', 30, 120);

INSERT INTO "roupas" ("categoria", "marca", "tamanho", "cor", "quantidade", "valor_unitario") 
VALUES ('Calça', 'Adidas', 'G', 'Azul', 20, 200);