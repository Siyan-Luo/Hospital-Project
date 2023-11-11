from flask import Flask, render_template, request, jsonify, request, send_file
from flask_cors import CORS
from flask_qrcode import QRcode
from io import BytesIO

# from flask_qrcode import QRcode

import webbrowser
import sqldb

app = Flask(__name__)
CORS(app)
qrcode = QRcode(app)

#进入首页
@app.route('/')
# def hei():
# 	return render_template('test.html')
#
#进入'index'页面
@app.route('/index/')
#进入后自动运行下面函数
def index():
	return render_template('goods.html')

@app.route('/other/')
def other():
	return render_template('inventory.html')


@app.route('/data/goods/')
def getgoods():
#data数据要以这种方式命名是为了LAYUI的数据要求
	data = {"code": 0, "msg": ""}
	name = request.args.get('search_name') or ''
	reference = request.args.get('search_reference') or ''
	factory = request.args.get('search_factory') or''
	
	# process = request.args.get('search_process') or ''
	# lst = sqldb.select_goods(name, model, process)
	lst = sqldb.select_goods(name, reference, factory)
	# for i in lst:
	# 	i['needbuy'] = int(i['safenumber']) - int(i['number'])
	data['count'] = len(lst)
	data['data'] = lst
	return data


@app.route('/data/inventory/')
def getinventory():
	data = {"code": 0, "msg": ""}
	name = request.args.get('search_name') or ''
	model = request.args.get('search_model') or ''
	factory = request.args.get('search_factory') or ''
	# process = request.args.get('search_process') or ''
	# lst = sqldb.select_goods(name, model, process)
	lst = sqldb.select_inventory(name, model, factory)
	# for i in lst:
	# 	i['needbuy'] = int(i['safenumber']) - int(i['number'])
	data['count'] = len(lst)
	data['data'] = lst
	return data



@app.route('/op/<kind>')
def op(kind):
	if kind == 'in':
		# id = request.args.get('in_id')
		change = request.args.get('in_change')
		reference = request.args.get('in_reference')
		factory = request.args.get('in_factory')
		lot = request.args.get('in_lot')
		internal_lot = request.args.get('in_internal_lot')
		# print(change)
		# print(reference)
		# print(factory)
		# print(lot)
		# print(internal_lot)
		# people = request.args.get('in_people');
		# sqldb.insert_records(id, 1, change, people)
		sqldb.update_inventory(reference, factory, lot, internal_lot, change, 1)


	elif kind == 'out':
		# id = request.args.get('out_id')
		change = request.args.get('out_change')
		reference = request.args.get('out_reference')
		factory = request.args.get('out_factory')
		lot = request.args.get('out_lot')
		internal_lot = request.args.get('out_internal_lot')
		# print(change)
		# print(reference)
		# print(factory)
		# print(lot)
		# print(internal_lot)
		# people = request.args.get('out_people');
		# sqldb.insert_records(id, 0, change, people)
		sqldb.update_inventory(reference, factory, lot, internal_lot, change, 0)


	elif kind == 'add':
		name = request.args.get('add_name')
		reference = request.args.get('add_reference')
		factory = request.args.get('add_factory') or ''
		num = request.args.get('add_num')
		lot = request.args.get('add_lot')
		# internal_lot = request.args.get('add_internal_lot')
		arrival_date = request.args.get('add_arrival')
		expiry_date =request.args.get('add_expiry')
		# process = request.args.get('add_process')
		# price = request.args.get('add_price') or 0
		# sqldb.insert_goods(name, model, factory, process, price)
		# sqldb.insert_goods(name, model, factory, num, lot, internal_lot, arrival_date, expiry_date)
		sqldb.insert_inventory(name, reference, factory, num, lot, arrival_date, expiry_date)
	elif kind == 'del':
		# id = request.args.get('del_id')
		# sqldb.del_goods(id)
		name = request.args.get('del_name')
		reference = request.args.get('del_reference')
		factory = request.args.get('del_factory')
		lot = request.args.get('del_lot')
		internal_lot = request.args.get('del_internal_lot')
		# print(name)
		# print(reference)
		# print(factory)
		# print(lot)
		# print(internal_lot)
		sqldb.del_inventory(reference, factory, lot, internal_lot)

	elif kind == 'edit':
		reference = request.args.get('edit_reference')
		safenumber = request.args.get('edit_safenumber')
		factory = request.args.get('edit_factory')
		# total_num =request.args.get('edit_total_num')
		# print(total_num)
		# print(reference)
		# print(safenumber)
		# print(factory)
		sqldb.edit_safenumber(safenumber, reference, factory)
	# elif kind == 'qrcode':

	return jsonify()



@app.route('/error/')
def error():
	return "500"


if __name__ == '__main__':
	webbrowser.open("http://127.0.0.1:5000/")
	app.run()
