import re
from market import app
import flask
from flask import render_template, flash
from market.models import Product, Location, ProductMovement
from market.forms import *
from market import db
import datetime
from market.access import *

@app.route('/')
@app.route('/product', methods=['GET', 'POST'])
def product_page():
    """Product Page"""
    form = RegisterProduct()
    if form.validate_on_submit():
        if flask.request.method == 'POST':
            check_item_database = Product.query.filter_by(product_id=form.product_id.data).first()
            execution_check("product",form, check_item_database)
            render_temp_refresh(type="product", form=form)
        else : # GET request
            render_temp_refresh(type="product", form=form)

    return render_temp_refresh(type="product", form=form)


@app.route('/location', methods=['GET', 'POST'])
def location_page():
    """Location Page"""
    form = RegisterLocation()
    if form.validate_on_submit():

        if flask.request.method == 'POST':
            check_item_database = Location.query.filter_by(location_id=form.location_id.data).first()
            execution_check("location",form, check_item_database)
            
            render_temp_refresh(type="location", form=form)
        else : # GET request
            render_temp_refresh(type="location", form=form)


    return render_temp_refresh(type="location", form=form)


@app.route('/transaction', methods=['GET', 'POST'])
def transaction_page():
    form = RegisterTransaction()
    edit_transaction_form(form)
    if form.validate_on_submit():
        create_transaction(form)    
    else : # GET request
        return render_temp_refresh(type="transaction", form=form)


    return render_temp_refresh(type="transaction", form=form)
    

def render_temp_refresh(type, form):
    if type is "location":
        items = Location.query.all()
        report = stocks()
        return render_template('location.html', items=items, form=form, report=report)
    
    elif type is "product":
        items = Product.query.all()
        return render_template('product.html', items=items, form=form)

    elif type is "transaction":
        items = ProductMovement.query.all()
        return render_template('transaction.html', items=items, form=form)