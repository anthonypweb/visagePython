from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
import cv2
import os
from datetime import datetime

app = Flask(__name__)

# Chemin du dossier où les photos seront enregistrées
UPLOAD_FOLDER = './photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Définir la taille maximale du fichier (10 Mo)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Définir le chemin du modèle de détection de visage
face_cascade_path = "haarcascade_frontalface_default.xml"

# Chemin du fichier XML de détection de visage

# Vérifier si le fichier existe
if os.path.isfile(face_cascade_path):
    print("Le fichier XML de détection de visage existe.")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + face_cascade_path)

else:
    print("Le fichier XML de détection de visage n'existe pas ou n'est pas accessible.")

# Fonction pour détourer le visage dans l'image
def crop_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        # Agrandir le rectangle de détection pour capturer une zone plus grande autour du visage
        margin = 70  # Vous pouvez ajuster cette valeur selon vos besoins
        x = max(0, x - margin)
        y = max(0, y - margin)
        w = min(image.shape[1], w + 2 * margin)
        h = min(image.shape[0], h + 2 * margin)
        cropped_face = image[y:y+h, x:x+w]
        return cropped_face
    else:
        print("Aucun visage détecté !")
        return None

# Page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour capturer une photo
@app.route('/process_image', methods=['POST'])
def capture():
    # Accéder à la webcam
    cap = cv2.VideoCapture(0)

    # Lire une image depuis la webcam
    ret, frame = cap.read()

    # Détourer le visage dans l'image
    cropped_face = crop_face(frame)
    print("Résolution de l'image capturée :", frame.shape)

    # Vérifier si le visage est détecté
    if cropped_face is not None:
        # Générer un nom de fichier unique basé sur la date et l'heure actuelles
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        filename = f"photo_{timestamp}.png"  # Enregistrer au format PNG pour la transparence

        # Enregistrer l'image dans le dossier de téléchargement
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv2.imwrite(filepath, cropped_face)
        print("Image enregistrée avec succès :", filepath)
        return jsonify({'success': True})
    else:
        print("Aucun visage n'a été détecté dans l'image capturée.")
        return jsonify({'success': False, 'message': 'Aucun visage détecté dans l\'image capturée'})

    # Libérer la webcam
    cap.release()

# Route pour accéder aux photos téléchargées
@app.route('/photos/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Créer le dossier de téléchargement s'il n'existe pas
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Lancer le serveur Flask
    app.run(debug=True, port=5001, ssl_context=('cert.pem', 'key.pem'))
