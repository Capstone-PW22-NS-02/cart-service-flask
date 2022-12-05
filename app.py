from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_pymongo import pymongo
import urllib.parse
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)


CONNECTION_STRING = 'mongodb+srv://suryamn:'+urllib.parse.quote_plus("qwerty@1234")+'@capstone.9nomawa.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('test')
cart_collection = pymongo.collection.Collection(db,'cart')
product_collection = pymongo.collection.Collection(db,'products')



@app.route('/getCart/<user_id>', methods=['GET'])
@cross_origin()
def getCart(user_id):

    try:
        userCart = cart_collection.find_one({"user_id":user_id})
        userCartProducts = []
        for i in userCart['products']:
            userCartProducts.append(ObjectId(i))
        print(userCartProducts)
        products = product_collection.find({"_id" : {"$in" : userCartProducts}})
        p = []
        for product in products:
            product['_id'] = str(product['_id'])
            p.append(product)
        print("Products : ", p)
        return jsonify(p)

    except Exception as e: 
        return jsonify({'msg':e})
      

@app.route('/addCart', methods=['POST'])
@cross_origin()
def addCart():

    try:
        cart = request.get_json()
        userCart = cart_collection.find_one({"user_id":ObjectId(cart["user_id"])})

        if userCart:
            cart_collection.update_one({'_id':cart['user_id']}, {"$push": {"products":cart['product_id']}}, upsert=False)

        else:
            newCart = {
                "user_id" : cart['user_id'],
                "products" : [cart['product_id']] 
            }
            cart_collection.insert_one(newCart)
        
        return jsonify({'msg':'Product added'})

    except Exception as e:
        return jsonify({'msg':e})


if __name__ == '__main__':
    app.run(port=8002, debug=True)