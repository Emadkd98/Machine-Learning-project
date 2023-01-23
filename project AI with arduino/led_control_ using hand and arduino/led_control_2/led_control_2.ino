const int redPin = 6;
int incomingByte;
void setup()
{
Serial.begin(9600);




pinMode(redPin, OUTPUT);
}
void loop()
{
while (Serial.available()>0){
incomingByte = Serial.read();

if (incomingByte == 'H')
  {
   int red = Serial.parseInt();
   red = constrain(red, 5, 255);
   analogWrite(redPin, red);
   //Serial.print(red);
  }
      if (incomingByte == 'L'){
     
      digitalWrite(redPin,LOW);
  }

}
}
