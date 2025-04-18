import logging

def _get_regs(bus: object, i2c_address: int, start_reg: int, length: int) -> list[int]|None:
    """Get raw registers content."""
    regs = None
    regs = bus.read_i2c_block_data(i2c_address, start_reg, length)
    logging.debug(f"Got registers '{regs}'")
    return regs

def _get_ascii(bus: object, i2c_address: int, start_reg: int, length: int) -> str|None:
    """Convert registers to ASCII"""
    regs = _get_regs(bus, i2c_address, start_reg, length)
    if regs == None:
        return None
    text = "".join([chr(r) for r in regs]).strip()
    logging.debug(f"Got text '{text}'")
    return text

def _get_data(bus: object, i2c_address: int, start_reg: int, length: int) -> int|None:
    """Convert registers to numeric data (int)."""
    regs = _get_regs(bus, i2c_address, start_reg, length)
    if regs == None:
        return None
    data = 0
    for reg in regs:
        data = (data << 8) + reg
    logging.debug(f"Got data '{data}'")
    return data

def get_error_status(bus: object, i2c_address: int) -> dict[str]|None:
    """Get a list of error flags."""
    start_reg = 0x00
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    errors = []
    opt = {0: "low_voltage",
           1: "measurement_timeout",
           2: "abnormal_signal_level",
           3: "unknown",
           4: "unknown",
           5: "unknown",
           6: "unknown",
           7: "scale_factor_error",
           8: "fatal_error",
           9: "i2c_error",
           10: "algorithm_error",
           11: "calibration_error",
           12: "self_diag_error",
           13: "out_of_range",
           14: "memory_error",
           15: "no_measurements_completed"}
    for k, v in opt.items():
        if data & (1 << k):
            errors.append(v)
    logging.debug(f"Got errors flags '{errors}'")
    return errors

def get_calibration_status(bus: object, i2c_address: int) -> str|None:
    """Get the calibration status."""
    start_reg = 0x81
    length = 1
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    opt = {0: "unknown",
           1: "unknown",
           2: "factory",
           3: "abc",
           4: "target",
           5: "background",
           6: "zero",
           7: "unknown"}
    data = opt[data]
    logging.debug(f"Got calibration status '{data}'")
    return data

def get_measurement_mode(bus: object, i2c_address: int) -> str|None:
    """Get the measurement mode."""
    start_reg = 0x95
    length = 1
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    opt = {0: "continuous",
           1: "single"}
    data = opt[data]
    logging.debug(f"Got measurement mode '{data}'")
    return data

def get_firmware_type(bus: object, i2c_address: int) -> int|None:
    """Get the firmware type."""
    start_reg = 0x2f
    length = 1
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    logging.debug(f"Got firmware type '{data}'")
    return data

def get_firmware_revision(bus: object, i2c_address: int) -> str|None:
    """Get the firmware revision."""
    start_reg = 0x38
    length = 1
    major = _get_data(bus, i2c_address, start_reg, length)
    start_reg = 0x39
    length = 1
    minor = _get_data(bus, i2c_address, start_reg, length)
    if major == None or minor == None:
        return None
    data = ".".join([str(major), str(minor)])
    logging.debug(f"Got firmware revision '{data}'")
    return data

def get_sensor_id(bus: object, i2c_address: int) -> int|None:
    """Get the sensor ID."""
    start_reg = 0x3a
    length = 4
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    logging.debug(f"Got sensor id '{data}'")
    return data

def get_product_code(bus: object, i2c_address: int) -> str|None:
    """Get the product code."""
    start_reg = 0x70
    length = 16
    text = _get_ascii(bus, i2c_address, start_reg, length)
    logging.debug(f"Got product code'{text}'")
    return text

def get_co2_filtered_compensated(bus: object, i2c_address: int) -> int|None:
    """Get the filtered and compensated CO2 measurement."""
    start_reg = 0x06
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data
    logging.debug(f"Got filtered and compensated co2 metric: '{metric} ppm'")
    return metric

def get_co2(bus: object, i2c_address: int) -> int|None:
    """ Alias for 'get_co2_filtered_compensated'
    Get the filtered and compensated CO2 measurement.
    
    """
    return get_co2_filtered_compensated(bus, i2c_address)

def get_co2_unfiltered_compensated(bus: object, i2c_address: int) -> int|None:
    """Get the unfiltered but compensated CO2 measurement."""
    start_reg = 0x10
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data
    logging.debug(f"Got unfiltered and compensated co2 metric: '{metric} ppm'")
    return metric

def get_co2_filtered_uncompensated(bus: object, i2c_address: int) -> int|None:
    """Get the filtered but uncompensated CO2 measurement."""
    start_reg = 0x12
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data
    logging.debug(f"Got filtered and uncompensated co2 metric: '{metric} ppm'")
    return metric

def get_co2_unfiltered_uncompensated(bus: object, i2c_address: int) -> int|None:
    """Get the unfiltered and uncompensated CO2 measurement."""
    start_reg = 0x14
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data
    logging.debug(f"Got unfiltered and uncompensated co2 metric: '{metric} ppm'")
    return metric

def get_temp(bus: object, i2c_address: int) -> float|None:
    """Get the temperature measurement used for compensation."""
    start_reg = 0x08
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data / 100
    logging.debug(f"Got temperature metric: '{metric} °C'")
    return metric

def get_press(bus: object, i2c_address: int) -> float|None:
    """Get the pressure setting used for compensation."""
    start_reg = 0xdc
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data / 10
    logging.debug(f"Got temperature metric: '{metric} hPa'")
    return metric

def get_cycle_count(bus: object, i2c_address: int) -> int|None:
    """Get the measurement cycle count (0..255)."""
    start_reg = 0x0d
    length = 1
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data
    logging.debug(f"Got cycle count: '{metric}'")
    return metric

def get_cycle_time(bus: object, i2c_address: int) -> int|None:
    """Get the time following the last measurement (in s)."""
    start_reg = 0x0e
    length = 2
    data = _get_data(bus, i2c_address, start_reg, length)
    if data == None:
        return None
    metric = data * 2
    logging.debug(f"Got cycle time: '{metric} s'")
    return metric
