from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import json
import os

# Set Matplotlib backend to a non-interactive mode
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

# Create static folder if it doesn't exist for heatmap storage
if not os.path.exists("static"):
    os.makedirs("static")

def evaluate_url(url):
    """Evaluate the usability of a given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch URL: {url}. Error: {str(e)}"}

    soup = BeautifulSoup(response.text, 'html.parser')

    images_missing_alt = [
        img.get('src', 'No src attribute') for img in soup.find_all('img') if not img.get('alt')
    ]
    headings = {
        'h1': len(soup.find_all('h1')),
        'h2': len(soup.find_all('h2'))
    }
    page_title = soup.title.string if soup.title else 'No Title Found'

    return {
        'title': page_title,
        'images_missing_alt': images_missing_alt,
        'headings': headings
    }

def generate_heatmap():
    """Generate a sample heatmap for visual attention."""
    data = np.random.random((10, 10))
    plt.figure(figsize=(6, 6))  # Set figure size
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.title("Visual Attention Heatmap")
    plt.savefig("static/heatmap.png")  # Save heatmap to static folder
    plt.close()  # Close the plot to avoid issues with multiple renders

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    url = request.form['url']
    evaluation_result = evaluate_url(url)
    
    if 'error' in evaluation_result:
        return render_template('error.html', error=evaluation_result['error'])
    
    generate_heatmap()  # Generate a heatmap as part of the evaluation
    return render_template('result.html', result=evaluation_result)

@app.route('/export', methods=['POST'])
def export():
    url = request.form['url']
    evaluation_result = evaluate_url(url)
    
    if 'error' in evaluation_result:
        return render_template('error.html', error=evaluation_result['error'])

    with open('results.json', 'w') as f:
        json.dump(evaluation_result, f, indent=4)
    return "Results exported successfully!"

if __name__ == "__main__":
    app.run(debug=True)
