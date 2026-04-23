//  single channel
#define SAMPLE_RATE 500
#define BAUD_RATE 115200
#define INPUT_PIN A0

float smoothed = 0;   // for envelope

void setup() {
  Serial.begin(BAUD_RATE);
}

void loop() {
  static unsigned long past = 0;
  unsigned long present = micros();
  unsigned long interval = present - past;
  past = present;

  static long timer = 0;
  timer -= interval;

  if (timer < 0) {
    timer += 1000000 / SAMPLE_RATE;

    int raw = analogRead(INPUT_PIN);

    // Step 1: Remove baseline (center around 0)
    int centered = raw - 575; //575 is not always constant, need to change depending on the output. Still working on it 

    // Step 2: Rectify (make all values positive)
    int rectified = abs(centered);

    // Step 3: Smooth (low-pass filter / envelope)
    smoothed = 0.9 * smoothed + 0.1 * rectified;

    // Output all for debugging
    Serial.print(raw);
    Serial.print(",");
    Serial.print(centered);
    Serial.print(",");
    Serial.print(rectified);
    Serial.print(",");
    Serial.println(smoothed);
  }
}
