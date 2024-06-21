#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>

#define LCD_ADDRESS 0x27
#define LCD_COLUMNS 16
#define LCD_ROWS 2

// JEJE
byte cross[8] = {
    B00000,
    B10001,
    B01010,
    B00100,
    B01010,
    B10001,
    B00000,
    B00000};

byte on[8] = {
    B00000,
    B00100,
    B01110,
    B10101,
    B10001,
    B01110,
    B00000,
    B00000};

byte alien[8] = {
    B00000,
    B01110,
    B11111,
    B10101,
    B01110,
    B00100,
    B00000,
    B00000};

LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLUMNS, LCD_ROWS);

String song = "";
unsigned long interval = 7000; // Tiempo hasta que se apaga la retroiluminación
unsigned long lastTime = 0;
bool lcdOn = true;

void setup()
{
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  lcd.clear();
}

void loop()
{
  if (Serial.available() > 0)
  {
    if (Serial.read() == '*')
    {
      String song = Serial.readStringUntil('\n');
      showMessage(song);
      lastTime = millis(); // Actualizar el tiempo de la última interacción
      if (!lcdOn) {
        lcdOn = true;
        lcd.backlight(); // Encender la retroiluminación
      }
    }
  }

  // Verificar si ha pasado el tiempo de inactividad
  if (lcdOn && (millis() - lastTime >= interval)) {
    lcd.noBacklight(); // Apagar la retroiluminación
    lcdOn = false;
  }
}

void showMessage(String message)
{
  String title;
  String artist;
  int index = message.indexOf('*'); // Encontrar la posición del carácter '*'

  if (index != -1)
  {                                        // Si se encuentra el carácter '*'
    title = message.substring(0, index);   // Subcadena desde el inicio hasta el carácter '*'
    artist = message.substring(index + 1); // Subcadena desde después del carácter '*' hasta el final
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(title);
  lcd.setCursor(0, 1);

  if (artist == "Martin Garrix")
  {
    lcd.print("Martin Garrix +");
    lcd.createChar(0, cross);
    lcd.setCursor(15, 1);
    lcd.write(byte(0));
  }
  else if (artist == "Justin Mylo")
  {
    lcd.print("Justin Mylo");
    lcd.createChar(0, on);
    lcd.setCursor(12, 1);
    lcd.write(byte(0));
  }
  else if (artist == "AREA21")
  {
    lcd.print("AREA21");
    lcd.createChar(0, alien);
    lcd.setCursor(7, 1);
    lcd.write(byte(0));
  }
  else
  {
    lcd.print(artist);
  }
}
