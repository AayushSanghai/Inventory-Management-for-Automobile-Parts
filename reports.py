
from flask import render_template
import pandas as pd
import json
import plotly
import plotly.express as px

from helpers import *


def orders(db):
    d = db.orders.count_documents({"recv_date": None})
    r = db.orders.count_documents({}) - d

    df = pd.DataFrame({
        "Status": ["Dispatched", "Received"],
        "Amount": [d, r]
    })

    fig = px.bar(df, x="Status", y="Amount", color="Status")

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('report.html', graphJSON=graphJSON, header="Orders MTD")

def storage(db):
    n = db.bins.count_documents({"item_id": None})
    e = db.bins.count_documents({"$and": [{"item_id": {"$ne": None}}, {"qty": 0}]})
    u = db.bins.count_documents({}) - (n+e)

    df = pd.DataFrame({
        "Type": ["Used", "Empty", "Unused"],
        "Count": [u, e, n]
    })

    fig = px.pie(df, values='Count', names='Type')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('report.html', graphJSON=graphJSON, header="Storage")
