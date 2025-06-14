from flask import Flask, request, redirect, render_template
import string, random, json, os

app = Flask(__name__)
DATA_FILE = 'url_data.json'

# Load or initialize mapping
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        url_mapping = json.load(f)
else:
    url_mapping = {}

# Reverse mapping for quick lookup
reverse_mapping = {v: k for k, v in url_mapping.items()}

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

def save_to_file():
    with open(DATA_FILE, 'w') as f:
        json.dump(url_mapping, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    short_url = None
    if request.method == 'POST':
        original_url = request.form['long_url'].strip()

        # Check if already shortened
        if original_url in reverse_mapping:
            short_id = reverse_mapping[original_url]
        else:
            short_id = generate_short_id()
            while short_id in url_mapping:
                short_id = generate_short_id()
            url_mapping[short_id] = original_url
            reverse_mapping[original_url] = short_id
            save_to_file()

        short_url = request.host_url + short_id

    return render_template('index.html', short_url=short_url)

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    long_url = url_mapping.get(short_id)
    if long_url:
        return redirect(long_url)
    return render_template('not_found.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
