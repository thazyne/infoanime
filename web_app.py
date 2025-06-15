# Sistem Rekomendasi Anime Berdasarkan Reviewer's Rating
# Pastikan jikanpy sudah terinstall: pip install jikanpy

from jikanpy import Jikan
import time
from flask import Flask, render_template, request

app = Flask(__name__)

# Fungsi untuk mengambil dan memproses review anime
def get_anime_recommendation(anime_id):
    jikan = Jikan()
    reviews = []
    page = 1
    # Ambil hingga 100 review (maks 20 per halaman, 5 halaman)
    while page <= 2:
        try:
            data = jikan.anime(anime_id, extension='reviews', page=page)
            page_reviews = data.get('data', [])
            if not page_reviews:
                break
            reviews.extend(page_reviews)
            page += 1
            time.sleep(1)  # Tunggu 1 detik antar request
        except Exception as e:
            print(f"Error saat mengambil halaman {page}: {e}")
            page += 1  # Tetap lanjut ke halaman berikutnya meski error
            time.sleep(2)  # Tunggu lebih lama jika error
            continue
    if not reviews:
        print('Tidak ada review ditemukan untuk anime ini.')
        return
    # Ambil semua skor review
    scores = [review.get('score') for review in reviews if review.get('score') is not None]
    if not scores:
        print('Tidak ada review dengan rating valid.')
        return
    avg_score = sum(scores) / len(scores)
    # Tentukan kategori berdasarkan rata-rata
    if avg_score >= 7:
        status = 'Recommended'
        color = '#4CAF50'
    elif avg_score >= 5:
        status = 'Mid'
        color = '#FFB443'
    elif avg_score >= 1:
        status = 'Not Recommended'
        color = '#FF4646'
    else:
        status = 'No Rating'
        color = '#888888'
    print(f"Rata-rata skor review: {avg_score:.2f}")
    print(f"Status Rekomendasi: {status}")
    # Hapus seluruh kode matplotlib dan pengolahan gambar
    # Gantikan return dengan data numerik saja
    return avg_score, status, color

def get_anime_recommendation_flask(anime_id):
    jikan = Jikan()
    reviews = []
    page = 1
    while page <= 5:
        try:
            data = jikan.anime(anime_id, extension='reviews', page=page)
            page_reviews = data.get('data', [])
            if not page_reviews:
                break
            reviews.extend(page_reviews)
            page += 1
            time.sleep(1)
        except Exception as e:
            page += 1
            time.sleep(2)
            continue
    if not reviews:
        return None, None, None
    scores = [review.get('score') for review in reviews if review.get('score') is not None]
    if not scores:
        return None, None, None
    avg_score = sum(scores) / len(scores)
    if avg_score >= 7:
        status = 'Recommended'
        color = '#4CAF50'
    elif avg_score >= 5:
        status = 'Mid'
        color = '#FFB443'
    elif avg_score >= 1:
        status = 'Not Recommended'
        color = '#FF4646'
    else:
        status = 'No Rating'
        color = '#888888'
    # Tidak ada matplotlib, hanya return data
    return avg_score, status, color

def get_anime_id_by_title(title):
    jikan = Jikan()
    try:
        search_result = jikan.search('anime', title)
        time.sleep(1)
        anime_list = search_result.get('data', [])
        if not anime_list:
            return None, None, None, None, None
        anime = anime_list[0]
        anime_id = anime['mal_id']
        anime_title = anime['title']
        anime_image = anime.get('images', {}).get('jpg', {}).get('image_url', '')
        anime_synopsis = anime.get('synopsis', '-')
        return anime_id, anime_title, anime_image, anime_synopsis
    except Exception:
        return None, None, None, None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    result = None
    title = ''
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        anime_id, anime_title, anime_image, anime_synopsis = get_anime_id_by_title(title)
        if not anime_id:
            error = 'Anime tidak ditemukan.'
        else:
            avg_score, status, color = get_anime_recommendation_flask(anime_id)
            if avg_score is None:
                error = 'Tidak ada review valid untuk anime ini.'
            else:
                result = {
                    'title': anime_title,
                    'avg_score': f'{avg_score:.2f}',
                    'status': status,
                    'color': color,
                    'image': anime_image,
                    'synopsis': anime_synopsis
                }
    return render_template('index.html', error=error, result=result, title=title)

if __name__ == '__main__':
    app.run(debug=True)
