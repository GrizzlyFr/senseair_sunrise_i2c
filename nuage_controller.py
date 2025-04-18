#!/usr/bin/env python3
"""Example of script to read data from the Senseair Sunrise CO2 sensor

"""

import os
import sys
import logging
from datetime import datetime
from time import sleep
import smbus2

import sunrise


LOGGING_LEVEL = logging.INFO
LOGGING_FILENAME = "sunrise.log"
LOGGING_FORMAT = "%(asctime)s [%(levelname)s]: %(message)s"
LOGGING_FOLDER = "local_files"
I2C_BUS_NUMBER =                   1  # On RPi use "sudo i2c-detect -y 1" to check bus id and sensor response
SUNRISE_SENSOR_ADDRESS =           0x68
MAIN_LOOP_NOMINAL_DURATION =       60  # in seconds


def pause(duration:int|float) -> None:
    """ Pause function allowing ctrl+c interrupts"""
    logging.debug(f"Pausing for {duration} s")
    q, r = divmod(duration, 1)
    q = int(q)
    for i in range(q):
        sleep(1)
    sleep(r)

def print_all_data_from_sunrise(bus: object) -> None:
    """Read all available data from the Sunrise sensor"""
    bus = bus
    add = SUNRISE_SENSOR_ADDRESS
    logging.info(f"Error statuses: {sunrise.get_error_status(bus, add)}")
    logging.info(f"Calibration status: {sunrise.get_calibration_status(bus, add)}")
    logging.info(f"Measurement mode: {sunrise.get_measurement_mode(bus, add)}")
    logging.info(f"Firmware type: {sunrise.get_firmware_type(bus, add)}")
    logging.info(f"Firmware revision: {sunrise.get_firmware_revision(bus, add)}")
    logging.info(f"Sensor ID: {sunrise.get_sensor_id(bus, add)}")
    logging.info(f"Product code: {sunrise.get_product_code(bus, add)}")
    logging.info(f"CO2 measure: {sunrise.get_co2_filtered_compensated(bus, add)} ppm")
    logging.info(f"Unfiltered CO2 measure: {sunrise.get_co2_unfiltered_compensated(bus, add)} ppm")
    logging.info(f"Uncompensated CO2 measure: {sunrise.get_co2_filtered_uncompensated(bus, add)} ppm")
    logging.info(f"Raw CO2 measure: {sunrise.get_co2_unfiltered_uncompensated(bus, add)} ppm")
    logging.info(f"Temperature measure: {sunrise.get_temp(bus, add):.02}°C")
    logging.info(f"Pressure setting: {sunrise.get_press(bus, add):.01} hPa")
    logging.info(f"Cycle counts: {sunrise.get_cycle_count(bus, add)}")
    logging.info(f"Cycle time: {sunrise.get_cycle_time(bus, add)} s")


if __name__ == "__main__":
    
    ### Init logging

    if not os.path.exists(LOGGING_FOLDER):
        os.mkdir(LOGGING_FOLDER)
    logging.basicConfig(
        level=LOGGING_LEVEL,
        format=LOGGING_FORMAT,
        handlers=[
            logging.FileHandler(os.path.join(LOGGING_FOLDER,
                                             LOGGING_FILENAME),),
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Init bus
    logging.info(f"Initializing IC2 bus {I2C_BUS_NUMBER}")
    try:
        bus = smbus2.SMBus(I2C_BUS_NUMBER)
    except Exception as e:
        logging.critical(f"Could not initialize IC2 bus {I2C_BUS_NUMBER}; exiting")
        raise e
    
    # Main loop
    logging.info(f"Entering main loop (interval between measurments: {MAIN_LOOP_NOMINAL_DURATION} s)")
    try:
        while True:
            start_time = datetime.now()
            logging.info("Getting measurements from sensor")
            try:
                print_all_data_from_sunrise(bus)
            except Exception as e:
                logging.critical(f"Could not read Sunrise sensor on address {SUNRISE_SENSOR_ADDRESS}; exiting")
                raise e
            end_time = datetime.now()
            elapsed = (end_time - start_time).seconds
            pause(max(elapsed, MAIN_LOOP_NOMINAL_DURATION))
                
    except KeyboardInterrupt:
        logging.info("Ending main loop on user request; exiting")
        sys.exit()
    except Exception as e:
        logging.critical(f"Received error ({e}); exiting")
        raise e
