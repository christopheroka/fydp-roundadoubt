int NORTH_OUTPUT_PIN = 10;
int EAST_OUTPUT_PIN = 9;
int SOUTH_OUTPUT_PIN = 8;
int WEST_OUTPUT_PIN = 11;
int NORTH_INPUT_PIN = 4;
int EAST_INPUT_PIN = 3;
int SOUTH_INPUT_PIN = 5;
int WEST_INPUT_PIN = 2;

void setup() {
  // Set pin as output pin
  pinMode(NORTH_OUTPUT_PIN, OUTPUT);
  pinMode(EAST_OUTPUT_PIN, OUTPUT);
  pinMode(SOUTH_OUTPUT_PIN, OUTPUT);
  pinMode(WEST_OUTPUT_PIN, OUTPUT);
  pinMode(NORTH_INPUT_PIN, INPUT);
  pinMode(EAST_INPUT_PIN, INPUT);
  pinMode(SOUTH_INPUT_PIN, INPUT);
  pinMode(WEST_INPUT_PIN, INPUT);

  // Initialize Serial monitor
  Serial.begin(9600);
}

void loop() {
  Serial.println(digitalRead(SOUTH_INPUT_PIN));
  // Listen for digital inputs
  if (digitalRead(NORTH_INPUT_PIN) == HIGH) {
	digitalWrite(NORTH_OUTPUT_PIN, HIGH);
  } else {
	digitalWrite(NORTH_OUTPUT_PIN, LOW);
  }
  if (digitalRead(EAST_INPUT_PIN) == HIGH) {
	digitalWrite(EAST_OUTPUT_PIN, HIGH);
  }  {
	digitalWrite(EAST_OUTPUT_PIN, LOW);
  } 
  if (digitalRead(SOUTH_INPUT_PIN) == HIGH) {
	digitalWrite(SOUTH_OUTPUT_PIN, HIGH);
  } else {
	digitalWrite(SOUTH_OUTPUT_PIN, LOW);
  }
  if (digitalRead(WEST_INPUT_PIN) == HIGH) {
	digitalWrite(WEST_OUTPUT_PIN, HIGH);
  }  else {
	digitalWrite(WEST_OUTPUT_PIN, LOW);
  }  
}
