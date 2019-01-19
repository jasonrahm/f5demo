from flask_wtf import FlaskForm
from flask_codemirror.fields import CodeMirrorField
from wtforms import StringField, PasswordField


class F5DeviceForm(FlaskForm):
    host = StringField('Hostname')
    uname = StringField('Username')
    upass = PasswordField('Password')


class EditorForm(FlaskForm):
    rule_name = StringField('Name')
    rule_partition = StringField('Partition', default='Common')
    rule_body = CodeMirrorField(language='tcl', config={'lineNumbers': 'true'})