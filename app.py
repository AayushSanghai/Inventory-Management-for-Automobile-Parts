from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from bson.timestamp import Timestamp
from bson import ObjectId
import datetime as dt
import math


import actions
import reports
from helpers import *

app = Flask(__name__)
app.debug = True  # ssh, don't tell anyone!

client = PyMongo(app, uri="mongodb+srv://invent_user:secure@cluster0.pzlhp.mongodb.net/inventory_db?retryWrites=true&w=majority")
# client = MongoClient('mongodb+srv://invent_user:secure@cluster0.pzlhp.mongodb.net?retryWrites=true&w=majority', 27017)

db = client.db


@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "฿{:,.2f}".format(value)


@app.route("/")
def home():
    # types = ['Purchase', 'Receive', 'Dispense', 'Remove', 'Modify']

    actions = query_actions(db)
    bins = db.bins.find({'item_id': {'$ne': None}}).limit(10).sort('location_code')

    b = []

    for bin in bins:
        item = db.items.find_one({'_id': bin['item_id']})
        if item is not None:
            bin['item'] = item['name']
            bin['item_desc'] = item['description']
            b.append(bin)

    if len(actions) > 3:
        actions = actions[0:3]

    # sql = """SELECT * FROM part_bin p LEFT JOIN item i ON i.ID=p.item_id ORDER BY p.location_code ASC"""
    # pg_cur.execute(sql)
    # bins = pg_cur.fetchall()

    return render_template('home.html', actions=actions, bins=b, order_count=count_new_orders(db))


@app.route("/item")
def item_list():
    try:
        text = request.args['stxt']
    except:
        text = ""

    try:
        pg = int(request.args['page'])
    except:
        pg = 0

    query = {"$or": [{"name":{"$regex": text}}, {"description":{"$regex": text}}]}

    pages = int(math.ceil(db.items.count_documents(query)/25))

    pg = min(max(0, pages-1), max(pg, 0))

    items = db.items.find(query).limit(25).skip(pg*25)
    item_data = []

    # get an aggregate count of inventory for this item and join it manually
    for item in items:
        pipe = [
            {'$match': {'item_id': item['_id']}},
            {'$group': {'_id': '$item_id', 'total': {'$sum': '$qty'}}}
        ]
        result = db.bins.aggregate(pipeline=pipe)

        try:
            item["total_qty"] = result.next()['total']
        except:
            item["total_qty"] = '0'
        item_data.append(item)

    # sql = """SELECT item.id,item.name,
	# partn, manufacturer,
	# s.name AS supplier_name,
    # (SELECT SUM(qty) FROM part_bin WHERE item_id=item.id) AS total_qty
	#  FROM item
	# 	LEFT JOIN supplier s ON s.id = item.supplier_id
    #    """
    # pg_cur.execute(sql)
    # items = pg_cur.fetchall()
    return render_template('items.html', items=item_data, pages=pages, page=pg, order_count=count_new_orders(db), search=text)

@app.route("/item/<iid>")
def item(iid):
    item = None

    bins = db.bins.find({"item_id": ObjectId(str(iid))})

    if iid is not None:
        item = db.items.find_one({"_id": ObjectId(str(iid))})

    return render_template('item.html', item=item, bins=bins, order_count=count_new_orders(db))


@app.route("/bin/<bid>")
def part_bin(bid):
    # types = ['Purchase', 'Receive', 'Dispense', 'Remove', 'Modify']
    bin = db.bins.find_one({"_id": ObjectId(str(bid))})
    item = db.items.find_one({'_id': bin['item_id']})

    bin['item_name'] = item['name'] if item is not None else None

    bins = db.bins.find({"location_code": bin["location_code"]})

    bin_list = []

    for b in bins:
        item = db.items.find_one({'_id': b['item_id']})
        if item is not None:
            b['item'] = item['name']
            b['item_desc'] = item['description']
            bin_list.append(b)

    actions = query_actions(db, bin["_id"])
    
    return render_template('bin.html', bin_data=bin, bin_list=bin_list, action_list=actions[0:3], order_count=count_new_orders(db))


@app.route("/action/<act>/<tid>")
def action(act, tid):
    # a little bit of pythonic reflection...
    return actions.__dict__[act](db, tid) if act in actions.__dict__ else "<p>"+act+":"+tid+" is an unknown action!</p>"


@app.route("/history")
def history():
    try:
        pg = int(request.args['page'])
    except:
        pg = 0
    pages = int(math.ceil(db.history.count_documents({}) / 10))

    pg = min(max(0, pages - 1), max(pg, 0))

    actions = db.history.find().sort('timestamp', -1).limit(10).skip(pg * 10)

    ret = []

    for action in actions:
        bin = db.bins.find_one({"_id": action["bin_id"]})
        item = db.items.find_one({"_id": action["item_id"]})
        if bin is not None:
            action["bin"] = bin["location_code"] + "-" + bin["position"]
        if item is not None:
            action["item"] = item["name"]
        ret.append(action)

    return render_template('history.html', actions=ret, pages=pages, page=pg, order_count=count_new_orders(db))

@app.route("/orders")
def orders():
    # types = ['Purchase', 'Receive', 'Dispense', 'Remove', 'Modify']
    orders = db.orders.find({'recv_date': None}).sort('date')

    order_list = []
    for o in orders:
        item = db.items.find_one({'_id': o['item_id']})
        if item is not None:
            o['item_name'] = item['name']
            o['item_desc'] = item['description']
        bin = db.bins.find_one({'_id': o['bin_id']})
        if bin is not None:
            o['bin_name'] = bin['location_code']+'-'+bin['position']
        order_list.append(o)
    return render_template('orders.html', orders=order_list, order_count=count_new_orders(db))


@app.route("/locations")
def locations():
    bins = db.bins.find().sort("location_code")
    bin_list = []
    for bin in bins:
        item = db.items.find_one({'_id': bin['item_id']})
        if item is not None:
            bin['item_name'] = item['name']
        else:
            bin['item_name'] = None
        bin_list.append(bin)
    return render_template('locations.html', bins=bin_list, order_count=count_new_orders(db))


@app.route("/reports")
def report_list():
    return render_template('reports.html', order_count=count_new_orders(db))


@app.route("/report/<rpt>")
def report(rpt):
    return reports.__dict__[rpt](db) if rpt in reports.__dict__ else "<p>" + rpt + " is an unknown report!</p>"


# form handlers
@app.route("/reorder_submit")
def reorder_submit():
    count = request.args['count']
    iid = request.args['iid']
    bid = request.args['bin']
    price = request.args['price']
    sid = request.args['supplier']
    # pg_cur.execute("CALL proc_simulate_order(%s, %s, %s, %s, %s)" % (bid, iid, count, price, sid))
    # pg_conn.commit()
    
    return """<h2>Order submitted!</h2><p><a class="button" href="/item">Return</a>"""


@app.route("/dispense_submit")
def dispense_submit():
    count = request.args['count']
    bid = ObjectId(request.args['bin'])

    bin = db.bins.find_one({'_id': bid})

    action = {'action_type': 'Dispense',
              'agent': 'Harsha',
              'timestamp': Timestamp(int(dt.datetime.today().timestamp()), 1),
              'qty': int(count),
              'bin_id': bid,
              'item_id': bin['item_id']}

    db.history.insert_one(action)

    db.bins.update_one({'_id':bid}, {'$set': {'qty': bin['qty']-int(count)}})
    
    return """<h2>Quantity dispensed!</h2><p><a class="button" href="/bin/%s">Return</a>""" % (bid,)


@app.route("/add_submit")
def add_sumbit():

    item = {'name': request.args['name'],
            'description': request.args['desc'],
            'supplier': request.args['supplier_id'],
            'item_type': request.args['type'],
            'subtype': request.args['subtype'],
            'partn': request.args['partn'],
            'manufacturer': request.args['manufacturer'],
            'reorder_min': request.args['reorder_min']}
    iid = db.items.insert_one(item).inserted_id

    return """<h2>Item added</h2><p><a class="button" href="/item/%s">Continue</a>""" % (iid,)


@app.route("/fillbin_submit")
def fillbin_sumbit():
    iid = ObjectId(request.args['iid'])
    bid = ObjectId(request.args['bin'])
    count = request.args['count']
    max_qty = request.args['max']

    action = {'action_type': 'Modify',
              'agent': 'Harsha',
              'timestamp': Timestamp(int(dt.datetime.today().timestamp()), 1),
              'qty': int(count),
              'bin_id': bid,
              'item_id': iid}

    db.history.insert_one(action)

    bin = db.bins.find_one({'_id': bid})

    db.bins.update_one({'_id': bid}, {'$set': {'item_id': iid, 'qty': bin['qty']+int(count), 'max_qty': int(max_qty)}})

    return """<h2>Bin filled</h2><p><a class="button" href="/bin/%s">Continue</a>""" % (bid,)


@app.route("/order_submit")
def order_submit():
    count = int(request.args['count'])
    iid = ObjectId(request.args['iid'])
    bid = ObjectId(request.args['bin'])
    price = float(request.args['price'])
    sid = request.args['supplier']

    order = {"supplier": sid,
             "cost": count*price,
             "item_id": iid,
             "bin_id": bid,
             "count": count,
             "date": None}
    print(order)
    db.orders.insert_one(order)

    return """<h2>Order submitted!</h2><p><a class="w3-button w3-green w3-round-xlarge w3-hover-teal" href="/item">Return</a>"""


@app.route("/modify_submit")
def modify_submit():
    current = int(request.args['current'])
    count = int(request.args['count'])
    bid = ObjectId(request.args['bin'])
    iid = ObjectId(request.args['iid'])

    action = {'action_type': 'Modify',
              'agent': 'Harsha',
              'timestamp': Timestamp(int(dt.datetime.today().timestamp()), 1),
              'qty': count-current,
              'bin_id': bid,
              'item_id': iid}

    db.history.insert_one(action)

    db.bins.update_one({'_id': bid}, {'$set': {'qty': count}})
    return """<h2>Bin count modified!</h2><p><a class="button" href="/bin/%s">Return</a>""" % (request.args['bin'],)
