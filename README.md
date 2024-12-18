# Projeto: Sistema de Estoque de Loja de Roupas

## Informações do Integrante
- **Nome:** Letícia Moreira Mendes
- **Matrícula:** 1705
- **Email:** leticia.m@gec.inatel.br

---

## Introdução ao Projeto
Este projeto é um sistema de estoque para uma loja de roupas, desenvolvido com base nos aprendizados do lab **C216-L1**. O sistema permite realizar o gerenciamento completo do estoque por meio de um conjunto de rotas CRUD, bem como funcionalidades adicionais como venda de produtos e reset do banco de dados.

### Objetivo
O objetivo do sistema é facilitar o controle de estoque e vendas da loja, permitindo que os itens sejam cadastrados, editados, vendidos e excluídos de forma eficiente. Ele também possibilita listar as roupas em estoque e as vendas realizadas.

---

## Funcionalidades
Abaixo estão listadas as rotas disponíveis e suas funcionalidades:

1. **Página Inicial:**
   - **Descrição:** Exibe a página inicial do sistema.

2. **Cadastro de Roupas:**
   - **Descrição:** Exibe o formulário para cadastrar uma nova roupa. Recebe os dados do formulário e envia para a API, inserindo a roupa no sistema.

3. **Listar Roupas:**
   - **Descrição:** Lista todas as roupas disponíveis no estoque.

4. **Atualizar Roupas:**
   - **Descrição:** Exibe o formulário para editar os dados de uma roupa. Recebe os dados editados e envia para a API, atualizando a roupa no sistema.

5. **Vender Roupas:**
   - **Descrição:** Exibe o formulário para realizar a venda de uma roupa. Envia os dados da venda para a API e atualiza o estoque.

6. **Listar Vendas:**
   - **Descrição:** Lista todas as vendas realizadas, incluindo o total arrecadado.

7. **Excluir Roupas:**
   - **Descrição:** Exclui uma roupa específica do sistema.

8. **Resetar Banco de Dados:**
   - **Descrição:** Reseta o banco de dados, removendo todas as roupas cadastradas.

---

## Como Rodar o Projeto
Siga as etapas abaixo para rodar o projeto:

1. Clone o repositório:
   ```bash
   git clone https://github.com/leticiamoreiram/C216-L1_ProjetoFinal.git
   cd C216-L1_ProjetoFinal
   ```

2. Execute o projeto utilizando o Docker:
   ```bash
   docker-compose up --build
   ```

3. Acesse o sistema no navegador:
   ```
   http://localhost:3000
   ```

---


