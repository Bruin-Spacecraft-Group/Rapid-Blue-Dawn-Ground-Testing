void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);     // Set baud rate to 115200 (Default serial configureation is 8N1).
  Serial.setTimeout(20);    // Time out if nothing is read

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(millis());
  
}
