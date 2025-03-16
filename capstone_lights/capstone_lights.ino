int FLOOR_LIGHT_PIN = 2;
int SIGN_STRAIGHT_OUTPUT_PIN = 3;
int SIGN_LEFT_OUTPUT_PIN = 4;
int SIGN_RIGHT_OUTPUT_PIN = 5;
int SIGN_STRAIGHT_INPUT_PIN = 6;
int SIGN_LEFT_INPUT_PIN = 7;
int SIGN_RIGHT_INPUT_PIN = 8;
bool floorLightIsOn = false;
bool straightLightIsOn = false;
bool leftLightIsOn = false;
bool rightLightIsOn = false;

void setup() {
  // Set pin as output pin
  pinMode(FLOOR_LIGHT_PIN, OUTPUT);
  pinMode(SIGN_STRAIGHT_OUTPUT_PIN, OUTPUT);
  pinMode(SIGN_LEFT_OUTPUT_PIN, OUTPUT);
  pinMode(SIGN_RIGHT_OUTPUT_PIN, OUTPUT);
  pinMode(SIGN_STRAIGHT_INPUT_PIN, INPUT);
  pinMode(SIGN_LEFT_INPUT_PIN, INPUT);
  pinMode(SIGN_RIGHT_INPUT_PIN, INPUT);

  // Initialize Serial monitor
  Serial.begin(9600);
}

void loop() {
  // Listen for digital inputs
  if (digitalRead(SIGN_STRAIGHT_INPUT_PIN) == HIGH && straightLightIsOn == false) {
    turnSignOn(SIGN_STRAIGHT_OUTPUT_PIN);
  } else if (digitalRead(SIGN_STRAIGHT_INPUT_PIN) == LOW && straightLightIsOn == true) {
    turnSignOff(SIGN_STRAIGHT_OUTPUT_PIN);
  } else if (digitalRead(SIGN_LEFT_INPUT_PIN) == HIGH && leftLightIsOn == false) {
    turnSignOn(SIGN_LEFT_OUTPUT_PIN);
  } else if (digitalRead(SIGN_LEFT_INPUT_PIN) == LOW && leftLightIsOn == true) {
    turnSignOff(SIGN_LEFT_OUTPUT_PIN);
  } else if (digitalRead(SIGN_RIGHT_INPUT_PIN) == HIGH && rightLightIsOn == false) {
    turnSignOn(SIGN_RIGHT_OUTPUT_PIN);
  } else if (digitalRead(SIGN_RIGHT_INPUT_PIN) == LOW && rightLightIsOn == true) {
    turnSignOff(SIGN_RIGHT_OUTPUT_PIN);
  }

  // Listen for Serial input
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    Serial.println(input);

    if (input.equals("FL on")) {
      turnFloorLightOn();
    } else if (input.equals("FL off")) {
      turnFloorLightOff();
    } else if (input.equals("FL toggle")) {
      toggleFloorLight();
    } else if (input.equals("FL high")) {
      digitalWrite(FLOOR_LIGHT_PIN, HIGH);
    } else if (input.equals("FL low")) {
      digitalWrite(FLOOR_LIGHT_PIN, LOW);
    } else if (input.equals("SS on")) {
      turnSignOn(SIGN_STRAIGHT_OUTPUT_PIN);
    } else if (input.equals("SS off")) {
      turnSignOff(SIGN_STRAIGHT_OUTPUT_PIN);
    } else if (input.equals("SL on")) {
      turnSignOn(SIGN_LEFT_OUTPUT_PIN);
    } else if (input.equals("SL off")) {
      turnSignOff(SIGN_LEFT_OUTPUT_PIN);
    } else if (input.equals("SR on")) {
      turnSignOn(SIGN_RIGHT_OUTPUT_PIN);
    } else if (input.equals("SR off")) {
      turnSignOff(SIGN_RIGHT_OUTPUT_PIN);
    }else {
      Serial.println("Invalid command");
    }
  }
}

void toggleFloorLight() {
  if (floorLightIsOn) {
    turnFloorLightOff();
  } else {
    turnFloorLightOn();
  }
}

void turnFloorLightOn() {
  Serial.println("Light turning on");
  digitalWrite(FLOOR_LIGHT_PIN, HIGH);
  delay(100);
  digitalWrite(FLOOR_LIGHT_PIN, LOW);
  Serial.println("Light turned on");
  floorLightIsOn = true;
}

void turnFloorLightOff() {
  Serial.println("Light turning off");
  digitalWrite(FLOOR_LIGHT_PIN, HIGH);
  delay(2500);
  digitalWrite(FLOOR_LIGHT_PIN, LOW);
  Serial.println("Light turned off");
  floorLightIsOn = false;
}

void turnSignOn(int pin) {
  digitalWrite(pin, HIGH);
  Serial.print("Sign ");
  if (pin == SIGN_STRAIGHT_OUTPUT_PIN) {
    straightLightIsOn = true;
    Serial.print("straight");
  } else if (pin == SIGN_LEFT_OUTPUT_PIN) {
    Serial.print("left");
  } else if (pin == SIGN_RIGHT_OUTPUT_PIN) {
    Serial.print("right");
  }
  Serial.println(" turned on");
  if (pin == SIGN_STRAIGHT_OUTPUT_PIN) {
    turnFloorLightOn();
  }
}

void turnSignOff(int pin) {
  digitalWrite(pin, LOW);
    Serial.print("Sign ");
  if (pin == SIGN_STRAIGHT_OUTPUT_PIN) {
    Serial.print("straight");
    straightLightIsOn = false;
  } else if (pin == SIGN_LEFT_OUTPUT_PIN) {
    Serial.print("left");
  } else if (pin == SIGN_RIGHT_OUTPUT_PIN) {
    Serial.print("right");
  }
  Serial.println(" turned off");
  if (pin == SIGN_STRAIGHT_OUTPUT_PIN) {
    turnFloorLightOff();
  }
}
