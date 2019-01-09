from config import Configuration
from flask import Flask, render_template
from f5.bigip import ManagementRoot
import requests

requests.packages.urllib3.disable_warnings()
# Obviously this should be done differently, with app login and users passing f5 credentials, but this is a demo
b = ManagementRoot('ltm3.test.local', 'admin', 'admin')

app = Flask(__name__)
app.config.from_object(Configuration)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/pools', methods=['GET'])
def pools():
    pools = b.tm.ltm.pools.get_collection()
    return render_template('pools.html', pools=pools)


@app.route('/pools/<string:pname>', methods=['GET'])
def pool(pname):
    pool = b.tm.ltm.pools.pool.load(name=pname)
    members = pool.members_s.get_collection()
    return render_template('pool.html', pool=pool, members=members)


if __name__ == '__main__':
    app.run()
