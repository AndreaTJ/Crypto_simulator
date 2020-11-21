from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError
from the_app.resources.funciones.funciones import Saldo_moneda
from the_app import app 


def valida_posibilidad_compra(form, field):
    if field.data ==form.Moneda_from.data:
        raise ValidationError("No transaction between equal currencies can be accepted.")
    elif field.data != "BTC" and form.Moneda_from.data == "EUR": 
        raise ValidationError("You cannot exchange EUR to {} directly. You can only purchase {}, with other cryptocurrencies.".format(field.data,field.data ))
    elif field.data == "EUR" and form.Moneda_from.data != "BTC":
        raise ValidationError("You cannot exchange {} to EUR directly. It is only possible to exchange BTC to EUR. If you want EUR, please exchange your {} to BTC first and try again.".format(form.Moneda_from.data, form.Moneda_from.data))
      

Cryptos = app.config['CRYPTOMONEDAS']
MonedaInicial = app.config['EUROS']
Monedas_posibles_to = [MonedaInicial] + Cryptos

class PurchaseForm(FlaskForm): 
    Moneda_from = SelectField(label='From:', choices=[(moneda, moneda) for moneda in MonedaInicial])
    Moneda_to = SelectField(label='To:', choices=[(moneda, moneda) for moneda in Monedas_posibles_to], validators=[valida_posibilidad_compra])
    Cantidad_from = FloatField('Q:', validators=[DataRequired(message="Please, enter a numerical quantity greater than zero. Decimal numbers must be separated by a period (.)")])
    Cantidad_to = HiddenField('Cantidad_To')
    ComprobacionMonedaFrom = HiddenField('ComprobacionMonedaFrom')
    ComprobacionMonedaTo = HiddenField('ComprobacionMonedaTo')
    ComprobacionCantidadFrom = HiddenField('ComprobacionCantidadFrom')
    calcular = SubmitField('Calcular')
    aceptar =  SubmitField('ACCEPT TRANSACTION')
    

    def validate_Cantidad_from(self,field): 
        if field.data < 0: 
            raise ValidationError("Please, enter a positive number")
        if field.data < 1e-8: 
            raise ValidationError("No pueden realizarse transacciones automáticamente con cantidades inferiores a 1e-8. Por favor, si necesita hacer una transacción con una cantidad inferior a 1e-8, contacte con el administrador.")
        if field.data > 1000000000: 
             raise ValidationError("No pueden realizarse transacciones automáticamente con cantidades mayores a 1000000000. Por favor, si necesita hacer una transacción con una cantidad mayor a 1000000000, contacte con el administrador.")

        
        if self.Moneda_from.data != "EUR":
            saldo = Saldo_moneda(self.Moneda_from.data)
            if field.data > saldo: 
                raise ValidationError("You do not have a sufficient balance of {} to carry out your operation. Your current balance of {} is {:,.8f}".format (self.Moneda_from.data, self.Moneda_from.data, saldo))
    
   
    
    
    
    

