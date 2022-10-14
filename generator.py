import random
import pymongo

client = pymongo.MongoClient('mongodb+srv://invent_user:secure@cluster0.pzlhp.mongodb.net/?retryWrites=true&w=majority', 27017)

db = client.inventory_db

dims = ['M4','M6','M8','M10','M12']

# useful globals
types = ["bolt", "pin", "nut", "screw"]

subtypes = [
    ["carriage", "hex", "flange", "structural", "square", "eye"],
    ["clevis", "spring", "cotter", "hitch"],
    ["hex", "lock", "jam", "flange", "wing", "nylock"],
    ["hex", "counter-sink", "mason", "metal", "wood"]
]

desc = [ "galv.", "steel", "stainless steel", "carbon steel"]

manu = ["Hillman", "Acme", "FastenerCo", "BoltCo", "Buildal"]

supplier = ["Acme", "Fastenal", "Bolts2Go", "MSCDirect"]


def generate_items(c):
    for x in range(c):
        t = random.randint(0,len(types)-1)

        item = {'name': random.choice(dims) + " " + types[t],
                'description': random.choice(desc),
                'supplier': random.choice(supplier),
                'item_type': types[t],
                'subtype': random.choice(subtypes[t]),
                'partn': random.randint(1000,1000000),
                'manufacturer': random.choice(manu),
                'reorder_min': random.randint(1,100)}
        db.items.insert_one(item)

bld = ["W1", "W2", "G1", "BT", "CL"]

def generate_bins(c):
    perb = c//5
    for b in bld:
        for x in range(perb):
            pos = chr(x//26+ord('A')) + chr(x%26 + ord('A'))
            bin = {'qty': 0, 'max_qty': 0, 'item_id': None, 'location_code': b, 'position': pos}
            db.bins.insert_one(bin)


if __name__ == "__main__":

    #generate_items(994)
    generate_bins(200)