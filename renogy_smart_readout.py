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
    # START - Slave returns unknown data address below here
    'test001':{                  'address':0x1388, 'length':2, 'type':'uint16'},
    'test002':{                  'address':0x1389, 'length':2, 'type':'uint16'},
    'test003':{                  'address':0x138a, 'length':2, 'type':'uint16'},
    'test004':{                  'address':0x138b, 'length':2, 'type':'uint16'},
    'test20':{                   'address':0x138c, 'length':2, 'type':'uint16'},
    'test21':{                   'address':0x138d, 'length':2, 'type':'uint16'},
    'test22':{                   'address':0x138e, 'length':2, 'type':'uint16'},
    'test23':{                   'address':0x138f, 'length':2, 'type':'uint16'},
    'test24':{                   'address':0x1390, 'length':2, 'type':'uint16'},
    'test25':{                   'address':0x1391, 'length':2, 'type':'uint16'},
    'test26':{                   'address':0x1392, 'length':2, 'type':'uint16'},
    'test27':{                   'address':0x1393, 'length':2, 'type':'uint16'},
    'test28':{                   'address':0x1394, 'length':2, 'type':'uint16'},
    'test29':{                   'address':0x1395, 'length':2, 'type':'uint16'},
    'test30':{                   'address':0x1396, 'length':2, 'type':'uint16'},
    'test31':{                   'address':0x1397, 'length':2, 'type':'uint16'},
    'test32':{                   'address':0x1398, 'length':2, 'type':'uint16'},
    'test33':{                   'address':0x1399, 'length':2, 'type':'uint16'},
    'test34':{                   'address':0x139a, 'length':2, 'type':'uint16'},
    'test35':{                   'address':0x139b, 'length':2, 'type':'uint16'},
    'test36':{                   'address':0x139c, 'length':2, 'type':'uint16'},
    'test50':{                   'address':0x139d, 'length':2, 'type':'uint16'},
    'test51':{                   'address':0x139e, 'length':2, 'type':'uint16'},
    'test52':{                   'address':0x139f, 'length':2, 'type':'uint16'},
    'test53':{                   'address':0x13a0, 'length':2, 'type':'uint16'},
    'test54':{                   'address':0x13a1, 'length':2, 'type':'uint16'},
    'test55':{                   'address':0x13a2, 'length':2, 'type':'uint16'},
    'test99':{                   'address':0x13a3, 'length':2, 'type':'uint16'},
    'test98':{                   'address':0x13a4, 'length':2, 'type':'uint16'},
    'test97':{                   'address':0x13a5, 'length':2, 'type':'uint16'},
    'test96':{                   'address':0x13a6, 'length':2, 'type':'uint16'},
    'test01':{                   'address':0x13a7, 'length':2, 'type':'uint16'},
    'test02':{                   'address':0x13a8, 'length':2, 'type':'uint16'},
    'test03':{                   'address':0x13a9, 'length':2, 'type':'uint16'},

    'test05':{                   'address':0x13ab, 'length':2, 'type':'uint16'},
    'test06':{                   'address':0x13ac, 'length':2, 'type':'uint16'},
    'test07':{                   'address':0x13ad, 'length':2, 'type':'uint16'},
    'test08':{                   'address':0x13ae, 'length':2, 'type':'uint16'},
    'test09':{                   'address':0x13af, 'length':2, 'type':'uint16'},
    'test10':{                   'address':0x13b0, 'length':2, 'type':'uint16'},
    'test11':{                   'address':0x13b1, 'length':2, 'type':'uint16'},
    'current':{                  'address':0x13b2, 'length':2, 'type':'uint16'},
    'voltage':{                  'address':0x13b3, 'length':2, 'type':'uint16'},
    'test88':{                   'address':0x13b4, 'length':2, 'type':'uint16'},
    'test12':{                   'address':0x13b5, 'length':2, 'type':'uint16'},
    'test99':{                   'address':0x13b6, 'length':2, 'type':'uint16'},
    'test13':{                   'address':0x13b7, 'length':2, 'type':'uint16'},
    'test14':{                   'address':0x13b8, 'length':2, 'type':'uint16'},
    'test15':{                   'address':0x13b9, 'length':2, 'type':'uint16'},
    'test16':{                   'address':0x13ba, 'length':2, 'type':'uint16'},
    'test17':{                   'address':0x13bb, 'length':2, 'type':'uint16'},
    'test18':{                   'address':0x13bc, 'length':2, 'type':'uint16'}
    # END - Slave returns unknown address from here onward
}

def read_register(instrument, reg: dict):
    if reg['type'] == 'string':
        return instrument.read_string(reg['address'], reg['length'])
    elif reg['type'] == 'uint16':
        return instrument.read_register(reg['address'])
    elif reg['type'] == 'uint32':
        return instrument.read_long(reg['address'])
    else:
        print(f'Warning: Unsupported register type {reg["type"]}.')
        return None

def scan_addresses(instrument):
    TEST_REGISTER = {'address':0x13b3, 'length':2, 'type':'uint16'}
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

def print_values_loop(instrument):
    global REGISTERS
    LINE_COUNT = 19
    GOBACK = "\033[F" * LINE_COUNT

    while(True):
        values = read_registers(instrument)

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
            print(val.ljust(25)+"{0:#0{1}x}".format(REGISTERS[val]['address'],6).ljust(10), str(values[val]).ljust(10))

        time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Renogy Smart Battery RS485 readout.')
    parser.add_argument('--device', default='/dev/ttyUSB0', help='Serial device to use for RS485 communication')
    parser.add_argument('--address', default=0x7f, type=lambda x: int(x,0), help='Slave address of the RS485 device')
    parser.add_argument('--scan-addresses', default=False, help='Determine slave address by brute force.', action='store_true')
    parser.add_argument('--list-devices', default=False, help='List serial devices', action='store_true')
    args = parser.parse_args()

    if args.list_devices:
        print('device'.ljust(25)+'manufacturer'.ljust(25)+'product'.ljust(25)+'description')
        print('---------------------------------------------------------------------------------------')
        for port in serial.tools.list_ports.comports():
            dev = port.device or 'n/a'
            manf = port.manufacturer or 'n/a'
            prod = port.product or 'n/a'
            desc = port.description or 'n/a'
            print(dev.ljust(25)+manf.ljust(25)+prod.ljust(25)+desc)
    else:
        # 247 (0xf7) is the default address. If the another renogy device is connected it might have reprogrammed the address to another value.
        instrument = minimalmodbus.Instrument(args.device, slaveaddress=247)
        instrument.serial.baudrate = 9600
        instrument.serial.timeout = 0.2

        if args.scan_addresses:
            print('Scanning addresses...')
            slave_address = scan_addresses(instrument)

            if(slave_address != None):
                print(f'Slave address: {hex(address)}')
            else:
                print('Error: could not determine slave address.')
        else:
            slave_address = args.address

        if slave_address != None:
            instrument.address = slave_address
            instrument.serial.timeout = 0.2
            print_values_loop(instrument)


