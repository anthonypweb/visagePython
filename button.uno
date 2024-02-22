#include <FastLED.h>

#define NUM_LEDS 80    // Nombre total de LED dans votre bande
#define DATA_PIN 6      // Broche de données connectée à la bande de LED
#define BRIGHTNESS 100 // Luminosité des LED (0-255)
#define COLOR_WHITE CRGB(255, 255, 255) // Couleur blanche
#define COLOR_GREEN CRGB(0, 255, 0)   // Couleur jaune
#define COLOR_RED CRGB(255, 0, 0)        // Couleur rouge
#define COLOR_YELLOW CRGB(255, 255, 0)        // Couleur rouge

#define COLOR_BLACK CRGB(0, 0, 0)        // Couleur rouge

CRGB leds[NUM_LEDS]; // Déclaration du tableau de LED

int lastCommand = -1; // Variable pour stocker la dernière commande reçue (-1 = inconnue)

void setup() {
  pinMode(4, INPUT_PULLUP);

  Serial.begin(9600); // Configuration du débit du moniteur série (Arduino)
  delay(100);
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  // Définir la couleur par défaut des LED en blanc
  setColor(COLOR_WHITE);
}

void loop() {
    int sensorVal = digitalRead(4);

  if (sensorVal == LOW) {
    setColor(COLOR_YELLOW); // Changer la couleur en rouge pour les valeurs de 6 à 9

    Serial.print(8);
  delay(2000);                // waits for a second
  } 

  if (Serial.available() > 0) {
    int receivedCommand = Serial.parseInt(); // Lire la commande reçue en tant qu'entier
    
    // Comparer la commande reçue avec la dernière commande
    if (receivedCommand != lastCommand) {
      Serial.println(String(receivedCommand));
      // Appel de la fonction pour contrôler les lumières
      controlerLumieres(receivedCommand);
      
      // Mettre à jour la dernière commande
      lastCommand = receivedCommand;
    }
  }
}

// Fonction pour contrôler les lumières en fonction de la commande reçue
void controlerLumieres(int commande) {
  if (commande == 1) {
    setColor(COLOR_GREEN); // Changer la couleur en jaune pour les valeurs de 1 à 5
    
  } else if (commande == 2) {
    setColor(COLOR_RED); // Changer la couleur en rouge pour les valeurs de 6 à 9
      delay(500);
    setColor(COLOR_BLACK); // Changer la couleur en rouge pour les valeurs de 6 à 9
      delay(500);
    setColor(COLOR_RED); // Changer la couleur en rouge pour les valeurs de 6 à 9
      delay(2000);

  } else {
        setColor(COLOR_WHITE); // Éteindre les LED

    // Autres traitements en fonction de la commande reçue
  }
}

void setColor(CRGB color) {
  fill_solid(leds, NUM_LEDS, color);
  FastLED.show();
}
