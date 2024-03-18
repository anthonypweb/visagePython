from flask import Flask, render_template, request, jsonify, send_from_directory, send_file
import os
import base64
from datetime import datetime
import cv2
import numpy as np

# Initialiser le détecteur de visages de OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

app = Flask(__name__)

# Chemin du dossier où les photos seront enregistrées
UPLOAD_FOLDER = '../Fun-Karousel-unity/Assets/photos'
#UPLOAD_FOLDER = './photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

def remove_background(image_path):
    # Charger l'image
    image = image_path
    
   # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Détection des visages dans l'image
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    # Créer un masque pour le visage
    mask = np.zeros_like(gray)
    
    # Détection du premier visage
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        
        # Calculer les nouvelles dimensions de l'image avec le padding
        new_width = w + 10 # 10 pixels de padding à gauche et à droite
        new_height = h + 10  # 10 pixels de padding en haut et en bas
        
        # Calculer les coordonnées du coin supérieur gauche du rectangle pour le padding
        x_padding = max(x - 0, 0)
        y_padding = max(y - 0, 0)
        
        # Dessiner un ovale autour du visage et le remplir avec le masque
        center = (x + w // 2, y + h // 2)
        axes = (w // 2, h * 2 // 3)  # Ajustement ici, 2/3 de la hauteur pour un axe vertical plus grand
        cv2.ellipse(mask, center, axes, 0, 0, 360, (255), -1)
        
        # Appliquer le masque à l'image
        result = cv2.bitwise_and(image, image, mask=mask)
        
        # Recadrer l'image avec le padding pour obtenir la nouvelle résolution
        result = result[y_padding:y_padding+new_height, x_padding:x_padding+new_width]
        
        return result
    
@app.route('/static/<path:filename>')
def serve_static(filename):
    # Récupérer le chemin absolu du fichier dans le dossier "static"
    return send_from_directory('static', filename)

@app.route('/latest_photo', methods=['GET'])
def get_latest_photo():
    # Récupérer la liste de tous les fichiers dans le dossier photo
    photo_files = os.listdir(app.config['UPLOAD_FOLDER'])
    # Trier la liste des fichiers par date de modification
    photo_files.sort(key=lambda x: os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    # Prendre le chemin de la première photo (la plus récente)
    latest_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_files[0])
    # Envoyer le fichier au client
    return send_file(latest_photo_path, mimetype='image/png')

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
        frame_with_faces = remove_background(frame)
        # Générer un nom de fichier unique basé sur la date et l'heure actuelles
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        image_name = f"image_{timestamp}.png"
        # Enregistrer l'image dans le dossier de téléchargement
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)

        if frame_with_faces is not None:
            cv2.imwrite(image_path, frame_with_faces)
            print("L'image a été enregistrée avec succès :")
            return jsonify({'success': True, 'message': 'Image sauvegardée avec succès.', 'image_path': image_path})
        else:
            print("L'image na pas fonctionné")
            return jsonify({'success': False, 'message': 'Aucun visage detecté'})


    else:
        print("Aucune image n'a été envoyée.")
        return jsonify({'success': False, 'message': 'Aucune image n\'a été envoyée.'})
        # Définition de la route pour servir les images
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('images', filename)

if __name__ == '__main__':
    # Créer le dossier de téléchargement s'il n'existe pas
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    # Lancer le serveur Flask

    app.run(debug=True)
