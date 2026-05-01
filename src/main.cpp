#include <Arduino.h> // <--- ESTA ES LA LÍNEA QUE TE FALTA

const int R = 9;
const int G = 10;
const int B = 11;

String estado = "free";

void actualizarLED(); // Prototipo de función (buena práctica en C++)

void setup() {
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
  Serial.begin(9600);
  actualizarLED();
}

void loop() {
  if (Serial.available() > 0) {
    estado = Serial.readStringUntil('\n');
    estado.trim();
    actualizarLED();
  }
}

void actualizarLED() {
  if (estado == "free") {
    digitalWrite(R, LOW);
    digitalWrite(G, HIGH);
    digitalWrite(B, LOW);
  } 
  else if (estado == "busy") {
    digitalWrite(R, HIGH);
    digitalWrite(G, LOW);
    digitalWrite(B, LOW);
  }
  else if (estado == "off") {
    digitalWrite(R, LOW);
    digitalWrite(G, LOW);
    digitalWrite(B, LOW);
  }
}