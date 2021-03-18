#include <AFMotor.h>
#include <string.h> 
#define CW 2
AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete

void setup() 
{

  motor1.run(RELEASE);
  motor2.run(RELEASE);
  motor3.run(RELEASE);
  motor4.run(RELEASE);
  // initialize serial:
  Serial.begin(9600);
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);

  
   pinMode(CW, OUTPUT); 
  //Set initial speed of the motor & stop
 
}
void loop() 
{
  // print the string when a newline arrives:
  if (stringComplete) {
    int commaIndex = inputString.indexOf(',');
    int secondCommaIndex = inputString.indexOf(',',commaIndex+1);

    String Name = inputString.substring(0,commaIndex);
    String time  = inputString.substring(secondCommaIndex +1);
    bool direction;
    if(inputString.substring(commaIndex+1,secondCommaIndex) == "0")
    {
      direction = false;
    }
    else
    {
      direction = true;
    }
    Serial.println(Name);
    Serial.println(direction);
    Serial.println(time.toInt());
    if (Name == "1"){
      digitalWrite(CW,HIGH);
      move(motor1, direction, time.toInt(),255);
    }

    if (Name == "2"){
      digitalWrite(CW,LOW);
      move(motor1, direction, time.toInt(),150);
    }
    if (Name == "3"){
      move(motor2, direction, time.toInt(),200);
    }

    if (Name == "4"){ 
      move(motor3, direction, time.toInt(),255);
    }

    if (Name == "5"){
      move(motor4, direction, time.toInt(),200);
    }
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
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
