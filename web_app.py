from flask import Flask, render_template, request
from jikanpy import Jikan

app = Flask(__name__)
jikan = Jikan()

@app.route('/', methods=['GET', 'POST'])
def index():
    judul = None
    anime = None
    review = None
    if request.method == 'POST':
        judul = request.form['judul']
        hasil = jikan.search('anime', judul)
        anime = hasil['data'][0] if hasil['data'] else None
        if anime:
            reviews = jikan.anime(anime['mal_id'], extension='reviews')
            review_data = reviews.get('data', [])
            if review_data:
                review = review_data[0]
    return render_template('index.html', judul=judul, anime=anime, review=review)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
