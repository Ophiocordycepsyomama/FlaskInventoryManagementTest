from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,SelectField
from wtforms.validators import Length, DataRequired

class RegisterTransaction(FlaskForm):
    from_transaction = SelectField(label='From:')
    to_transaction = SelectField(label='To:')
    product_id = SelectField(label='Product', validators=[ DataRequired()])
    qty = IntegerField('Qty', validators=[ DataRequired()])
    submit = SubmitField(label='Create/Edit')
    submit1 = SubmitField(label='Delete')

class RegisterProduct(FlaskForm):
    product_id = StringField(label='Product Name:', validators=[Length(min=2, max=30), DataRequired()])
    qnty = StringField(label='Quntity:', validators=[Length(min=2, max=30), DataRequired()])
    submit = SubmitField(label='Create/Edit Product')
    submit1 = SubmitField(label='Delete Product')

class RegisterLocation(FlaskForm):
    location_id = StringField(label='Product Name:', validators=[Length(min=2, max=30), DataRequired()])
    submit = SubmitField(label='Create/Edit Location')
    submit1 = SubmitField(label='Delete Location')

