#include <string.h> 
#include <AFMotor.h>
#define CW 2
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
String input, m5, m4, m3, m2;
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
int rate;

void setup() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  Serial.begin(9600);

  pinMode(CW, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){
    input = Serial.readStringUntil('\n');
    Serial.println(input);

    int commaIndex = input.indexOf(',');
    int secondCommaIndex = input.indexOf(',',commaIndex+1);
    int thirdCommaIndex = input.indexOf(',',secondCommaIndex+1);
    
    m5 = input.substring(0,commaIndex);
    m4  = input.substring(commaIndex+1, secondCommaIndex);
    m3  = input.substring(secondCommaIndex+1, thirdCommaIndex);
    m2 = input.substring(thirdCommaIndex+1);
    Serial.println(m5.toInt());
    if (m5.toInt() > 0){
      rate = 15000/270*(m5.toInt());
      Serial.println(rate);
//      move(motor4, false, rate, 200);
      Serial.println("yesss");
    }
    else
    {
      rate = -1*15000/270*(m5.toInt());
      Serial.println(rate);
//      move(motor4, true, rate, 200);
    }
  }
}

void move(AF_DCMotor motor_name, bool direction, int time, int speed){
  motor_name.setSpeed(speed);

  if (direction){
  motor_name.run(FORWARD);
  }
  else{
    motor_name.run(BACKWARD);
  }
  delay(time);
  motor_name.run(RELEASE);
}
