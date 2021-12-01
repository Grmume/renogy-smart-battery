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
import json
import binascii


REGISTERS = {
    'cell_count':{               'address':0x1388, 'length':1, 'type':'uint', 'scaling':'identical',      'unit':'cells'},
    'cellvoltage_1':{            'address':0x1389, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,2)',  'unit':'V'},
    'cellvoltage_2':{            'address':0x138a, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,2)',  'unit':'V'},
    'cellvoltage_3':{            'address':0x138b, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,2)',  'unit':'V'},
    'cellvoltage_4':{            'address':0x138c, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,2)',  'unit':'V'},
    'unknown_0x138d':{           'address':0x138d, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x138e':{           'address':0x138e, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x138f':{           'address':0x138f, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1390':{           'address':0x1390, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'celltemp_1':{               'address':0x139a, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'celltemp_2':{               'address':0x139b, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'celltemp_3':{               'address':0x139c, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'celltemp_4':{               'address':0x139d, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'unknown_0x1391':{           'address':0x1391, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1392':{           'address':0x1392, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1393':{           'address':0x1393, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1394':{           'address':0x1394, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1395':{           'address':0x1395, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1396':{           'address':0x1396, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1397':{           'address':0x1397, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1398':{           'address':0x1398, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1399':{           'address':0x1399, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x139e':{           'address':0x139e, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x139f':{           'address':0x139f, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a0':{           'address':0x13a0, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a1':{           'address':0x13a1, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a2':{           'address':0x13a2, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a3':{           'address':0x13a3, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a4':{           'address':0x13a4, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a5':{           'address':0x13a5, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a6':{           'address':0x13a6, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a7':{           'address':0x13a7, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a8':{           'address':0x13a8, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13a9':{           'address':0x13a9, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ab':{           'address':0x13ab, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ac':{           'address':0x13ac, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ad':{           'address':0x13ad, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ae':{           'address':0x13ae, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13af':{           'address':0x13af, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13b0':{           'address':0x13b0, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13b1':{           'address':0x13b1, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'current':{                  'address':0x13b2, 'length':1, 'type':'sint', 'scaling':'linear(0.1,0,2)', 'unit': 'A'},
    'voltage':{                  'address':0x13b3, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,2)',  'unit':'V'},
    'remaining_charge':{         'address':0x13b4, 'length':2, 'type':'uint', 'scaling':'linear(0.001,0,2)','unit':'Ah'},
    'charge_capacity':{          'address':0x13b6, 'length':2, 'type':'uint', 'scaling':'linear(0.001,0,-1)','unit':'Ah'},
    'unknown_0x13b7':{           'address':0x13b7, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13b8':{           'address':0x13b8, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'maximum_voltage?':{           'address':0x13b9, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,1)', 'unit': 'V'},
    'minimum_voltage?':{           'address':0x13ba, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,1)', 'unit': 'V'},
    'unknown_0x13bb':{           'address':0x13bb, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13bc':{           'address':0x13bc, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ec':{           'address':0x13ec, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ed':{           'address':0x13ed, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ee':{           'address':0x13ee, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'heater_level':{             'address':0x13ef, 'length':1, 'type':'uint', 'scaling':'linear(1,0,0)', 'unit': '%'},
    'unknown_0x13f0':{           'address':0x13f0, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13f1':{           'address':0x13f1, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13f2':{           'address':0x13f2, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13f3':{           'address':0x13f3, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13f4':{           'address':0x13f4, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13f5':{           'address':0x13f5, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'serial':{                   'address':0x13f6, 'length':8, 'type':'uint', 'scaling':'ascii(0)',  'unit': ''},
    'unknown_0x13fe':{           'address':0x13fe, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x13ff':{           'address':0x13ff, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1400':{           'address':0x1400, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1401':{           'address':0x1401, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'model':{                    'address':0x1402, 'length':8, 'type':'uint', 'scaling':'ascii(0)', 'unit': ''},
    'firmware_version':{           'address':0x140a, 'length':2, 'type':'uint', 'scaling':'ascii(0)', 'unit': ''},
    'manufacturer':{             'address':0x140c, 'length':4, 'type':'uint', 'scaling':'ascii(0)', 'unit': ''},
    'unknown_0x1410':{           'address':0x1410, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1411':{           'address':0x1411, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1412':{           'address':0x1412, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1413':{           'address':0x1413, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1414':{           'address':0x1414, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1415':{           'address':0x1415, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1450':{           'address':0x1450, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1451':{           'address':0x1451, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1452':{           'address':0x1452, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1453':{           'address':0x1453, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1454':{           'address':0x1454, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1455':{           'address':0x1455, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1456':{           'address':0x1456, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1457':{           'address':0x1457, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1458':{           'address':0x1458, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1459':{           'address':0x1459, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x145a':{           'address':0x145a, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x145b':{           'address':0x145b, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x145c':{           'address':0x145c, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x145d':{           'address':0x145d, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x145e':{           'address':0x145e, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x145f':{           'address':0x145f, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1460':{           'address':0x1460, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1461':{           'address':0x1461, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1462':{           'address':0x1462, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1463':{           'address':0x1463, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1464':{           'address':0x1464, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1465':{           'address':0x1465, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'unknown_0x1466':{           'address':0x1466, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
    'device_address_echo':{      'address':0x1467, 'length':1, 'type':'uint', 'scaling':'identical', 'unit': ''},
}

def linear(factor, offset, precision, input):
    if precision < 0:
        return (input*factor)+offset
    else:
        return round(linear(factor, offset, -1, input), precision)

def ascii(_nothing, input):
    return binascii.unhexlify(hex(input).replace("0x", "").encode()).decode()

def read_register(instrument, reg: dict):
    raw_data = instrument.read_registers(reg['address'], reg['length'])
    value = 0
    
    # Calculate RAW Value
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

    else:
        print(f'Warning: Unsupported register type {reg["type"]}.')
        return None
    
    # Apply scaling
    if reg['scaling']=='identical':
        return value
    else:
        # Add paramter for the input value
        head, _sep, tail = partitioned = reg['scaling'].rpartition(')')
        fnc_call = head+', value)'
        scaled = eval(fnc_call)
        return scaled

def read_register_or_false(instrument, reg):
    try:
        return read_register(instrument, reg)
    except:
        return False

def scan_addresses(instrument):
    instrument.serial.timeout = 0.1
    for address in range(1, 248):
        instrument.address = address
        print(f"checking address: {hex(address)}... ", end="")
        try:
            val = read_register(instrument, {'address':0x1467, 'length':1, 'type':'uint', 'scaling':'identical'})
            if val == address:
                print(f"battery")
            else:
                print(f"somethingelse:{hex(val)}")
        except:
            print("nope")
            pass

def find_devices(instrument):
    instrument.serial.timeout = 0.1
    for address in range(0, 248):
        print(f"checking device address: {hex(address)}... ", end="")
        
        instrument.address = address

        val = read_register_or_false(instrument, {'address':0x00C, 'length':8, 'type':'uint', 'scaling':'identical'})

        if val == False:
            print(f"no response")
            continue
            
        try:
            if binascii.unhexlify(hex(val).replace("0x", "").encode()).decode().strip() == "RBC50D1S-G1":
                print(f"RBC50D1S-G1 ")
                continue
        except:
            pass

        print(hex(val))

def scan_registers(instrument):
    usableregs = {}
    for address in range(0x0000, 0xFFFF):
        print(f"register {hex(address)}... ", end=" ")
        try:
            val = read_register(instrument, {'address': address, 'length': 1, 'type':'uint', 'scaling':'identical'})

            print(f"good! {val}")
            usableregs[address]=val
        except:
            print(f"nope")
            pass
    print(json.dumps(usableregs, indent=4))

def read_registers(instrument):
    global REGISTERS
    values = {}
    for reg in REGISTERS:
        try:
            values[reg] = read_register(instrument, REGISTERS[reg])
        except Exception as inst:
            print(f'Error: Exception reading register {reg}: {inst}.')    
    return values

def print_values_loop(instrument, format, once):
    global REGISTERS
    LINE_COUNT = 19
    GOBACK = "\033[F" * LINE_COUNT

    while(True):
        values = read_registers(instrument)

        if format == "dump":
            print('Register'.ljust(25)+'Address'.ljust(10)+'Value'.ljust(10)+'Decimal'.ljust(10)+'Binary'.ljust(21))
            print('-'*25 + '-'*10 + '-'*10 + '-'*10 + '-'*21)
            for key in values:
                keyP = key.ljust(25)
                addressP = "{0:#0{1}x}".format(REGISTERS[key]['address'],6).ljust(10)

                if isinstance(values[key], str):
                    print(f"{keyP}{addressP}\"{values[key]}\"")
                else:
                    value = f"{str(values[key])} {REGISTERS[key]['unit']}" if REGISTERS[key]['unit'] != "" else "{0:#0{1}x}".format(values[key],6)
                    valueP = value.ljust(10)
                    decP = str(values[key] if REGISTERS[key]['unit'] == '' else '').ljust(10)
                    binP = ("{0:#0{1}b}".format(values[key],18) if REGISTERS[key]['unit'] == '' else '').ljust(21)

                    print(f"{keyP}{addressP}{valueP}{decP}{binP}")

            time.sleep(1)

        elif format == "jsonl":
            print(json.dumps(values))
        
        else:
            print(f"bad format: {format}")

        if once:
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renogy Smart Battery RS485 readout.')
    parser.add_argument('--device', default='/dev/ttyUSB0', help='Serial device to use for RS485 communication')
    parser.add_argument('--address', default=0xf7, type=lambda x: int(x,0), help='Slave address of the RS485 device')
    parser.add_argument('--scan-addresses', default=False, help='Determine slave address by brute force.', action='store_true')
    parser.add_argument('--scan-registers', default=False, help='', action='store_true')
    parser.add_argument('--list-devices', default=False, help='List serial devices', action='store_true')
    parser.add_argument('--format', default='dump', help='[dump,jsonl]')
    parser.add_argument('--once', default=False, action='store_true')
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
        # 247 (0xf7) is the default address. If the another renogy device is connected it might have reprogrammed the address to another value.
        instrument = minimalmodbus.Instrument(args.device, slaveaddress=247)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 0.2

        if args.scan_addresses:
            print('Scanning addresses...')
            scan_addresses(instrument)
        else:
            instrument.address = args.address
            instrument.serial.timeout = 0.2

            if args.scan_registers:
                scan_registers(instrument)
            else:
                print_values_loop(instrument, args.format, args.once)


