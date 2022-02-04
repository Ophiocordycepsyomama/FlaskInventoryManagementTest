from market import app
from flask import render_template, redirect, url_for
from market.models import Product, Location, ProductMovement
from market.forms import *
from market import db
import datetime

@app.route('/')
@app.route('/product', methods=['GET', 'POST'])
def product_page():
    form = RegisterProduct()
    items = Product.query.all()
    if form.validate_on_submit():
        check_item = Product.query.filter_by(product_id=form.product_id.data).first()
        if(form.submit.data):
            if(check_item ):
                check_item.qnty = form.qnty.data
                db.session.add(check_item)
                db.session.commit()

            else:
                product_to_create = Product(product_id=form.product_id.data, qnty=int(form.qnty.data))
                db.session.add(product_to_create)
                db.session.commit()
        
        if(form.submit1.data):
            if(check_item ):
                db.session.delete(check_item)
                db.session.commit()

        
        items = Product.query.all()
        form.product_id.data = ''
        form.qnty.data = ''
        return render_template('product.html', items=items, form=form)

    return render_template('product.html', items=items, form=form)


@app.route('/location', methods=['GET', 'POST'])
def location_page():
    form = RegisterLocation()
    items = Location.query.all()
    for item in items:
        item.storage = item.storage.replace(",",":")
        item.storage = item.storage.replace(";"," , ")
        item.storage = item.storage[:-2]

        
    if form.validate_on_submit():
        check_item = Location.query.filter_by(location_id=form.location_id.data).first()
        if(form.submit.data):
            if(check_item ):
                check_item.location_id = form.location_id.data
                db.session.add(check_item)
                db.session.commit()

            else:
                location_to_create = Location(location_id=form.location_id.data, storage='')
                db.session.add(location_to_create)
                db.session.commit()
        
        if(form.submit1.data):
            if(check_item ):
                db.session.delete(check_item)
                db.session.commit()

        
        items = Location.query.all()
        for item in items:
            item.storage = item.storage.replace(",",":")
            item.storage = item.storage.replace(";"," , ")
            item.storage = item.storage[:-2]
        form.location_id.data = ''
        return render_template('location.html', items=items, form=form)
    return render_template('location.html', items=items, form=form)

# to -> from 
# -> to ==>done
# from -> 

@app.route('/transaction', methods=['GET', 'POST'])
def transaction_page():
    form = RegisterTransaction()
    items = ProductMovement.query.all()
    
    form.from_transaction.choices = Location.query.all()
    form.from_transaction.choices.insert(0,'')
    form.to_transaction.choices = Location.query.all()
    form.to_transaction.choices.insert(0,'')
    form.product_id.choices = Product.query.all()

    if form.validate_on_submit():
        
        if(form.to_transaction.data != '' or form.from_transaction.data != ''):
            
            if(form.submit.data):
                flagSucess = 0
                if(form.from_transaction.data == ''):
                   situation1()

                elif(form.to_transaction.data == ''):
                    situation2()

                else:
                    situation3()
                    

            if(form.submit1.data):
                return "nope"

            items = ProductMovement.query.all()
            return render_template('transaction.html', items=items, form=form)

    return render_template('transaction.html', items=items, form=form)


def trancheck():
    form = RegisterTransaction()
    a = ProductMovement(timestamp=str(datetime.datetime.now()), \
                from_location=form.from_transaction.data,to_location=form.to_transaction.data,\
                    product_id = form.product_id.data[:form.product_id.data.index('|')],qty =  form.qty.data)
    
    return a

def situation1():
    form = RegisterTransaction()
    
    check_item = Location.query.filter_by(location_id=form.to_transaction.data).first()
    check_item2 = Product.query.filter_by(product_id=form.product_id.data[:form.product_id.data.index('|')]).first()
    
    if(check_item2.qnty >= form.qty.data):
    
        if(check_item2.qnty == form.qty.data):
            db.session.delete(check_item2)
            db.session.commit()
            form = RegisterTransaction()
    
        else:
            check_item2.qnty -= form.qty.data
            db.session.add(check_item2)
            db.session.commit()

        ss = check_item.storage.split(';')
        ss.pop()
        aa = [i.split(',') for i in ss]
        flag = 0
    
        for a in aa:
    
            if(a[0]==form.product_id.data[:form.product_id.data.index('|')]):
                flag = 1
                a[1] = str(int(a[1]) + form.qty.data)
                temp = ''
    
                for a1 in aa:
                    temp += a1[0] +','+ a1[1]+';'
                check_item.storage = temp
    
                break

        if(flag == 0):
            check_item.storage += form.product_id.data[:form.product_id.data.index('|')]+","+str(form.qty.data)+";"

        db.session.add(check_item)
        db.session.commit()
        transaction_to_create = trancheck()
        db.session.add(transaction_to_create)
        db.session.commit()
    

def situation2():
    form = RegisterTransaction()
    
    check_item = Location.query.filter_by(location_id=form.from_transaction.data).first()
    check_item2 = Product.query.filter_by(product_id=form.product_id.data[:form.product_id.data.index('|')]).first()
    
    ss = check_item.storage.split(';')
    ss.pop()
    aa = [i.split(',') for i in ss]
    flag = 0
    
    for a in aa:
    
        if(a[0]==form.product_id.data[:form.product_id.data.index('|')]):
    
            if(int(a[1])>form.qty.data):
                a[1] = str(int(a[1]) - form.qty.data)
                flag = 1
            
            elif(int(a[1])==form.qty.data):
                aa.remove(a)
                flag = 1

            if(flag==1):
                check_item2.qnty += form.qty.data
                temp = ''
    
                for a1 in aa:
                    temp += a1[0] +','+ a1[1]+';'
    
                check_item.storage = temp
                transaction_to_create = trancheck()
                db.session.add(transaction_to_create)
                db.session.commit()
            
            db.session.add(check_item)
            db.session.commit()
            db.session.add(check_item2)
            db.session.commit()
    
            break

def situation3():
    form = RegisterTransaction()
    
    check_item = Location.query.filter_by(location_id=form.to_transaction.data).first()
    check_item1 = Location.query.filter_by(location_id=form.from_transaction.data).first()
    
    ss = check_item.storage.split(';')
    ss.pop()
    aa = [i.split(',') for i in ss] #to
    ss = check_item1.storage.split(';')
    ss.pop()
    aa1 = [i.split(',') for i in ss] #from
    
    flag = 0
    flagnew = 0
    
    for a in aa1:
    
        if(a[0]==form.product_id.data[:form.product_id.data.index('|')]):
                
    
            if(int(a[1])>form.qty.data):
                a[1] = str(int(a[1]) - form.qty.data)
                flag = 1
            
            elif(int(a[1])==form.qty.data):
                aa1.remove(a)
                flag = 1

            if(flag==1):
    
                for b in aa:
    
                    if(b[0]==form.product_id.data[:form.product_id.data.index('|')]):
                        flagnew = 1
                        b[1]= str(int(b[1]) + form.qty.data)
    
                        break

                temp = ''
    
                for a1 in aa1:
                    temp += a1[0] +','+ a1[1]+';'
    
                check_item1.storage = temp
                db.session.add(check_item1)
                db.session.commit()

                temp = ''
    
                for a2 in aa:
                    temp += a2[0] +','+ a2[1]+';'
                
                if(flagnew == 0):
                    check_item.storage = temp+form.product_id.data[:form.product_id.data.index('|')] \
                        +","+str(form.qty.data)+";"
                
                else:
                    check_item.storage = temp
                    
                db.session.add(check_item)
                db.session.commit()

                transaction_to_create = trancheck()
                db.session.add(transaction_to_create)
                db.session.commit()

            break