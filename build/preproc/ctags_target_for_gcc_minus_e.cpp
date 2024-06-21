# 1 "C:\\Users\\jorge\\Desktop\\own_deej\\own_deej.ino"
# 2 "C:\\Users\\jorge\\Desktop\\own_deej\\own_deej.ino" 2
# 3 "C:\\Users\\jorge\\Desktop\\own_deej\\own_deej.ino" 2
# 4 "C:\\Users\\jorge\\Desktop\\own_deej\\own_deej.ino" 2






# 9 "C:\\Users\\jorge\\Desktop\\own_deej\\own_deej.ino"
//JEJE
byte cross [8] = {
  0,
  17,
  10,
  4,
  10,
  17,
  0,
  0
};

byte on [8] = {
  0,
  4,
  14,
  21,
  17,
  14,
  0,
  0
};

LiquidCrystal_I2C lcd(0x27, 16, 2);

String song = "";
unsigned long previousMillis = 0;

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
      song = Serial.readStringUntil('\n');
      showMessage(song);
    }
  }
}

void showMessage(String message)
{
  String title;
  String artist;
  int index = message.indexOf('*'); // Encontrar la posición del carácter '*'

  if (index != -1)
  { // Si se encuentra el carácter '*'
    title = message.substring(0, index); // Subcadena desde el inicio hasta el carácter '*'
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
    lcd.setCursor(15,1);
    lcd.write(byte(0));
  }
  else if(artist == "Justin Mylo")
  {
    lcd.print("Justin Mylo");
    lcd.createChar(0, on);
    lcd.setCursor(12,1);
    lcd.write(byte(0));
  }
  else
  {
    lcd.print(artist);
  }
}
