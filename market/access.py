from pickle import FALSE
from market.forms import *
from market import db
from market.models import Product, Location, ProductMovement
import datetime
from flask import render_template, flash

def create_item(type,form):
    data = None
    if type is "product":
        data = form.product_id.data
        form.product_id.data = ''
        item_to_create = Product(product_id=data)
    
    elif type is "location":
        data = form.location_id.data
        form.location_id.data = ''
        item_to_create = Location(location_id=data)
    
    elif type is "transaction":
        item_to_create = ProductMovement(timestamp=str(datetime.datetime.now())[:-7], \
                from_location=form.from_transaction.data,to_location=form.to_transaction.data,\
                    product_id = form.product_id.data,qty =  form.qty.data)

    db.session.add(item_to_create)
    db.session.commit()
    
    flash(f"{type.title()} created successfully!",'success')


def delete_item(type,item_to_delete, form):
    if type is "product":
        form.product_id.data = ''
    
    elif type is "location":
        form.location_id.data = ''
        
    db.session.delete(item_to_delete)
    db.session.commit()
    flash(f'Successfully deleted {type}!','success')


def execution_check(type, form, check_item_database):
    if form.create.data:
            if not check_item_database: 
                create_item(type=type,form=form)
            else:
                flash(f"{type.title()} already exists. No changes made.",'warning')
            
    if form.delete.data:
        
        if not check_item_database: 
            flash(f"{type.title()} does not exist. No deletion made.",'danger')
        else:
            delete_item(type=type,item_to_delete=check_item_database, form=form)


def create_transaction(form):
    if form.create.data:
        if form.from_transaction.data is not '' or form.to_transaction.data is not '':
            create_item(type="transaction",form=form)
    return stocks()
        

def stocks():
    transactions = ProductMovement.query.all()
    products = Product.query.all()
    locations = Location.query.all()
    stock_current = []
    storage = ''
    for location in locations:
        for product in products:
            from_qty,to_qty = 0, 0
            for row in transactions:
                if row.product_id == product.product_id and row.from_location == location.location_id:
                    from_qty += row.qty
            
            for row in transactions:
                if row.product_id == product.product_id and row.to_location == location.location_id:
                    to_qty += row.qty

            if not from_qty and not to_qty:
                continue
            balanced_qty = to_qty - from_qty
            storage += str(product)+":"+str(balanced_qty)+" ,"

            # if balanced_qty > 0:
            #     storage += str(product)+":"+str(balanced_qty)+" ,"

        stock_current.append([str(location), storage])
        storage = ''
                
    

    
    return stock_current

def edit_transaction_form(form):
    form.from_transaction.choices = Location.query.all()
    form.from_transaction.choices.insert(0,'')
    form.to_transaction.choices = Location.query.all()
    form.to_transaction.choices.insert(0,'')
    form.product_id.choices = Product.query.all()