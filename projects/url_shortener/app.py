from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import shortuuid

app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

# Create a table to store URLs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        long_url TEXT NOT NULL,
        short_url TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Define the route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to handle URL shortening
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url')
    if not long_url:
        return redirect(url_for('index'))

    # Generate a short URL using shortuuid
    short_url = shortuuid.uuid()[:8]

    # Insert the URL into the database
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO urls (long_url, short_url) VALUES (?, ?)', (long_url, short_url))
    conn.commit()
    conn.close()

    return render_template('index.html', short_url=short_url)

# Define a route to handle redirection to the original URL
@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url FROM urls WHERE short_url = ?', (short_url,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        long_url = result[0]
        return redirect(long_url)
    else:
        return "URL not found."

# Define a route to display all shortened URLs
@app.route('/all_urls')
def all_urls():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT long_url, short_url FROM urls')
    urls = cursor.fetchall()
    conn.close()
    
    return render_template('all_urls.html', urls=urls)


if __name__ == '__main__':
    app.run(debug=True)
