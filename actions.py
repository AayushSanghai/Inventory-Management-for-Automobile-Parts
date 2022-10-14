from flask import Flask
from flask import render_template
from bson import ObjectId
from bson.timestamp import Timestamp
import datetime as dt

from helpers import *

def order(db, iid):
    info = db.items.find_one({'_id': ObjectId(str(iid))})

    bins = db.bins.find({'$or': [{'qty': 0}, {'item_id': None}]})
    
    return render_template('order.html', item_data=info, bins=bins, order_count=count_new_orders(db))

def fill(db, bid):

    info = db.items.find_one({'_id': ObjectId(str(bid))})

    bins = db.bins.find({'$or':[ {"qty":0}, {"item_id":None}]})
    
    return render_template('fillbin.html', item_data=info, bins=bins, order_count=count_new_orders(db))
    
def reorder(db, bid):

    info = db.bins.find_one({'_id': ObjectId(str(bid))})
    item = db.items.find_one({'_id': info['item_id']})


    return render_template('reorder.html', bin_data=info, item=item, max=int(info['max_qty']) - int(info['qty']), order_count=count_new_orders(db))

def use(db, bid):
    info = db.bins.find_one({'_id': ObjectId(str(bid))})
    item = db.items.find_one({'_id': info['item_id']})

    return render_template('dispense.html', bin_data=info, item=item)

def add(db, iid):
    types = db.types.find()
    subs = db.subtypes.find()
    sup = db.suppliers.find()
    
    return render_template('add.html', types=types, subtypes=subs, suppliers=sup, order_count=count_new_orders(db))
    
def modify(db, bid):
    info = db.bins.find_one({'_id': ObjectId(str(bid))})
    item = db.items.find_one({'_id': info['item_id']})

    return render_template('modify.html', bin_data=info, item=item, order_count=count_new_orders(db))

def dispatch(db, bid):
    order = db.orders.find_one({'_id': ObjectId(str(bid))})
    item = db.items.find_one({'_id': order['item_id']})
    action = {'action_type': 'Purchase',
              'agent': 'Harsha',
              'timestamp': Timestamp(int(dt.datetime.today().timestamp()), 1),
              'qty': int(order['count']),
              'bin_id': order['bin_id'],
              'item_id': order['item_id'],
              'supplier': item['supplier']}
    db.history.insert_one(action)

    db.orders.update_one({'_id':order['_id']}, {'$set': {'date': Timestamp(int(dt.datetime.today().timestamp()), 1)}})
    return """<h2>Order dispatched!</h2>"""

def cancel(db, bid):
    db.orders.delete_one({'_id': ObjectId(str(bid))})
    return """<h2>Order cancelled</h2><p><a href="/orders">Return</a>"""

def receive(db, bid):
    order = db.orders.find_one({'_id': ObjectId(str(bid))})
    bin = db.bins.find_one({'_id': order['bin_id']})

    action = {'action_type': 'Receive',
              'agent': 'Harsha',
              'timestamp': Timestamp(int(dt.datetime.today().timestamp()), 1),
              'qty': int(order['count']),
              'bin_id': order['bin_id'],
              'item_id': order['item_id'],
              'via': 'UPS'}

    db.bins.update_one({'_id': order['bin_id']}, {'$set': {'qty': bin['qty']+int(order['count'])}})

    db.orders.update_one({'_id': order['_id']}, {'$set': {'recv_date': Timestamp(int(dt.datetime.today().timestamp()), 1)}})

    db.history.insert_one(action)
    return """<h2>Order received</h2><p><a href="/orders">Return</a>"""