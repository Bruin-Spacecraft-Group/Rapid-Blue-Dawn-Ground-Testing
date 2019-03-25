////////////////////////////////////////////////////////////////////////////////////////////////////
// nff-sample.ino
// Z Porter
// NanoRacks LLC
//
// Version 2.0
// Last Updated: 2-11-19
//
// Sample NanoLab payload for the NanoRacks Feather Frame that controls a series of LEDs to indicate 
// the current flight altitude. All example-specific code is clearly marked as such in the comments, 
// and should be removed or replaced by the relevant code for the developer's experiment. This 
// sample code is provided as-is by NanoRacks LLC to help customers develop flight code for their 
// Feather Frame payloads as quickly and easily as possible.
//
//                    *     .--.
//                         / /  `
//        +               | |
//               '         \ \__,
//           *          +   '--'  *
//               +   /\
//  +              .'  '.   *
//         *      /======\      +
//               ;:.  _   ;
//               |:. (_)  |
//               |:.  _   |
//     +         |:. (_)  |          *
//               ;:.      ;
//             .' \:.    / `.
//            / .-'':._.'`-. \
//            |/    /||\    \|
//          _..--"""````"""--.._
//    _.-'``                    ``'-._
//  -'                                '-
//
////////////////////////////////////////////////////////////////////////////////////////////////////


#define NUMDATAFIELDS   21      // Number of data fields for each packet.
#define MAXBUFSIZE      200     // Maximum buffer size for serial packet.
#define MAXFIELDSIZE    20      // Maximum size of any data field in the serial packet.

#define SUCCESS         0       // Success return code.
#define ERROR           -1      // Error return code.


////////////////////////////////////////////////////////////////////////////////////////////////////
// Example specific definition.
////////////////////////////////////////////////////////////////////////////////////////////////////
#define INC       (long) 50000  // Increment value of altitude for LED indicators.
////////////////////////////////////////////////////////////////////////////////////////////////////


// Struct to contain all of the NFF flight data in one object.
typedef struct NRdata
{
  char flight_event;
  double exptime;
  double altitude;
  double gps_altitude;
  double velocity[3];
  double acc_magnitude;
  double acceleration[3];
  double attitude[3];
  double angular_velocity[3];
  bool liftoff_warn;
  bool drogue_chute_warn;
  bool landing_warn;
  bool chute_fault_warn;
} NRdata;


int parse_serial_packet(const char* buf, NRdata* flight_data);


void setup()
{
  Serial.begin(115200);     // Set baud rate to 115200 (Default serial configureation is 8N1).
  Serial.setTimeout(20);    // Set timeout to 20ms (It may take up to 17ms for all of the data to
                            // transfer from the NFF, this ensures that enough time has passed
                            // to allow for a complete transfer before timing out).
  
////////////////////////////////////////////////////////////////////////////////////////////////////
// Example specific code to set up output pins for driving LEDs and set them to off.
////////////////////////////////////////////////////////////////////////////////////////////////////
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  digitalWrite(2, LOW);
  digitalWrite(3, LOW);
  digitalWrite(4, LOW);
  digitalWrite(5, LOW);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
////////////////////////////////////////////////////////////////////////////////////////////////////
  
}


void loop()
{
  char buffer[MAXBUFSIZE + 1] = {0};      // Buffer for receiving serial packets.
  int res;                                // Value for storing results of function calls.
  NRdata flight_info;                     // Struct for holding current flight data.

  // Initialize the struct and all its data to 0.
  memset(&flight_info, 0, sizeof(NRdata));

  // Loop forever on receiving data packets.
  while (1)
  {
    // Wait for serial input (Delay 1ms between polling serial port).
    while(!Serial.available())
    {
      delay(1);
    }

    // Read in the serial data up to the maximum serial packet size.
    res = Serial.readBytes(buffer, MAXBUFSIZE);

    // If no bytes are read then go back to waiting.
    if (res == 0)
    {
      continue;
    }

    // Null terminate the buffer (Possibly unnecessary).
    buffer[res] = 0;

    // Update the current flight info with the new data.
    res = parse_serial_packet(buffer, &flight_info);

    // If the program failed to parse the new data then go back to waiting.
    if (res != SUCCESS)
    {
      continue;
    }
    
    
////////////////////////////////////////////////////////////////////////////////////////////////////
// Example specific code for turning on an additional LED after each increment of altitude has been 
// reached. 
////////////////////////////////////////////////////////////////////////////////////////////////////
    (flight_info.altitude > INC) ? digitalWrite(2, HIGH) : digitalWrite(2, LOW);
    (flight_info.altitude > (INC * 2)) ? digitalWrite(3, HIGH) : digitalWrite(3, LOW);
    (flight_info.altitude > (INC * 3)) ? digitalWrite(4, HIGH) : digitalWrite(4, LOW);
    (flight_info.altitude > (INC * 4)) ? digitalWrite(5, HIGH) : digitalWrite(5, LOW);
    (flight_info.altitude > (INC * 5)) ? digitalWrite(6, HIGH) : digitalWrite(6, LOW);
    (flight_info.altitude > (INC * 6)) ? digitalWrite(7, HIGH) : digitalWrite(7, LOW);
////////////////////////////////////////////////////////////////////////////////////////////////////
    
  }
}


////////////////////////////////////////////////////////////////////////////////////////////////////
// parse_serial_packet:
//
// Takes in a buffer containing an NFF serial data packet and parses the information into the 
// provided data struct.
//
// buf            =   Buffer containing serial data packet.
// flight_data    =   Struct containing current flight data.
//
// return   =   SUCCESS or ERROR
//
////////////////////////////////////////////////////////////////////////////////////////////////////
int parse_serial_packet(const char* buf, NRdata* flight_data)
{
  int res;                          // Value for storing result of function calls.
  int fieldnum = 1;                 // Index for field number being parsed.
  int index = 0;                    // Index for position in serial buffer.
  char temp[MAXFIELDSIZE] = { 0 };  // Temporary buffer for holding a data field.

  // If the buffer is empty then return with an error.
  if (strlen(buf) == 0)
  {
    return (ERROR);
  }

  // Continue parsing until the end of the buffer is reached
  while (index < strlen(buf))
  {
    // Scan the buffer from the current index until the next comma and place the data into the 
    // temporary buffer.
    res = sscanf((buf + index), "%[^,]", temp);
   
    // If sscanf failed to get a parameter then the buffer was not in the correct format so the 
    // function should return with an error.
    if (res == 0)
    {
      return (ERROR);
    }

    // Increment the buffer index by the length of the data field plus the comma.
    index += (strlen(temp) + 1);

    // If the index for the field number is greater than the expected number of data fields then 
    // the buffer is not correctly formatted so the function should return with an error.
    if (fieldnum > NUMDATAFIELDS)
    {
      return (ERROR);
    }

    // Depending upon the current data field being parsed, convert the data in the temporary buffer 
    // to the appropriate format and store it in the flight data struct.
    switch (fieldnum)
    {
      case 1:
        // Flight event is just a single character.
        flight_data->flight_event = temp[0];
        break;
      case 2:
        // atof() converts a c-string to a floating point number.
        flight_data->exptime = atof(temp);
        break;
      case 3:
        flight_data->altitude = atof(temp);
        break;
      case 4:
        flight_data->gps_altitude = atof(temp);
        break;
      case 5:
        flight_data->velocity[0] = atof(temp);
        break;
      case 6:
        flight_data->velocity[1] = atof(temp);
        break;
      case 7:
        flight_data->velocity[2] = atof(temp);
        break;
      case 8:
        flight_data->acc_magnitude = atof(temp);
        break;
      case 9:
        flight_data->acceleration[0] = atof(temp);
        break;
      case 10:
        flight_data->acceleration[1] = atof(temp);
        break;
      case 11:
        flight_data->acceleration[2] = atof(temp);
        break;
      case 12:
        flight_data->attitude[0] = atof(temp);
        break;
      case 13:
        flight_data->attitude[1] = atof(temp);
        break;
      case 14:
        flight_data->attitude[2] = atof(temp);
        break;
      case 15:
        flight_data->angular_velocity[0] = atof(temp);
        break;
      case 16:
        flight_data->angular_velocity[1] = atof(temp);
        break;
      case 17:
        flight_data->angular_velocity[2] = atof(temp);
        break;
      case 18:
        // For the flight warnings, assign a boolean value of false for a 0 and true for anything 
        // else.
        flight_data->liftoff_warn = (temp[0] == '0') ? false : true;
        break;
      case 19:
        flight_data->drogue_chute_warn = (temp[0] == '0') ? false : true;
        break;
      case 20:
        flight_data->landing_warn = (temp[0] == '0') ? false : true;
        break;
      case 21:
        flight_data->chute_fault_warn = (temp[0] == '0') ? false : true;
        break;
    }

    // Increment the index for the current data field.
    fieldnum++;
  }

  // If the correct number of fields have been parsed then return with succcess, otherwise return 
  // with an error.
  if (fieldnum == (NUMDATAFIELDS + 1))
  {
    return (SUCCESS);
  }
  else
  {
    return (ERROR);
  }
}
