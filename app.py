from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from datetime import datetime

app = Flask(__name__)
# Enable cors
CORS(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///model/db.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    service = db.Column(db.String(5000), unique=True, nullable=False)
    url = db.Column(db.String(5000), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    pwd = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Pwd %r>' % self.pwd

class PasswordSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('service', 'username', 'pwd', 'url', 'created_at')

db.create_all()


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/pwd', methods=['GET'])
def pwd():
    return render_template('pwd.html')

@app.route('/pwd/list', methods=['GET'])
@app.route('/pwd/list/<service>', defaults={'service': None}, methods=['GET'])
def pwd_list(service=None):    
    if request.args.get("service") is None:
        items = db.session.query(Password).all()
    else:
        pattern = f'%{request.args.get("service")}%'
        with open('log.html', 'w') as f:
            f.write(pattern)
        print('=============>', pattern)
        items = db.session.query(Password        
        ).filter(Password.service.ilike(pattern)
        ).all()
    
    password_schema = PasswordSchema(many=True)
    output = password_schema.dump(items)
    return jsonify({'passwords': output})

@app.route('/pwd/store', methods=['POST'])
def pwd_store():
    # With silent=True set, the get_json function will fail silently when trying to retrieve the json body. 
    # By default this is set to False. 
    # If you are always expecting a json body (not optionally), leave it as silent=False.
    if request.method == 'POST':
        print(request.is_json)
        if not request.is_json:
            return jsonify({'error': 'Only request of JSON type is allowed'})
        postdatas = request.get_json()
        print(postdatas)
        if postdatas is None:
            return jsonify({'error': 'Post data is none'}, 204)       
        pwd = Password(service=postdatas.get('service'), 
            username=postdatas.get('username'), 
            pwd=postdatas.get('pwd'),
            url=postdatas.get('url', '')
        )
        db.session.add(pwd)
        db.session.commit()
        return jsonify({'response': 'Password saved'})


# FLASK_APP=app.py FLASK_ENV=development flask run --port 8080