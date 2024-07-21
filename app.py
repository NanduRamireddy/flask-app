from flask import Flask, request, send_file, render_template, jsonify
import pandas as pd
import numpy as np
import random
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.table as tbl
import io

app = Flask(__name__)

def get_random_sample(data, min_samples=1, max_samples=None):
    if max_samples is None:
        max_samples = len(data)
    num_samples = random.randint(min_samples, max_samples)
    num_samples = min(num_samples, len(data))
    return data.sample(n=num_samples)

def compute_row_means(data):
    y_values = data.drop(columns=['x'])
    row_means = y_values.mean(axis=1)
    return row_means

def confidence_intervals(data, confidence_level=0.80):
    x_values = data['x']
    y_values = data.drop(columns=['x'])

    means = y_values.mean(axis=1)
    std_errors = y_values.std(axis=1, ddof=1) / np.sqrt(y_values.count(axis=1))
    degrees_of_freedom = y_values.count(axis=1) - 1

    t_scores = degrees_of_freedom.apply(lambda df: stats.t.ppf(1 - (1 - confidence_level) / 2, df))
    margins_of_error = t_scores * std_errors

    lower_bounds = means - margins_of_error
    upper_bounds = means + margins_of_error

    result = pd.DataFrame({
        'x': x_values,
        'mean': means,
        'lower_bound': lower_bounds,
        'upper_bound': upper_bounds
    })

    return result

def plot_with_confidence_intervals_sorted(data, confidence_level=0.80):
    ci_data = confidence_intervals(data, confidence_level)
    
    ci_data_sorted = ci_data.sort_values(by='x')
    
    x = ci_data_sorted['x']
    mean = ci_data_sorted['mean']
    lower_bound = ci_data_sorted['lower_bound']
    upper_bound = ci_data_sorted['upper_bound']
    
    plt.figure(figsize=(10, 6))
    
    # Plot data points
    for col in data.columns:
        if col != 'x':
            plt.scatter(data['x'], data[col], alpha=0.5)
    
    # Plot mean
    plt.plot(x, mean, label='Mean', color='blue')
    
    # Plot confidence intervals
    plt.fill_between(x, lower_bound, upper_bound, color='blue', alpha=0.2, label='Confidence Interval')
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Plot of Data Points, Mean, and Confidence Intervals with Sorted Data')
    plt.legend()
    plt.grid(True)
    
    plot_buffer = io.BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)
    plt.close()
    
    return plot_buffer, ci_data_sorted

def plot_ci_table(ci_data):
    fig, ax = plt.subplots(figsize=(10, 4))  
    ax.axis('off')

    # Convert DataFrame to list of lists for the table
    table_data = [ci_data.columns.tolist()] + ci_data.values.tolist()
    table = tbl.table(ax, cellText=table_data, colLabels=None, loc='center', cellLoc='center', colWidths=[0.2]*len(ci_data.columns))
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  

    table_buffer = io.BytesIO()
    plt.savefig(table_buffer, format='png')
    table_buffer.seek(0)
    plt.close()

    return table_buffer

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        data = pd.read_csv(file)
        data_filled_zero = data.fillna(0)
        random_sample = get_random_sample(data_filled_zero, min_samples=1, max_samples=10)
        plot_buffer, ci_data = plot_with_confidence_intervals_sorted(random_sample)
        table_buffer = plot_ci_table(ci_data)

        plot_path = '/tmp/plot.png'
        table_path = '/tmp/table.png'

        with open(plot_path, 'wb') as f:
            f.write(plot_buffer.getvalue())
        
        with open(table_path, 'wb') as f:
            f.write(table_buffer.getvalue())

        return jsonify({
            "plot_url": "/plot.png",
            "table_url": "/table.png",
            "means_and_cis": ci_data.to_dict(orient='records')
        })

@app.route('/plot.png')
def get_plot():
    return send_file('/tmp/plot.png', mimetype='image/png')

@app.route('/table.png')
def get_table():
    return send_file('/tmp/table.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
