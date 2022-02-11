from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,SelectField
from wtforms.validators import Length, DataRequired,ValidationError

class RegisterTransaction(FlaskForm):
    def validate_name(self, qty):
        if qty.data < 1:
            raise ValidationError('Quantity cannot be negative.')
    
    from_transaction = SelectField(label='From:')
    to_transaction = SelectField(label='To:')
    product_id = SelectField(label='Product', validators=[DataRequired()])
    qty = IntegerField('Qty', validators=[DataRequired(),validate_name])
    create = SubmitField(label='Create/Edit')
    delete = SubmitField(label='Delete')

    

class RegisterProduct(FlaskForm):
    product_id = StringField(label='Product Name:', validators=[Length(min=2, max=30), DataRequired()])
    
    create = SubmitField(label='Create/Edit Product')
    delete = SubmitField(label='Delete Product')

class RegisterLocation(FlaskForm):
    location_id = StringField(label='Location Name:', validators=[Length(min=2, max=30), DataRequired()])
    create = SubmitField(label='Create/Edit Location')
    delete = SubmitField(label='Delete Location')

