from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime
import cv2
import numpy as np

# Initialiser le détecteur de visages de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

app = Flask(__name__)

# Chemin du dossier où les photos seront enregistrées
UPLOAD_FOLDER = './photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')
def detect_faces(frame, padding=50):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Recadrer chaque visage détecté
    for (x, y, w, h) in faces:
        # Ajouter du padding autour des coordonnées du visage
        x_pad = max(x - padding, 0)
        y_pad = max(y - padding, 0)
        w_pad = min(w + 2 * padding, frame.shape[1] - x_pad)
        h_pad = min(h + 2 * padding, frame.shape[0] - y_pad)
        # Recadrer le visage avec du padding
        cropped_face = frame[y_pad:y_pad+h_pad, x_pad:x_pad+w_pad]
        # Vous pouvez faire quelque chose avec le visage recadré ici
        # Par exemple, vous pouvez enregistrer chaque visage recadré dans une liste
        # Ou les traiter d'une autre manière
    return cropped_face

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
        # Lire l'image à l'aide de OpenCV
        nparr = np.frombuffer(photo_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # Détecter les visages dans l'image
        frame_with_faces = detect_faces(frame)
        # Générer un nom de fichier unique basé sur la date et l'heure actuelles
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        image_name = f"image_{timestamp}.jpg"
        # Enregistrer l'image dans le dossier de téléchargement
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
        cv2.imwrite(image_path, frame_with_faces)
        print("L'image a été enregistrée avec succès :", image_path)
        return jsonify({'success': True, 'message': 'Image sauvegardée avec succès.', 'image_path': image_path})
    else:
        print("Aucune image n'a été envoyée.")
        return jsonify({'success': False, 'message': 'Aucune image n\'a été envoyée.'})

if __name__ == '__main__':
    # Créer le dossier de téléchargement s'il n'existe pas
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # Lancer le serveur Flask
    app.run(debug=True)
