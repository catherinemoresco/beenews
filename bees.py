from flask import Flask, render_template
from flask.ext.cache import Cache

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

import requests
from bs4 import BeautifulSoup



@cache.cached(timeout=43200)
def beenews():
  # cache to update once a day only (thanks, Google captcha)

  r = requests.get('https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q=bees&oq=bees&gs_l=news-cc.3..43j0l10j43i53.5224.5630.0.5735.4.4.0.0.0.0.76.173.3.3.0...0.0...1ac.1.XVE1F-CxNM8')
  curated_headlines = {}
  soup = BeautifulSoup(r.text, "lxml")

  headlines = soup.find_all('h3')
  for hl in headlines:
    if u'r' in hl.attrs.get(u'class'):
      sl = hl.findNext('div')
      st = sl.findNext('div')
      curated_headlines[hl.text] = [hl.a.attrs.get(u'href').split('&')[0].split('/url?q=')[1], sl.text, st.text]
  print curated_headlines
  return render_template('home.html', curated_headlines=curated_headlines)

@app.route("/")
def bees():
  return beenews()

if __name__ == "__main__":
    app.run(port=5001)