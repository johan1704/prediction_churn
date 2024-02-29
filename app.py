# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 15:41:58 2023

@author: PROBOOK
"""

import plotly.graph_objects as go
from werkzeug.utils import import_string
import werkzeug
werkzeug.import_string = import_string
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import plotly.express as px
from sqlalchemy.sql import func

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost/cap_dap'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost:5433/test'

db = SQLAlchemy(app)

class DataPoint(db.Model):
    __tablename__ = 'budget_table'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    date = db.Column(db.Date)  # Assuming transaction_date is of type Date
    budget1 = db.Column(db.Float)  # Assuming budget1 is of type Float
    budget2 = db.Column(db.Float)  # Assuming budget2 is of type Float
    
@app.route('/line-chart')
def index():
    # Retrieve aggregated data from the database, extract month, and group by month
    data = db.session.query(func.date_trunc('month', DataPoint.date).label('month'),
                             func.sum(DataPoint.budget1).label('sum_budget1'),
                             func.sum(DataPoint.budget2).label('sum_budget2')) \
                     .group_by('month') \
                     .order_by('month') \
                     .all()

    # Extract month, sum_budget1, and sum_budget2 data
    month_data, sum_budget1_data, sum_budget2_data = zip(*data)

    # Create a Plotly.js graph with two y-axes
    fig = px.line(x=month_data, y=[sum_budget1_data, sum_budget2_data], labels={'x': 'Month', 'y': 'Amount'}, title='Sum of Budget1 and Budget2 Per Month', line_shape='spline')

    # Update y-axis titles
    fig.update_yaxes(title_text="Sum of Budget1", secondary_y=False)
    fig.update_yaxes(title_text="Sum of Budget2", secondary_y=True)
    graph_json = fig.to_json()

    return render_template('index.html', graph_json_line=graph_json, graph_json_bar=None)


@app.route('/bar-chart')
def bar_chart():
    # ... (your existing code)
    # Retrieve aggregated data from the database, extract month, and group by month
    data = db.session.query(func.date_trunc('month', DataPoint.date).label('month'),
                             func.sum(DataPoint.budget1).label('sum_budget1'),
                             func.sum(DataPoint.budget2).label('sum_budget2')) \
                     .group_by('month') \
                     .order_by('month') \
                     .all()

    # Extract month, sum_budget1, and sum_budget2 data
    month_data, sum_budget1_data, sum_budget2_data = zip(*data)

    # Create a Plotly.js graph with a bar chart
    fig = px.bar(x=month_data, y=[sum_budget1_data, sum_budget2_data], labels={'x': 'Month', 'y': 'Amount'},
                 title='Sum of Budget1 and Budget2 Per Month',barmode='group')

    # Convert the graph to JSON
    graph_json = fig.to_json()

    return render_template('index.html', graph_json_line=None, graph_json_bar=graph_json)

    