#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>

#define LCD_ADDRESS 0x27
#define LCD_COLUMNS 16
#define LCD_ROWS 2

LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLUMNS, LCD_ROWS);

String song = "";
bool newMessage = false;
unsigned long previousMillis = 0;
const long interval = 350;  // Intervalo de desplazamiento en milisegundos

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
}

void loop() {
  if (Serial.available() > 0) {
    if (Serial.read() == '*') {
      song = Serial.readStringUntil('\n');
      newMessage = true;
    }
  }
  if (newMessage) {
    lcd.clear();
    if (song.length() > LCD_COLUMNS) {
      scrollMessage(song);
    } else {
      lcd.setCursor(0, 0);
      lcd.print(song);
    }
    newMessage = false;
  }
}

void scrollMessage(String message) {
  message.erase(0, 1);
  int messageLength = message.length();
  int scrollPosition = 0;
  while (scrollPosition < messageLength - LCD_COLUMNS + 1) {
    lcd.setCursor(0, 0);
    lcd.print(message.substring(scrollPosition, scrollPosition + LCD_COLUMNS));
    scrollPosition++;
    delay(interval);
    if (Serial.available() > 0) {
      song = Serial.readStringUntil('\n');
      newMessage = true;
      break;
    }
  }
  lcd.setCursor(0, 0);
  lcd.print(message);
  if (!newMessage) {
    lcd.setCursor(0, 0);
    lcd.print(message.substring(scrollPosition, scrollPosition + LCD_COLUMNS));
  }
}
