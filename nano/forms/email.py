from flask.ext.wtf import (Form, HiddenField, BooleanField, TextField,
                          SubmitField, SelectField, FormField, TextAreaField,
                          ValidationError, required, equal_to, email,
                          length)

from nano.extensions import db

class EmailForm(Form):
    
    to          = TextField('To',           [required()])
    bcc         = TextField('BCC',          [required()])
    subject     = TextField('Subject',      [required()])
    message     = TextAreaField('Message',  [required()])

    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(EmailForm, self).__init__(formdata, obj, prefix, kwargs)


    def save(self):
        pass


