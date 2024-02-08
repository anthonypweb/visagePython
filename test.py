import cv2

# Charger le classificateur de cascade Haar pour la détection de visage
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Fonction pour détecter les visages et dessiner un carré autour de chaque visage détecté
def detect_faces(frame):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Détecter les visages dans l'image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Dessiner un carré autour de chaque visage détecté
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return frame

# Fonction pour afficher le menu de sélection de la webcam
def select_webcam():
    # Obtenir le nombre de webcams disponibles
    num_webcams = cv2.VideoCapture(0).get(cv2.CAP_PROP_FRAME_COUNT)
    print("Nombre de webcams disponibles :", int(num_webcams))
    # Afficher le menu de sélection de la webcam
    print("Sélectionnez la webcam :")
    for i in range(int(num_webcams)):
        print(f"{i}: Webcam {i}")
    # Demander à l'utilisateur de sélectionner une webcam
    selected_webcam = input("Entrez le numéro de la webcam sélectionnée : ")
    return int(selected_webcam)

# Sélectionner la webcam
webcam_index = select_webcam()

# Capturer la vidéo depuis la webcam sélectionnée
cap = cv2.VideoCapture(webcam_index)

while True:
    # Lire une frame depuis la webcam
    ret, frame = cap.read()
    # Si la frame est correctement lue
    if ret:
        # Détecter les visages et dessiner des carrés autour d'eux
        frame_with_faces = detect_faces(frame)
        # Afficher la frame avec les visages détectés
        cv2.imshow('Face Detection', frame_with_faces)
    # Quitter la boucle si la touche 'q' est pressée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libérer la capture de la webcam et fermer les fenêtres
cap.release()
cv2.destroyAllWindows()
