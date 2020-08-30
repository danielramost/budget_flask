import csv
from flask import Flask, make_response, redirect, render_template, request, url_for
from io import StringIO
from markupsafe import escape

from models import *

app = Flask(__name__)

users=[]
categories=[]

@app.route('/')
def index():
    expenses = Expense.get_expenses_for_table()
    global users
    users = User.all()
    global categories
    categories = Category.all()

    return render_template('index.html', expenses_data = expenses)

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'POST':
        data = get_data_from_request(request)
        expense = Expense(data=data)
        expense.create_expense()
        return redirect(url_for('index'))
    else:
        return render_template('expense.html',
            header='Nuevo', users=users, categories=categories,
            expense=Expense()
        )

@app.route('/edit/<string:id>', methods=['GET','POST'])
def edit(id):
    if request.method == 'POST':
        data = get_data_from_request(request)
        expense = Expense(data=data, id=id)
        expense.update_expense()
        return redirect(url_for('index'))
    else:
        expense = Expense.get_expense(id)
        return render_template('expense.html',
            header='Modificar', users=users, categories=categories,
            expense=expense
        )

def get_data_from_request(request):
    full_category = request.form.get('category')
    group, category = full_category.split(' ==> ')

    return {
        'date': request.form.get('date'),
        'user': request.form.get('user'),
        'value': request.form.get('value'),
        'group': group,
        'category': category,
        'comment': request.form.get('comment'),
    }

@app.route('/download')
def download():
    expenses = Expense.get_expenses_for_download()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(expenses)

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=gastos.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/delete_all', methods=['GET','POST'])
def delete_all():
    if request.method == 'POST':
        Expense.delete_all()
        return redirect(url_for('index'))
    else:
        return render_template('delete_all.html')
