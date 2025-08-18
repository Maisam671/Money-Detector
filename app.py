from flask import Flask, render_template, request, send_from_directory
from ultralytics import YOLO
import os
import shutil
from pathlib import Path  # Add this import

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['RESULTS_FOLDER'] = 'static/results'

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)

# Load YOLO model (ensure 'best.pt' is in the root folder)
model = YOLO('best.pt')

@app.route('/', methods=['GET', 'POST'])
def index():
    results_img_path = None

    if request.method == 'POST':
        file = request.files['image']
        if file:
            # Save uploaded file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(upload_path)

            # Run YOLO detection — always save to a temp folder
            results = model.predict(
                source=upload_path,
                save=True,
                project='static/results',
                name='predict',  # YOLO will save inside static/results/predict
                exist_ok=True
            )

            # Find the saved image path
            saved_dir = Path(results[0].save_dir)  # Convert to Path object
            detected_files = list(saved_dir.glob("*.jpg"))

            if detected_files:
                detected_file = detected_files[0]
                # Move file to static/results root
                final_path = os.path.join(app.config['RESULTS_FOLDER'], detected_file.name)
                shutil.move(str(detected_file), final_path)

                results_img_path = f"results/{detected_file.name}"

    return render_template('index.html', results_img_path=results_img_path)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

