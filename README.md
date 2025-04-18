# Senseair Sunrise CO2 sensor Python interface

Python functions to interface Senseair Sunrise CO2 sensors through I2C.

Do basic readings, no settings. The following parameters shall be set in test_sunrise.py before launch:
- I2C_BUS_NUMBER
- SUNRISE_SENSOR_ADDRESS (if different from the base I2C address)
- MAIN_LOOP_NOMINAL_DURATION (the script loop every 60 s by default)
