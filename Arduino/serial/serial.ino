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

    
    if (m5.toInt() > 0){
      rate = 15000/270*(m5.toInt());
      Serial.println(rate);
      move(motor4, false, rate, 200);
      Serial.println("yesss");
    }
    else
    {
      rate = -1*15000/270*(m5.toInt());
      Serial.println(rate);
      move(motor4, true, rate, 200);
    }
    
    if (m4.toInt() > 0){
      rate = 5000/90*(m4.toInt());
      Serial.println(rate);
      move(motor3, true, rate, 255);
      Serial.println("yesss");
    }
    else
    {
      rate = -1*11000/90*(m4.toInt());
      Serial.println(rate);
      move(motor3, false, rate, 255);
    }

    if (m3.toInt() > 0){
      rate = 3600/90*(m3.toInt());
      Serial.println(rate);
      move(motor2, true, rate, 200);
      Serial.println("yesss");
    }
    else
    {
      rate = -1*7500/90*(m3.toInt());
      Serial.println(rate);
      move(motor2, false, rate, 200);
   }

     if (m2.toInt() > 0){
      digitalWrite(CW,LOW);
      rate = 6300/120*(m2.toInt());
      Serial.println(rate);
      move(motor1, true, rate, 150);
      Serial.println("yesss");
    }
    else
    {
      digitalWrite(CW,LOW);
      rate = -1*7300/120*(m2.toInt());
      Serial.println(rate);
      move(motor1, false, rate, 150);
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
