from flask import Flask, request, jsonify, Response, make_response
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS

class Produto():
    def __init__(self, name, price, image):
        self.atributos = {
            'product_name': name,
            'product_price': price,
            'product_image': image
        }

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Freshmania:TIxrootoor10@cluster0.uf14a.mongodb.net/mydb?retryWrites=true&w=majority"

mongo = PyMongo()
mongo.init_app(app)

CORS(app)

@app.route("/", methods=["GET"])
def index():
    return('Hello World');

#rota para adicionar novos produtos ao banco de dados
@app.route("/add_product", methods=["POST"])
def add_produto():
    #referenciando a coleção produtos
    products = mongo.db.produtos

    #verificando se os parâmetros foram corretamente passados
    if 'product_name' in request.form and 'product_price' in request.form and 'product_image' in request.form:
        try:
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            product_image = request.form.get('product_image')

            #instânciando a classe Produto
            produto = Produto(product_name, product_price, product_image)
            insertResult = products.insert_one(produto.atributos)
            response = make_response('Ok', 200)

        #tratamento de exceção
        except Exception as e:
            print(repr(e))
            response = make_response('Erro interno do Servidor', 500)
    else:
        response = make_response('Preencha todos os campos do formulário', 400)
    return(response);

#rota para editar produtos no banco de dado
@app.route("/edit_product/<oid>", methods=["POST"])
def edit_product(oid):
    print('oid', oid)
    #referenciando a coleção produtos
    products = mongo.db.produtos

    #verificando se os parâmetros foram corretamente passados
    if 'product_name' in request.form and 'product_price' in request.form and 'product_image' in request.form:
        try:
            product_name = request.form.get('product_name')
            product_price = request.form.get('product_price')
            product_image = request.form.get('product_image')

            produto = Produto(product_name, product_price, product_image)

            filter = { '_id': ObjectId(oid) }
            newvalues = { "$set": produto.atributos }
            products.update_one(filter, newvalues)
            response = make_response('Ok', 200)

        #tratamento de exceção
        except Exception as e:
            print('something went wrong')
            print(repr(e))
            response = make_response('Erro interno do Servidor', 500)
    else:
        response = make_response('Preencha todos os campos do formulário', 400)

    return(response);

#rota para deletar produtos no banco de dado
@app.route("/delete_product/<oid>", methods=["POST"])
def delete_product(oid):
    print('oid', oid)
    products = mongo.db.produtos

    try:
        products.delete_many({'_id': ObjectId(oid)})
        response = make_response('Ok', 200)

    except Exception as e:
        print('something went wrong')
        print(repr(e))
        response = make_response('Erro interno do Servidor', 500)

    return(response);

#rota para carregar os produtos armazenados no banco de dado
@app.route("/get_products", methods=["GET"])
def get_products():
    products = mongo.db.produtos
    saved_products = []
    try:
        if not (products is None):
            for product in products.find():
                saved_products.append({
                    '_id': str(ObjectId(product['_id'])),
                    'product_name': product['product_name'],
                    'product_price': product['product_price'],
                    'product_image': product['product_image']
                })

        response = make_response(jsonify(saved_products), 200)
        response.headers["Content-Type"] = "application/json"

    except Exception as e:
        print('something went wrong')
        print(repr(e))
        response = make_response('Erro interno do Servidor', 500)


    return(response);

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
