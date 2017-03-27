from flask import Flask, render_template, request, redirect
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.charts import TimeSeries

app = Flask(__name__)
#app.config['DEBUG'] = True

import datetime
from calendar import monthrange
td =  datetime.datetime.today()
ndays_this_month = monthrange(td.year, td.month)[1]
start_date = td - datetime.timedelta(days=ndays_this_month)

def get_series(symbol):
  from pandas_datareader import data
  return data.DataReader(symbol, "yahoo", start_date)

js_resources = INLINE.render_js()
css_resources = INLINE.render_css()

@app.route('/')
def main():
  return redirect('/plot')

@app.route('/setsymbol', methods=['POST'])
def setsymbol():
  print request.form['symbol']
  return redirect('/plot?symbol=%s'% request.form['symbol'])

@app.route('/plot')
def plot_():
  current_stock_symbol = request.args.get('symbol')
  if current_stock_symbol is None:
	return render_template('noplot.html')
    
  dat = get_series(current_stock_symbol)
  js_resources = INLINE.render_js()
  css_resources = INLINE.render_css()
  hp = TimeSeries(dat[['Close']],plot_width=800, plot_height=300,
             title="%s daily Closing Price" % current_stock_symbol, ylabel="price in $", xlabel="Date")
  script, div = components(hp, INLINE)
  html=render_template(
     'plot.html',
      plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        color='Color',
    )
  return encode_utf8(html)

if __name__ == '__main__':
  app.run('0.0.0.0', port=33507)
