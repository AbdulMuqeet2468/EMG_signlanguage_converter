#define BAUD_RATE 115200

// ADC pins
#define CH1 34
#define CH2 35
#define CH3 32
#define CH4 33

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  int ch1 = analogRead(CH1);
  int ch2 = analogRead(CH2);
  int ch3 = analogRead(CH3);
  int ch4 = analogRead(CH4);

  // Send: timestamp,ch1,ch2,ch3,ch4
  Serial.print(millis());
  Serial.print(",");

  Serial.print(ch1);
  Serial.print(",");

  Serial.print(ch2);
  Serial.print(",");

  Serial.print(ch3);
  Serial.print(",");

  Serial.println(ch4);

  delay(2);  // ~500 Hz
}
