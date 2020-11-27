from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
temp = [] #initiating a tuple

#insert the scrapping process here
for i in range(1, len(tr)):
     row = table.find_all('tr')[i]
     
    #get date
     date = row.find_all('td')[0].text
     date = date.strip()
    
   # get currency
     currency = row.find_all('td')[2].text
     currency = currency.strip()
    
     temp.append((date, currency)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','currency'))

#insert data wrangling here
df['currency'] = df['currency'].str.replace(" IDR", "")
df['currency'] = df['currency'][:-2].str.replace(",", "")
df['currency'] = df['currency'].astype('float64').round(2)
df.date= pd.to_datetime(df.date, format = '%m/%d/%Y' )

df.fillna(method='ffill')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["currency"].mean()}'

	# generate plot
	ax = df.plot(x='date', figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]


	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
