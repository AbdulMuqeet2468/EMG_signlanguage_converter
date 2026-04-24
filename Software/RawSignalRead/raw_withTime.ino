//  raw signal with timestamp
#define BAUD_RATE 115200
#define INPUT_PIN A0   // ESP8266 has only A0

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  int raw = analogRead(INPUT_PIN);

  // send: timestamp, raw value
  Serial.print(millis());
  Serial.print(",");
  Serial.println(raw);

  delay(2);  // ~500 Hz sampling
}
