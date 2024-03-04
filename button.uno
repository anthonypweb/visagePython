#include <FastLED.h>

#define NUM_LEDS 80                      // Nombre total de LED dans votre bande
#define DATA_PIN 7                       // Broche de données connectée à la bande de LED
#define BRIGHTNESS 100                   // Luminosité des LED (0-255)
#define COLOR_WHITE CRGB(255, 255, 255)  // Couleur blanche
#define COLOR_GREEN CRGB(0, 255, 0)      // Couleur verte
#define COLOR_RED CRGB(255, 0, 0)        // Couleur rouge
#define COLOR_YELLOW CRGB(255, 255, 0)   // Couleur jaune
#define COLOR_BLACK CRGB(0, 0, 0)        // Couleur rouge

CRGB leds[NUM_LEDS];   // Déclaration du tableau de LED
int lastCommand = -1;  // Variable pour stocker la dernière commande reçue (-1 = inconnue)

void setup() {
  Serial.begin(9600);        // Démarre la connexion série
  pinMode(4, INPUT_PULLUP);  // Configure la broche 4 en entrée avec résistance de tirage
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.setBrightness(BRIGHTNESS);
  setColor(COLOR_WHITE);  // Définit la couleur par défaut des LED en blanc
}

void loop() {
  int sensorVal = digitalRead(4);  // Lit la valeur du bouton poussoir

  if (Serial.available() > 0) {
    int receivedCommand = Serial.parseInt();  // Lit la commande reçue en tant qu'entier

    // Vérifie si la commande reçue est différente de la dernière commande
    if (receivedCommand != lastCommand) {
      // Appelle la fonction pour contrôler les LED
      if (receivedCommand == 1) {
        setColor(COLOR_GREEN);
      } else if (receivedCommand == 2) {
        setColor(COLOR_RED);
        delay(500);
        setColor(COLOR_BLACK);
        delay(500);

        setColor(COLOR_RED);
        delay(500);
        setColor(COLOR_BLACK);
        delay(500);

        setColor(COLOR_WHITE);
      } else if (receivedCommand == 5){
        setColor(COLOR_WHITE);
      }
      // Met à jour la dernière commande
      lastCommand = receivedCommand;
    }
  }

  // Vérifie si le bouton poussoir est enfoncé
  if (sensorVal == LOW) {
    Serial.println(8);  // Envoie la commande 8 via la connexion série
    delay(500);         // Attend un moment
  }
}

void setColor(CRGB color) {
  fill_solid(leds, NUM_LEDS, color);  // Remplit le tableau de LED avec la couleur spécifiée
  FastLED.show();                     // Affiche les changements sur les LED
}
