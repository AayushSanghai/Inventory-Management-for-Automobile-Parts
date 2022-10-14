from bson import ObjectId

def query_actions(db, bid=None, limit=None):

    if bid is None:
        actions = db.history.find().limit(3).sort('timestamp', -1)
    else:
        actions = db.history.find({"bin_id": ObjectId(str(bid))}).limit(3).sort('timestamp', -1)

    ret = []

    for action in actions:
        bin = db.bins.find_one({"_id": action["bin_id"]})
        item = db.items.find_one({"_id": action["item_id"]})
        if bin is not None:
            action["bin"] = bin["location_code"] + "-" + bin["position"]
        if item is not None:
            action["item"] = item["name"]
        ret.append(action)

    return ret


def count_new_orders(db):
    c = db.orders.count_documents({"date": None})
    if c==0:
        return ""
    return c
