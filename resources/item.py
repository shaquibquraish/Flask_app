from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank!")
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        # item = ItemModel(name, **data) same as line below

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:

            return {'msg': 'An error occurred while inserting item'}, 500

        return item.json(), 201

    def delete(self, name):

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        try:
            item.save_to_db()
        except:
            return {'msg': 'An error occurred while updating item'}, 500

        return item.json()


class Items(Resource):
    def get(self):
        # result = ItemModel.query.all()

        # items = []

        # for item in result:
        #     items.append(item.json())

        # return {'items': items}
        return {'items': [item.json() for item in ItemModel.query.all()]}
