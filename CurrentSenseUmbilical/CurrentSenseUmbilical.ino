#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;


void setup(void) 
{
  Serial.begin(115200);
  while (!Serial) {
      // will pause Zero, Leonardo, etc until serial console opens
      delay(1);
  }

  uint32_t currentFrequency;
    
  //Serial.println("Umbilical Initialization!");
  
  // Initialize the INA219.
  // By default the initialization will use the largest range (32V, 2A).  However
  // you can call a setCalibration function to change this range (see comments).
  ina219.begin();
  // To use a slightly lower 32V, 1A range (higher precision on amps):
  ina219.setCalibration_32V_1A(); //expecting a max of 900mA
  // Or to use a lower 16V, 400mA range (higher precision on volts and amps):
  //ina219.setCalibration_16V_400mA();

  //Serial.println("Measuring voltage and current with INA219 ...");
}

void loop(void) 
{
  float shuntVoltage = 0;
  float busVoltage = 0;
  float current_mA = 0;
  float loadVoltage = 0;
  float power_mW = 0;

  shuntVoltage = ina219.getShuntVoltage_mV();
  busVoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadVoltage = busVoltage + (shuntVoltage / 1000);
  
  //Serial.print("Bus Voltage:   "); Serial.print(busVoltage); Serial.println(" V");
  //Serial.print("Shunt Voltage: "); Serial.print(shuntVoltage); Serial.println(" mV");
  //Serial.print("Load Voltage:  "); Serial.print(loadVoltage); Serial.println(" V");
  //Serial.print("Current:       "); Serial.print(current_mA); Serial.println(" mA");
  //Serial.print("Power:         "); Serial.print(power_mW); Serial.println(" mW");
  //Serial.println("");
  
  //String umbilical_packet = String(busVoltage)+','+String(shuntVoltage)+','+String(current_mA)+','+String(power_mW);
  String umbilical_packet = String(current_mA)+','+String(busVoltage);
  Serial.println(umbilical_packet);
  delay(250);
}
