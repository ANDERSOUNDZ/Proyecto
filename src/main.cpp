#include <Arduino.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUM_LEDS 6

Adafruit_NeoPixel strip(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

String input = "";

void procesarEstado(String data);

void setup() {
  Serial.begin(9600);
  strip.begin();
  strip.show();

  for (int i = 0; i < NUM_LEDS; i++) {
    strip.setPixelColor(i, strip.Color(0, 255, 0));
  }
  strip.show();
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n') {
      procesarEstado(input);
      input = "";
    } else {
      input += c;
    }
  }
}

void procesarEstado(String data) {
  if (data.length() != NUM_LEDS) return;

  strip.clear();

  for (int i = 0; i < NUM_LEDS; i++) {
    if (data[i] == '0') {
      strip.setPixelColor(i, strip.Color(0, 255, 0));
    } else if (data[i] == '1') {
      strip.setPixelColor(i, strip.Color(255, 0, 0));
    } else if (data[i] == '2') {
      strip.setPixelColor(i, strip.Color(0, 0, 0));
    }
  }

  strip.show();
}