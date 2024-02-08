from flask import Flask, jsonify, render_template, request
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('webcam_capture.html')

from flask import Flask, request, jsonify
import base64
import os

app.config['UPLOAD_FOLDER'] = 'uploads'  # Dossier de téléchargement, assurez-vous qu'il existe

# Créez le dossier de téléchargement s'il n'existe pas
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'image' in request.json:
        print("Une image a été envoyée.")
        # Récupérer les données de l'image depuis la requête JSON
        image_data = request.json['image']
        # Extraire les données base64 de l'image
        _, base64_data = image_data.split(',')
        # Décoder les données base64 en bytes
        photo_bytes = base64.b64decode(base64_data)
        # Enregistrer l'image dans le dossier de téléchargement
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'captured_image.jpg')
        with open(image_path, 'wb') as f:
            f.write(photo_bytes)
        print("L'image a été enregistrée avec succès :", image_path)
        return jsonify({'success': True, 'message': 'Image sauvegardée avec succès.', 'image_path': image_path})
    else:
        print("Aucune image n'a été envoyée.")
        return jsonify({'success': False, 'message': 'Aucune image n\'a été envoyée.'})

if __name__ == '__main__':
    app.run(debug=True)
