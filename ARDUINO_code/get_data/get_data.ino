//Program to get the data from serial
#include <stdio.h>
#include <stdlib.h>

void setup() 
{
  Serial.begin(9600);
  Serial.println("Serial OK");  
}

void loop()
{
//Get the serial command:
int SerialCommand=0;
  if(Serial.available()>0)
  {
    SerialCommand=Serial.parseInt();
    delay(200);
    Serial.println("\n*************\n");
    Serial.print("Here the command: ");
    Serial.println(SerialCommand);
    Serial.println("\n*************\n");
  }
  if(Serial.available()==0)
  {
    Serial.print("\nWaiting for command...\n");
  }
  delay(1000);

}
