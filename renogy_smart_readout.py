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


REGISTERS = {
    'cell_count':{               'address':0x1388, 'length':1, 'type':'uint', 'scaling':'identical',      'unit':''},
    'celltemp_1':{               'address':0x139a, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'celltemp_2':{               'address':0x139b, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'celltemp_3':{               'address':0x139c, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'celltemp_4':{               'address':0x139d, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit': '°c'},
    'cellvoltage_1':{            'address':0x1389, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit':'V'},
    'cellvoltage_2':{            'address':0x138a, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit':'V'},
    'cellvoltage_3':{            'address':0x138b, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit':'V'},
    'cellvoltage_4':{            'address':0x138c, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,-1)',  'unit':'V'},
    'current':{                  'address':0x13b2, 'length':1, 'type':'sint', 'scaling':'linear(0.1,0,-1)', 'unit': 'A'},
    'charge_capacity':{          'address':0x13b6, 'length':2, 'type':'uint', 'scaling':'linear(0.001,0,-1)','unit':'Ah'},
    'remaining_charge':{         'address':0x13b4, 'length':2, 'type':'uint', 'scaling':'linear(0.001,0,2)','unit':'Ah'},
    'voltage':{                  'address':0x13b3, 'length':1, 'type':'uint', 'scaling':'linear(0.1,0,2)',  'unit':'V'},

    'unknown_0x138d':{           'address':0x138d, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x138e':{           'address':0x138e, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x138f':{           'address':0x138f, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1390':{           'address':0x1390, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1391':{           'address':0x1391, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1392':{           'address':0x1392, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1393':{           'address':0x1393, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1394':{           'address':0x1394, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1395':{           'address':0x1395, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1396':{           'address':0x1396, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1397':{           'address':0x1397, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1398':{           'address':0x1398, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x1399':{           'address':0x1399, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x139e':{           'address':0x139e, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x139f':{           'address':0x139f, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a0':{           'address':0x13a0, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a1':{           'address':0x13a1, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a2':{           'address':0x13a2, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a3':{           'address':0x13a3, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a4':{           'address':0x13a4, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a5':{           'address':0x13a5, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a6':{           'address':0x13a6, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a7':{           'address':0x13a7, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a8':{           'address':0x13a8, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13a9':{           'address':0x13a9, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13ab':{           'address':0x13ab, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13ac':{           'address':0x13ac, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13ad':{           'address':0x13ad, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13ae':{           'address':0x13ae, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13af':{           'address':0x13af, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13b0':{           'address':0x13b0, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13b1':{           'address':0x13b1, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13b7':{           'address':0x13b7, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13b8':{           'address':0x13b8, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13b9':{           'address':0x13b9, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13ba':{           'address':0x13ba, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13bb':{           'address':0x13bb, 'length':1, 'type':'uint', 'scaling':'identical'},
    'unknown_0x13bc':{           'address':0x13bc, 'length':1, 'type':'uint', 'scaling':'identical'}
    # END - Slave returns unknown address from here onward
}

def linear(factor, offset, precision, input):
    if precision < 0:
        return (input*factor)+offset
    else:
        return round(linear(factor, offset, -1, input), precision)

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

def scan_addresses(instrument):
    TEST_REGISTER = {'address':0x13b3, 'length':1, 'type':'uint', 'scaling':'identical'}
    instrument.serial.timeout = 0.1
    for address in range(247, 248):
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

def print_values_loop(instrument, format, once):
    global REGISTERS
    LINE_COUNT = 19
    GOBACK = "\033[F" * LINE_COUNT

    while(True):
        values = read_registers(instrument)

        if format == "dump":
            # print(f'''{GOBACK}
            #         SOC:                {values['soc_aux']}
            #         Temps:              {values['temp_pcb_cells']}
            #         Charge State:       {values['charge_state']}
            #         Error Codes:        {values['error_codes']}
            #         Aux. Voltage:       {values['voltage_aux']}
            #         Max Charge:         {values['max_charge']}
            #         Alt. Voltage:       {values['voltage_alt']}
            #         Alt. Current:       {values['current_alt']}
            #         Alt. Watts:         {values['power_alt']}
            #         Solar Voltage:      {values['voltage_solar']}
            #         Solar Current:      {values['current_solar']}
            #         Daily Voltage Low:  {values['voltage_daily_low']}
            #         Daily Voltage High: {values['voltage_daily_high']}
            #         Daily Current High: {values['current_daily_high']}
            #         Daily Power High:   {values['power_daily_high']}
            #         Daily gen. Power:   {values['power_daily_acc']}
            #         Capacity charged:   {values['charged_capacity_acc']}
            #         Tot. running days:  {values['total_running_days']}''')
            print('')
            print('Register'.ljust(25)+'Address'.ljust(10)+'Value'.ljust(10))
            print('---------------------------------------------------------------------')
            for val in values:
                print(val.ljust(25)+"{0:#0{1}x}".format(REGISTERS[val]['address'],6).ljust(10), str(values[val]).ljust(10)+f" {REGISTERS[val]['unit']}")

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
            print_values_loop(instrument, args.format, args.once)


