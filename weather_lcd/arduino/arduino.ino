#include <LiquidCrystal.h>

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 1);
  lcd.print("Waiting for weather data.");
}

void loop() {
  if (Serial.available()) {
    delay(100);
    lcd.clear();
    while (Serial.available() > 0) {
      lcd.write(Serial.read());
    }
  }
  for (int i = 0; i < 16; i ++) {
    delay(250);
    lcd.scrollDisplayLeft();
  }
}
