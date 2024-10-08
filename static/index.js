     // Déclarer les variables globales pour la vidéo et le canvas
     const video = document.getElementById('video');
     const canvas = document.getElementById('canvas');
     const context = canvas.getContext('2d');
     let captureButtonEnabled = true;

     // Fonction pour demander l'accès au port série
     async function getSerialPort() {
         try {
             // Demander à l'utilisateur de sélectionner un port série
             const ports = await navigator.serial.getPorts();
             const port = ports[0];
             // Ouvrir le port série
             await port.open({ baudRate: 9600 }); // Spécifier le débit en bauds (baudRate)

             // Créer un lecteur pour lire les données du port série
             const reader = port.readable.getReader();

             // Lire continuellement les données du port série
             while (true) {
                 const { value, done } = await reader.read();
                 if (done) {
                     console.log('Fin de la lecture du port série.');
                     break;
                 }
                 processData(new TextDecoder().decode(value));
             }

         } catch (error) {
             console.error('Erreur lors de l\'accès au port série :', error);
         }
     }
     async function requestSerialPort() {
         try {
             // Demander à l'utilisateur de sélectionner un port série
             const port = await navigator.serial.requestPort();
             // Ouvrir le port série
             await port.open({ baudRate: 9600 }); // Spécifier le débit en bauds (baudRate)

             // Créer un lecteur pour lire les données du port série
             const reader = port.readable.getReader();

             // Lire continuellement les données du port série
             while (true) {
                 const { value, done } = await reader.read();
                 if (done) {
                     console.log('Fin de la lecture du port série.');
                     break;
                 }
                 processData(new TextDecoder().decode(value));
             }

         } catch (error) {
             console.error('Erreur lors de l\'accès au port série :', error);
         }
     }
     window.onload = getSerialPort;

     // Fonction pour traiter les données reçues du port série
     function processData(data) {
         if(data == 8 && captureButtonEnabled) {
         console.log('Données reçues du port série :', data);
         capturePhoto();
     }
     }

     // Fonction pour capturer une photo
     function capturePhoto() {
         context.drawImage(video, 0, 0, canvas.width, canvas.height);
         var imageData = canvas.toDataURL('image/jpeg'); // Convertir en base64
         sendData(imageData); // Envoyer les données à la fonction sendData()
     }

     // Capture vidéo et envoi d'image
     navigator.mediaDevices.getUserMedia({ video: true })
         .then(function(stream) {
             video.srcObject = stream;
         })
         .catch(function(error) {
             console.log("Error accessing the webcam: " + error.message);
         });

     document.getElementById('capture').addEventListener('click', function() {
         capturePhoto();
     });

     // Ajouter un écouteur d'événements au bouton pour demander l'accès au port série
     document.getElementById('connectButton').addEventListener('click', requestSerialPort);
// Fonction pour envoyer les données de l'image au serveur
function sendData(imageData) {
 fetch('/process_image', {
     method: 'POST',
     body: JSON.stringify({ image: imageData }),
     headers: {
         'Content-Type': 'application/json'
     }
 })
 .then(response => {
     return response.json(); // Convertir la réponse en JSON
 })
 .then(data => {
     if (data.success) {
         console.log('Image uploaded successfully');
         sendToSerialPort(1);
// Faire une requête GET pour récupérer la dernière photo
fetch('/latest_photo')
 .then(response => response.blob())
 .then(blob => {
     // Créer un objet URL pour l'image
     const imageUrl = URL.createObjectURL(blob);
     // Créer une balise img pour afficher l'image
     const imageElement = document.createElement('img');
     // Mettre à jour l'attribut src avec l'URL de l'image
     imageElement.src = imageUrl;
     // Ajouter l'élément image à la page

     const successMessage = document.createElement('div');
     const compteur = document.createElement('h1');
     compteur.id = "compteur";
     successMessage.style.position = 'absolute';
     successMessage.style.width = '100%';
     successMessage.style.height = '100vh';
     const h1Element = document.createElement('h1');
     h1Element.textContent = 'Vous êtes maintenant sur le carrousel!';
     h1Element.style.marginTop= '20vh';
     h1Element.style.textAlign = 'center';
     successMessage.appendChild(h1Element);
     successMessage.appendChild(compteur);

     // Ajouter du style à la balise
     successMessage.style.backgroundColor = '#28a745';
     successMessage.style.color = '#fff';
     successMessage.style.padding = '10px';
     successMessage.style.borderRadius = '5px';
     // Ajouter la balise au corps du document
     document.body.appendChild(successMessage);
     const image = document.body.appendChild(imageElement);
     image.style.position = 'absolute';
     image.style.width= '400px'
     captureButtonEnabled = false
     afficherCompteur(8); // Démarre un compteur de 10 secondes

      //Supprimer la balise après 5 secondes
    setTimeout(function() {
         successMessage.remove();
         image.remove();
         captureButtonEnabled = true
         sendToSerialPort(5);

     }, 8000);
 })
     } else {
         console.error('Error uploading image:');
         sendToSerialPort(2)
         // Créer une balise HTML pour afficher le message d'erreur
         const errorMessage = document.createElement('div');
         errorMessage.style.position = 'absolute';
         errorMessage.style.width = '100%';
         errorMessage.style.height = '100vh';
         const h1Element = document.createElement('h1');
         h1Element.textContent = 'Aucun visage détecté!';
         h1Element.style.marginTop= '40vh';
         h1Element.style.textAlign = 'center';
         errorMessage.appendChild(h1Element);
         
         // Ajouter du style à la balise
         errorMessage.style.backgroundColor = '#dc3545';
         errorMessage.style.color = '#fff';
         errorMessage.style.padding = '10px';
         errorMessage.style.borderRadius = '5px';
         errorMessage.style.marginTop = '10px';
         // Ajouter la balise au corps du document
         document.body.appendChild(errorMessage);
         setTimeout(function() {
             errorMessage.remove();
         }, 3000);
     }
 })
 .catch(error => {
     console.error('Error uploading image:', error);
 });
}

     var videoConstraints = {
         video: {
             whiteBalanceMode: 'manual',  // Vous pouvez ajuster ce paramètre
             brightness: 2,              // Vous pouvez ajuster ce paramètre
             contrast: 1,                // Vous pouvez ajuster ce paramètre
             // Ajoutez d'autres paramètres si nécessaire
         }
     };

     navigator.mediaDevices.getUserMedia(videoConstraints)
         .then(function (stream) {
             var videoElement = document.getElementById('video');
             videoElement.srcObject = stream;
         })
         .catch(function (error) {
             console.error('Error accessing webcam:', error);
         });

// Fonction pour envoyer des données à un port série déjà ouvert
async function sendToSerialPort(message) {
 try {
 // Obtenir la liste des ports série déjà autorisés
 const ports = await navigator.serial.getPorts();

 // Vérifier s'il existe des ports série déjà autorisés
 if (ports && ports.length > 0) {
     const port = ports[0];

     // Créer un transformateur de texte en flux d'octets
     const textEncoder = new TextEncoderStream();

     // Créer un flux d'écriture
     const writableStreamClosed = textEncoder.readable.pipeTo(port.writable);

     // Obtenir le writer
     const writer = textEncoder.writable.getWriter();

     // Écrire le message dans le flux
     await writer.write(message + "\n"); // Ajouter le caractère de saut de ligne à la fin

     console.log("Message envoyé : " + message);

     // Fermer le writer
     await writer.close();
 }
} catch (error) {
 console.error("Erreur lors de l'envoi du message :", error);
}
}
function afficherCompteur(secondeRestantes) {
    // Sélection de l'élément HTML où afficher le compteur
    var compteurElement = document.getElementById('compteur');

    // Affichage du compteur
    compteurElement.innerText = "Prochaine prise de photo  dans " + secondeRestantes + " sec";

    // Décrémentation du compteur chaque seconde
    var compteurInterval = setInterval(function() {
        secondeRestantes--;

        // Mise à jour du texte du compteur
        compteurElement.innerText = "Prochaine photo disponible dans " + secondeRestantes + " secondes";

        // Arrêt du compteur quand il atteint zéro
        if (secondeRestantes <= 0) {
            clearInterval(compteurInterval);
            compteurElement.innerText = "La photo est maintenant disponible !";
            // Ajoutez ici le code à exécuter une fois que le compteur atteint zéro
        }
    }, 1000); // Actualisation du compteur toutes les 1000 millisecondes (1 seconde)
}