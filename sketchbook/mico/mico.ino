/* 
  Firmware for MicOS.
  by Diego de los Reyes Rodríguez <http://diegorys.es> 

  created on 9 Dec 2014
  modified on 22 Dec 2014
  by Diego de los Reyes Rodríguez.
  http://diegorys.es
*/

#include <Servo.h>

/** VARIABLES **/

Servo servoCam;      // create servo object to control the webcam

int posCam = 0;  //Position of the webcam
int pinLDR = A5; //LDR pin

/** FUNCTIONS ARDUINO **/

void setup() 
{ 
  Serial.begin(9600);         // initialize serial communication at 9600 bits per second.
  servoCam.attach(9);         // attaches the servo on pin 9 to the servo obj
  pinMode(pinLDR, INPUT);     // input sensor LDR
  moveCenter();               // initialize position
} 
 
void loop() 
{
  int command = -1;
  
  if (Serial.available() > 0) {
    // read the incoming byte:
    command = Serial.read();
    
    switch(command){
      case 'a':
        moveRight();
        break;
      case 'd':
        moveLeft();
        break;
      case 'x':
        moveCenter();
        break;
      case 'o':
        getLight();
        break;
      case 'p':
        getPosition();
        break;
      default:
        Serial.println("Error:Unknown command");
    }
  }
  delay(100);
}

/** ACTIONS **/

/**
 * Rotates the motor 30 degrees to the right.
 */
void moveRight(){
  posCam -= 30;
  rotate();
}

/**
 * Rotates the motor 30 degrees to the left.
 */
void moveLeft(){
  posCam += 30;
  rotate();
}

/**
 * Center the motor.
 */
void moveCenter(){
  posCam = 90;
  rotate();
}

/**
 * Gets the amount of light.
 */
void getLight(){
  int light = analogRead(pinLDR);
  Serial.print("Light:");
  Serial.println(light);
}

/**
 * Rotates the motor.
 */
void rotate(){
  if(posCam < 0) posCam = 0;
  else if(posCam > 179) posCam = 179;
  servoCam.write(posCam);
  getPosition();
}

/**
 * Gets the position of the motor.
 */
 void getPosition(){
  Serial.print("Cam:");
  Serial.println(posCam);
 }

