from flask import Flask, render_template, redirect, Markup, jsonify, url_for, request
import ystockquote

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/stock', methods=['GET'])
def stocks():
  symbol = request.args.get('symbol')
  start = request.args.get('start')
  end = request.args.get('end')
  if not symbol:
    return 'ERROR: Invalid stock symbol'

  if not start or not start.isdigit():
    return 'ERROR: Invalid start date'

  if not end or not start.isdigit():
    return 'ERROR: Invalid end date'

  data = ystockquote.get_historical_prices(symbol, start, end)
  header = data.pop(0)
  return render_template('stock.html', header=header, data=data, symbol=symbol, start_date=start, end_date=end)

app.run()
