""" Specifies routing for the application"""
from flask import render_template, request, jsonify, redirect
from app import app
from app import database as db_helper

@app.route("/create_user", methods=['POST'])
def create_user():
    """ recieves post requests to add new task """
    data = request.get_json()
    print(request)
    db_helper.insert_new_user(data['username'], data['password'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    query_result = db_helper.login_user(data['username'], data['password'])
    result = {'success':True, 'response': 'Login Success'}
    if (query_result == 'No User Found'):
        result['success'] = False
        result['response'] = 'No User Found'
    elif (query_result == 'Wrong Password'):
        result['success'] = False
        result['response'] = 'Wrong Password'
    return jsonify(result)

@app.route("/profile/<string:user_id>", methods=['GET'])
def profile(user_id):
    
    urls = db_helper.find_urls(user_id)
    return render_template("profile.html", items = urls, username=user_id)

@app.route("/create_url/", methods=['POST'])
def create_url():
    data = request.get_json()
    db_helper.insert_new_url(data['long_url'], data['username'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)

@app.route("/remove_url/<string:short_url>", methods=['POST'])
def remove_url(short_url):
    
    try:
        db_helper.delete_url(short_url)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/edit_url/<string:short_url>", methods=['POST'])
def edit_url(short_url):
    data = request.get_json()
    try:
        db_helper.change_url(short_url, data['long_url'])
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)

@app.route("/")
def homepage():
    """ returns rendered homepage """
    return render_template("login.html")

@app.route("/<string:short_url>", methods=['GET'])
def redirect_url(short_url):
    long_url = db_helper.find_long_url(short_url)
    return redirect(long_url)