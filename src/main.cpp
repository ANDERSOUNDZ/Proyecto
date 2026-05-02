#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_LEDS 6

Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

String input = "";

// NUEVAS VARIABLES
int horasObjetivo[NUM_LEDS] = {0};
int horasActual[NUM_LEDS] = {0};

unsigned long lastUpdate = 0;
const int intervalo = 2000; // 2 segundos = 1 hora simulada

void procesarEstado(String data);
void actualizarLeds();
void estadoInicial();

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.clear();
  strip.show();

  estadoInicial();
}

void loop() {

  // Lectura serial
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      input.trim();
      procesarEstado(input);
      input = "";
    } else {
      input += c;
    }
  }

  // Simulación de tiempo SIN bloquear
  if (millis() - lastUpdate > intervalo) {
    lastUpdate = millis();

    for (int i = 0; i < NUM_LEDS; i++) {
      if (horasActual[i] < horasObjetivo[i]) {
        horasActual[i]++;
      }
    }

    actualizarLeds();
  }
}

// Estado inicial: TODO APAGADO
void estadoInicial() {
  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(0, 0, 0)); // ⚫
  }
  strip.show();
}

// Recibe horas desde Python (ej: "120031")
void procesarEstado(String data) {
  data.trim();

  Serial.print("Recibido: ");
  Serial.println(data);

  if (data.length() != NUM_LEDS) {
    Serial.println("Error longitud");
    return;
  }

  for (int i = 0; i < NUM_LEDS; i++) {
    horasObjetivo[i] = data[i] - '0'; // convertir char a int
    horasActual[i] = 0;               // reiniciar simulación
  }
}

// Lógica de colores + progreso
void actualizarLeds() {

  for (int i = 0; i < NUM_LEDS; i++) {

    int h = horasActual[i];

    if (h == 0) {
      // ⚫ libre
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
    else if (h <= 2) {
      // 🟢 verde con brillo progresivo
      int brillo = map(h, 1, 2, 50, 255);
      strip.setPixelColor(i, strip.Color(0, brillo, 0));
    }
    else if (h <= 4) {
      // 🟡 amarillo
      strip.setPixelColor(i, strip.Color(255, 150, 0));
    }
    else {
      // 🔴 rojo
      strip.setPixelColor(i, strip.Color(255, 0, 0));
    }
  }

  strip.show();
}