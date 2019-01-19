from flask_codemirror import CodeMirror
from config import Configuration
from flask import Flask, render_template, request, flash, redirect, url_for, session
from forms import EditorForm, F5DeviceForm
from f5.bigip import ManagementRoot
import requests

requests.packages.urllib3.disable_warnings()
# Obviously this should be done differently, with app login and users passing f5 credentials, but this is a demo


app = Flask(__name__)
app.config.from_object(Configuration)
codemirror = CodeMirror(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    form = F5DeviceForm(request.form)
    # Add form validation!!
    if request.method == 'POST':

        session['host'] = request.form['host']
        session['uname'] = request.form['uname']
        session['upass'] = request.form['upass']

        b = ManagementRoot(session['host'], session['uname'], session['upass'])

        flash('BIG-IP Instantiated', 'success')
        return redirect(url_for('home'))

    return render_template('connect.html', form=form)


@app.route('/pools', methods=['GET'])
def pools():
    b = ManagementRoot(session['host'], session['uname'], session['upass'])
    pools = b.tm.ltm.pools.get_collection()
    return render_template('pools.html', pools=pools, host=b.hostname)


@app.route('/pools/<string:name>', methods=['GET'])
def pool(name):
    b = ManagementRoot(session['host'], session['uname'], session['upass'])
    pool = b.tm.ltm.pools.pool.load(name=name)
    members = pool.members_s.get_collection()
    return render_template('pool.html', pool=pool, members=members, host=b.hostname)


@app.route('/rules', methods=['GET'])
def rules():
    b = ManagementRoot(session['host'], session['uname'], session['upass'])
    rules = b.tm.ltm.rules.get_collection()
    return render_template('rules.html', rules=rules, host=b.hostname)


@app.route('/add_rule', methods=['GET', 'POST'])
def add_rule():
    form = EditorForm(request.form)
    b = ManagementRoot(session['host'], session['uname'], session['upass'])
    # Add form validation!!
    if request.method == 'POST':
        rule_name = request.form['rule_name']
        rule_partition = request.form['rule_partition']
        rule_body = request.form['rule_body'].replace('\r\n', '\\r\\n')

        if not b.tm.ltm.rules.rule.exists(name=rule_name, partition=rule_partition):
            r1 = b.tm.ltm.rules.rule.create(name=rule_name, partition=rule_partition, apiAnonymous=rule_body)
            flash('Rule created', 'success')
            return redirect(url_for('rules'))
        else:
            flash('Rule already exists, try another name', 'info')
            return redirect(url_for('add_rule'))

    return render_template('add_rule.html', form=form, host=b.hostname)


@app.route('/edit_rule/<string:name>', methods=['GET', 'POST'])
def edit_rule(name):
    partition, name = name.split('~')
    b = ManagementRoot(session['host'], session['uname'], session['upass'])
    rule = b.tm.ltm.rules.rule.load(name=name, partition=partition)
    form = EditorForm(request.form)
    form.rule_name.data = rule.name
    form.rule_partition.data = rule.partition
    form.rule_body.data = rule.apiAnonymous
    # Add form validation!!
    if request.method == 'POST':
        rule_name = request.form['rule_name']
        rule_partition = request.form['rule_partition']
        rule_body = request.form['rule_body']
        # Set attributes on BIG-IP object and update
        r1 = b.tm.ltm.rules.rule.load(name=rule_name, partition=rule_partition)
        r1.apiAnonymous = rule_body
        r1.update()

        flash('Rule updated', 'success')
        return redirect(url_for('rules'))

    return render_template('edit_rule.html', form=form, host=b.hostname)



