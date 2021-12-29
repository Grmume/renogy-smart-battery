'''
Renogy smart battery RS485 readout.
This script features:
  - Detection of slave address
  - Readout of register data

The intention is to use it as a starting point to figure out the meaning of the register data of the renogy LIFEPO smart batteries.
'''
import minimalmodbus
import serial.tools.list_ports
import argparse
import time

REGISTERS = {
    # Abbreviations:
    # -ov: overvoltage
    # -uv: unvervoltage
    
    # Cell information
    'cell_count':{               'address':0x1388, 'length':1, 'type':'uint',   'scaling':'identical',        'unit':''},
    'cellvoltage_1':{            'address':0x1389, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_2':{            'address':0x138a, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_3':{            'address':0x138b, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'cellvoltage_4':{            'address':0x138c, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'unknown_0x138d':{           'address':0x138d, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x138e':{           'address':0x138e, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x138f':{           'address':0x138f, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1390':{           'address':0x1390, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'celltemp_1':{               'address':0x139a, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_2':{               'address':0x139b, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_3':{               'address':0x139c, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'celltemp_4':{               'address':0x139d, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'unknown_0x1391':{           'address':0x1391, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1392':{           'address':0x1392, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1393':{           'address':0x1393, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1394':{           'address':0x1394, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1395':{           'address':0x1395, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1396':{           'address':0x1396, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1397':{           'address':0x1397, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1398':{           'address':0x1398, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1399':{           'address':0x1399, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x139e':{           'address':0x139e, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x139f':{           'address':0x139f, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a0':{           'address':0x13a0, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a1':{           'address':0x13a1, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a2':{           'address':0x13a2, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a3':{           'address':0x13a3, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a4':{           'address':0x13a4, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a5':{           'address':0x13a5, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a6':{           'address':0x13a6, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a7':{           'address':0x13a7, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a8':{           'address':0x13a8, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13a9':{           'address':0x13a9, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ab':{           'address':0x13ab, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},

    # Battery information
    'unknown_0x13ac':{           'address':0x13ac, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ad':{           'address':0x13ad, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ae':{           'address':0x13ae, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13af':{           'address':0x13af, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13b0':{           'address':0x13b0, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13b1':{           'address':0x13b1, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'current':{                  'address':0x13b2, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': 'A'},
    'voltage':{                  'address':0x13b3, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit':'V'},
    'remaining_charge':{         'address':0x13b4, 'length':2, 'type':'uint',   'scaling':'linear(0.001,0)',  'unit':'Ah'},
    'capacity':{                 'address':0x13b6, 'length':2, 'type':'uint',   'scaling':'linear(0.001,0)',  'unit':'Ah'},
    'unknown_0x13b7':{           'address':0x13b7, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13b8':{           'address':0x13b8, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},

    # Battery Thresholds
    'ov_protect':{               'address':0x13b9, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'uv_protect':{               'address':0x13ba, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'unknown_0x13bb':{           'address':0x13bb, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13bc':{           'address':0x13bc, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ec':{           'address':0x13ec, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ed':{           'address':0x13ed, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ee':{           'address':0x13ee, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    
    # Mystery Block 1
    'heater_level':{             'address':0x13ef, 'length':1, 'type':'uint',   'scaling':'linear(0.3922,0)', 'unit': '%'},
    'unknown_0x13f0':{           'address':0x13f0, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13f1':{           'address':0x13f1, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13f2':{           'address':0x13f2, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13f3':{           'address':0x13f3, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13f4':{           'address':0x13f4, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13f5':{           'address':0x13f5, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},

    # General information
    'serial':{                   'address':0x13f6, 'length':8, 'type':'string', 'scaling':'identical',        'unit': ''},
    'unknown_0x13fe':{           'address':0x13fe, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x13ff':{           'address':0x13ff, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1400':{           'address':0x1400, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1401':{           'address':0x1401, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'model':{                    'address':0x1402, 'length':8, 'type':'string', 'scaling':'identical',        'unit': ''},
    'firmware_version':{         'address':0x140a, 'length':2, 'type':'string', 'scaling':'identical',        'unit': ''},
    'manufacturer':{             'address':0x140c, 'length':4, 'type':'string', 'scaling':'identical',        'unit': ''},

    # Mystery Block 2 
    'unknown_0x1410':{           'address':0x1410, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1411':{           'address':0x1411, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1412':{           'address':0x1412, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1413':{           'address':0x1413, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1414':{           'address':0x1414, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1415':{           'address':0x1415, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},

    # Cell voltage protection
    'cell_ov_protect':{          'address':0x1450, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'cell_ov_recover':{          'address':0x1451, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'cell_uv_warn':{             'address':0x1452, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},
    'cell_uv_protect':{          'address':0x1453, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'V'},

    # Temperature protection
    'hightemp_protect':{         'address':0x1454, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'hightemp_warn?':{           'address':0x1455, 'length':1, 'type':'sint',   'scaling':'linear(0.1,0)',    'unit': '°C'},
    'hightemp_hysteresis':{      'address':0x1456, 'length':1, 'type':'uint',   'scaling':'linear(0.1,0)',    'unit': 'K'},

    # Mystery Block 3 
    'unknown_0x1457':{           'address':0x1457, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1458':{           'address':0x1458, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1459':{           'address':0x1459, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x145a':{           'address':0x145a, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x145b':{           'address':0x145b, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x145c':{           'address':0x145c, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x145d':{           'address':0x145d, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x145e':{           'address':0x145e, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x145f':{           'address':0x145f, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1460':{           'address':0x1460, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1461':{           'address':0x1461, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1462':{           'address':0x1462, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1463':{           'address':0x1463, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1464':{           'address':0x1464, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1465':{           'address':0x1465, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'unknown_0x1466':{           'address':0x1466, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
    'device_address':{           'address':0x1467, 'length':1, 'type':'uint',   'scaling':'identical',        'unit': ''},
}

def linear(factor, offset, input):
    return (input*factor)+offset

def read_register(instrument, reg: dict):
    raw_data = instrument.read_registers(reg['address'], reg['length'])
    raw_bytes = []
    idx = 0
    for uint16 in raw_data:
        raw_bytes.append(uint16 >> 8)
        raw_bytes.append(uint16 & 0x00ff)
        idx = idx + 2
    value = 0
    
    # Calculate raw value
    if reg['type'] == 'sint':
        # Check if sign bit is set
        if raw_data[0] > 32768:
            negative = True
        else:
            negative = False

        value = 0
        for shift in range(0, reg['length']):
            shift_amount = (reg['length'] - shift - 1)*16
            value = value | (raw_data[shift] << shift_amount)

        if negative:
            value = value - 32768

    elif reg['type'] == 'uint':
        value = 0
        for shift in range(0, reg['length']):
            shift_amount = (reg['length'] - shift - 1)*16
            value = value | (raw_data[shift] << shift_amount)
    elif reg['type'] == 'string':
        string = ''
        for reg in raw_data:
            string = string+chr(reg >> 8)
            string = string+chr(reg & 0xff)
        # If the string does not match the register length exactly it will contain a termination character (0x00)
        # Truncate the string if required:
        string = string.split("\x00")[0]
        return {'value':string, 'raw_bytes': raw_bytes}
    else:
        print(f'Warning: Unsupported register type {reg["type"]}.')
        return None
    
    # Apply scaling
    if reg['scaling']=='identical':
        return {'value':value, 'raw_bytes': raw_bytes}
    else:
        # Add paramter for the input value
        head, _sep, tail = partitioned = reg['scaling'].rpartition(')')
        fnc_call = head+', value)'
        scaled = eval(fnc_call)
        return {'value':scaled, 'raw_bytes': raw_bytes}

def scan_addresses(instrument):
    TEST_REGISTER = {'address':0x13b3, 'length':1, 'type':'uint',   'scaling':'identical'}
    instrument.serial.timeout = 0.1
    for address in range(0x01, 0xf8):
        instrument.address = address
        try:
            read_register(instrument, TEST_REGISTER)
            return address
        except:
            pass           
    
    return None

def read_registers(instrument):
    global REGISTERS
    values = {}
    for reg in REGISTERS:
        try:
            values[reg] = read_register(instrument, REGISTERS[reg])
        except Exception as inst:
            print(f'Error: Exception reading register {reg}: {inst}.')    
    return values

def print_values_loop(instrument):
    global REGISTERS

    while(True):
        values = read_registers(instrument)
        print('')
        print('Register'.ljust(25)+'Address'.ljust(10)+'Value'.ljust(20).ljust(10)+'Binary'.ljust(35))
        print('----------------------------------------------------------------------------------------------')
        for key in values:
            register_name = key.ljust(25)
            address_string = "{0:#0{1}x}".format(REGISTERS[key]['address'],6).ljust(10)
            if isinstance(values[key]['value'], float):
                value_number_string = "{:.2f}".format(values[key]['value'])
            else:
                value_number_string = str(values[key]['value'])
            value_string = (value_number_string+' '+REGISTERS[key]['unit']).ljust(20)
            binary_string = (' '.join(format(byte, '08b') for byte in values[key]['raw_bytes'])).ljust(35)
            if len(binary_string) > 35:
                binary_string = binary_string[:32]+'...'
            print(register_name+address_string+value_string+binary_string)
        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renogy Smart Battery RS485 readout.')
    parser.add_argument('--device', default='/dev/ttyUSB0', help='Serial device to use for RS485 communication')
    parser.add_argument('--address', default=0xf7, type=lambda x: int(x,0), help='Slave address of the RS485 device')
    parser.add_argument('--scan-addresses', default=False, help='Determine slave address by brute force.', action='store_true')
    parser.add_argument('--list-devices', default=False, help='List serial devices', action='store_true')
    args = parser.parse_args()

    if args.list_devices:
        print('device'.ljust(20)+'manufacturer'.ljust(25)+'product'.ljust(25)+'description')
        print('---------------------------------------------------------------------------------------')
        for port in serial.tools.list_ports.comports():
            dev = port.device or 'n/a'
            manf = port.manufacturer or 'n/a'
            prod = port.product or 'n/a'
            desc = port.description or 'n/a'
            print(dev.ljust(20)+manf.ljust(25)+prod.ljust(25)+desc)
    else:
        # 247 (0xf7) is the default address. If another renogy device is connected it might have reprogrammed the address to another value.
        instrument = minimalmodbus.Instrument(args.device, slaveaddress=247)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 0.2

        if args.scan_addresses:
            print('Scanning addresses...')
            slave_address = scan_addresses(instrument)

            if(slave_address != None):
                print(f'Slave address: {hex(slave_address)}')
            else:
                print('Error: could not determine slave address.')
        else:
            slave_address = args.address

        if slave_address != None:
            instrument.address = slave_address
            instrument.serial.timeout = 0.2
            print_values_loop(instrument)


