#define MAXBUFSIZE      200     // Maximum buffer size for serial packet.

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);     // Set baud rate to 115200 (Default serial configureation is 8N1).
  Serial.setTimeout(20);    // Time out if nothing is read

}

void loop() {
  // put your main code here, to run repeatedly:
  char buf [MAXBUFSIZE] = {0};
  
  int bytes_read = Serial.readBytes(buf, MAXBUFSIZE);
  if(bytes_read) {
    buf[bytes_read] = '\0';

    Serial.println(buf);
  }
  
}
