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
String finalString = "";
int M5_angle = 90;
float rate;

void setup() {
  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  Serial.begin(115200);
  inputString.reserve(200);

  pinMode(CW, OUTPUT);
}

void loop() {
  if (finalString == "start\n")
  {
      M5_angle = M5_angle-10;
      move(motor4, true, 824.8, 200); //10 degree
      //Serial.println("M5_angle");
      delay(1500);
   }
   else if(finalString == "found\n")
   {
      Serial.println(M5_angle);
      M5_angle = 90;
      finalString = "";
  }
  else if(finalString == "close\n")
  {
      digitalWrite(CW,HIGH);
      move(motor1, true, 1000, 255);
      finalString = "";  
  }
  else if(finalString != "")
  {
    
    int commaIndex = finalString.indexOf(',');
    int secondCommaIndex = finalString.indexOf(',',commaIndex+1);
    int thirdCommaIndex = finalString.indexOf(',',secondCommaIndex+1);
    
    m5 = finalString.substring(0,commaIndex);
    m4  = finalString.substring(commaIndex+1, secondCommaIndex);
    m3  = finalString.substring(secondCommaIndex+1, thirdCommaIndex);
    m2 = finalString.substring(thirdCommaIndex+1,(finalString.length())-2); 

    
    if (m5.toFloat() > 0){
      rate = 82.48*(m5.toFloat());
      move(motor4, false, rate, 200);
    }
    else
    {
      rate = -1*82.48*(m5.toFloat());
      move(motor4, true, rate, 200);
    }
    
    if (m4.toFloat() > 0){
      rate = 5000/90*(m4.toFloat());
      move(motor3, false, rate, 255);
    }
    else
    {
      rate = -1*5000/90*(m4.toFloat()); //11000
      move(motor3, true, rate, 255);
    }

    if (m3.toFloat() > 0){
      rate = 3600/90*(m3.toFloat());
      move(motor2, true, rate, 200);
    }
    else
    {
      rate = -1*7500/90*(m3.toFloat());
      move(motor2, false, rate, 200);
   }

     if (m2.toFloat() > 0){
      digitalWrite(CW,LOW);
      rate = 6300/120*(m2.toFloat());
      move(motor1, true, rate, 150);
    }
    else
    {
      digitalWrite(CW,LOW);
      rate = -1*7300/120*(m2.toFloat());
      move(motor1, false, rate, 150);
    }

    Serial.println("ki pu dire?");
    finalString = "";
  }
     

  if (M5_angle == -90)
  {   
    Serial.println("not found");
    M5_angle = 90;
  }
    
}

void move(AF_DCMotor motor_name, bool direction, float time, int speed){
  motor_name.setSpeed(speed);

  if (direction){
  motor_name.run(FORWARD);
  }
  else{
    motor_name.run(BACKWARD);
  }
  delay(time);
  motor_name.run(RELEASE);
  delay(500);
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
      finalString = inputString;
      inputString = "";
    }
  }
}
