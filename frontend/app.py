from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import requests
import os
import csv

app = Flask(__name__)

# Definindo a URL base da API
API_BASE_URL = "http://backend:8000"

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para exibir o formulário de cadastro de roupa
@app.route('/cadastro', methods=['GET'])
def inserir_roupa_form():
    return render_template('cadastro.html')

# Rota para enviar os dados do formulário de cadastro para a API
@app.route('/inserir', methods=['POST'])
def inserir_roupa():
    categoria = request.form['categoria']
    marca = request.form['marca']
    tamanho = request.form['tamanho']
    cor = request.form['cor']
    quantidade = request.form['quantidade']
    valor_unitario = request.form['valor_unitario']

    payload = {
        'categoria': categoria,
        'marca': marca,
        'tamanho': tamanho,
        'cor': cor,
        'quantidade': int(quantidade),
        'valor_unitario': float(valor_unitario)
    }

    response = requests.post(f'{API_BASE_URL}/api/v1/roupas/', json=payload)

    if response.status_code == 201:
        return redirect(url_for('listar_roupas'))
    else:
        return "Erro ao inserir roupa", 500

# Rota para listar todas as roupas
@app.route('/estoque', methods=['GET'])
def listar_roupas():
    response = requests.get(f'{API_BASE_URL}/api/v1/roupas/')
    try:
        roupas = response.json()
    except:
        roupas = []
    return render_template('estoque.html', roupas=roupas)

# Rota para exibir o formulário de edição de roupa
@app.route('/atualizar/<int:roupa_id>', methods=['GET'])
def atualizar_roupa_form(roupa_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/roupas/{roupa_id}")
    if response.status_code == 404:
        return "Roupa não encontrada", 404
    roupa = response.json()
    return render_template('atualizar.html', roupa=roupa)

# Rota para enviar os dados do formulário de edição de roupa para a API
@app.route('/atualizar/<int:roupa_id>', methods=['POST'])
def atualizar_roupa(roupa_id):
    categoria = request.form['categoria']
    marca = request.form['marca']
    tamanho = request.form['tamanho']
    cor = request.form['cor']
    quantidade = request.form['quantidade']
    valor_unitario = request.form['valor_unitario']

    payload = {
        'categoria': categoria,
        'marca': marca,
        'tamanho': tamanho,
        'cor': cor,
        'quantidade': int(quantidade),
        'valor_unitario': float(valor_unitario)
    }

    response = requests.patch(f"{API_BASE_URL}/api/v1/roupas/{roupa_id}", json=payload)

    if response.status_code == 200:
        return redirect(url_for('listar_roupas'))
    else:
        return "Erro ao atualizar roupa", 500

# Rota para exibir o formulário de venda de roupa
@app.route('/vender/<int:roupa_id>', methods=['GET'])
def vender_roupa_form(roupa_id):
    response = requests.get(f"{API_BASE_URL}/api/v1/roupas/{roupa_id}")
    if response.status_code == 404:
        return "Roupa não encontrada", 404
    roupa = response.json()
    return render_template('vender.html', roupa=roupa)

# Rota para vender uma roupa
@app.route('/vender/<int:roupa_id>', methods=['POST'])
def vender_roupa(roupa_id):
    quantidade = request.form['quantidade']

    payload = {
        'quantidade': int(quantidade)
    }

    response = requests.put(f"{API_BASE_URL}/api/v1/roupas/{roupa_id}/vender/", json=payload)

    if response.status_code == 200:
        return redirect(url_for('listar_roupas'))
    else:
        return "Erro ao vender roupa", 500

# Rota para listar todas as vendas
@app.route('/vendas', methods=['GET'])
def listar_vendas():
    response = requests.get(f"{API_BASE_URL}/api/v1/vendas/")
    try:
        vendas = response.json()
    except:
        vendas = []

    total_vendas = sum(float(venda['valor_venda']) for venda in vendas)
    return render_template('vendas.html', vendas=vendas, total_vendas=total_vendas)

# Rota para excluir uma roupa
@app.route('/excluir/<int:roupa_id>', methods=['POST'])
def excluir_roupa(roupa_id):
    response = requests.delete(f"{API_BASE_URL}/api/v1/roupas/{roupa_id}")

    if response.status_code == 200:
        return redirect(url_for('listar_roupas'))
    else:
        return "Erro ao excluir roupa", 500

# Rota para resetar o banco de dados
@app.route('/reset-database', methods=['GET'])
def resetar_database():
    response = requests.delete(f"{API_BASE_URL}/api/v1/roupas/")

    if response.status_code == 200:
        return render_template('reset-database.html')
    else:
        return "Erro ao resetar o banco de dados", 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
