#include<Servo.h>

Servo servoX;
Servo servoY;
int x = 90;
int y = 90;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  servoX.attach(9);
  servoY.attach(10);
  servoX.write(x);
  servoY.write(y);
  delay(1000);
}
char input = ""; //serial input is stored in this variable
void loop() {
  // put your main code here, to run repeatedly:
 if(Serial.available()){ //checks if any data is in the serial buffer
  input = Serial.read(); //reads the data into a variable
  if(input == 'U'){
   servoY.write(y+1);    //adjusts the servo angle according to the input
   y += 1;               //updates the value of the angle
  }
  else if(input == 'D'){ 
   servoY.write(y-1);
   y -= 1;
  }
  else{
   servoY.write(y);
  } 
  if(input == 'L'){
  servoX.write(x-1);
  x -= 1;
  } else if(input == 'R'){
  servoX.write(x+1);
  x += 1;
  }
  else{
  servoX.write(x);
  }
  input = "";           //clears the variable
  }
 //process keeps repeating!! :)
}
