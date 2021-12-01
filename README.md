## Renogy Smart Battery RS485 Data readout

This python script serves as a playground to determine the register mapping for the renogy smart batteries. I've run `--scan-registers` against all registers in the range of `0x0000` to `0xFFFF` and the example below shows which registers the battery responded to.

I'm still in the process of figuring out which register contains which value.

### Pinout

Both RJ45 jacks are connected to the same RS485 lines on the PCB, so it does not matter which jack is used to connect to the battery.
The UP port also has lines for the activation button which is connected to lines 3 and 4 and allows putting the battery into shelf mode.
![pinout](https://github.com/Grmume/renogy-smart-battery/blob/main/UP_Pinout.png)

### Commandline options

`--device`: Which serial device to use for the RS485 communication

`--address`: Address of the battery (247 by default, but can be changed by other devices). In the example below, it was changed by the DC-Home app to `0x30`.

`--scan-addresses`: Scan all addresses to determine the address of the battery.

`--scan-registers`: Scan all registers on the device address to see which ones responds. Take mulitple hours.

`--list-devices`: List all available serial devices to use for the --device option

Example output for a battery at idle (no current):

```
Register                 Address   Value     Decimal   Binary
----------------------------------------------------------------------------
cell_count               0x1388    4 cells
cellvoltage_1            0x1389    3.4 V
cellvoltage_2            0x138a    3.4 V
cellvoltage_3            0x138b    3.4 V
cellvoltage_4            0x138c    3.4 V
unknown_0x138d           0x138d    0x0000    0         0b0000000000000000
unknown_0x138e           0x138e    0x0000    0         0b0000000000000000
unknown_0x138f           0x138f    0x0000    0         0b0000000000000000
unknown_0x1390           0x1390    0x0000    0         0b0000000000000000
celltemp_1               0x139a    23.0 °c
celltemp_2               0x139b    23.0 °c
celltemp_3               0x139c    23.0 °c
celltemp_4               0x139d    22.0 °c
unknown_0x1391           0x1391    0x0000    0         0b0000000000000000
unknown_0x1392           0x1392    0x0000    0         0b0000000000000000
unknown_0x1393           0x1393    0x0000    0         0b0000000000000000
unknown_0x1394           0x1394    0x0000    0         0b0000000000000000
unknown_0x1395           0x1395    0x0000    0         0b0000000000000000
unknown_0x1396           0x1396    0x0000    0         0b0000000000000000
unknown_0x1397           0x1397    0x0000    0         0b0000000000000000
unknown_0x1398           0x1398    0x0000    0         0b0000000000000000
unknown_0x1399           0x1399    0x0003    3         0b0000000000000011
unknown_0x139e           0x139e    0x0000    0         0b0000000000000000
unknown_0x139f           0x139f    0x0000    0         0b0000000000000000
unknown_0x13a0           0x13a0    0x0000    0         0b0000000000000000
unknown_0x13a1           0x13a1    0x0000    0         0b0000000000000000
unknown_0x13a2           0x13a2    0x0000    0         0b0000000000000000
unknown_0x13a3           0x13a3    0x0000    0         0b0000000000000000
unknown_0x13a4           0x13a4    0x0000    0         0b0000000000000000
unknown_0x13a5           0x13a5    0x0000    0         0b0000000000000000
unknown_0x13a6           0x13a6    0x0000    0         0b0000000000000000
unknown_0x13a7           0x13a7    0x0000    0         0b0000000000000000
unknown_0x13a8           0x13a8    0x0000    0         0b0000000000000000
unknown_0x13a9           0x13a9    0x0000    0         0b0000000000000000
unknown_0x13ab           0x13ab    0x0000    0         0b0000000000000000
unknown_0x13ac           0x13ac    0x0001    1         0b0000000000000001
unknown_0x13ad           0x13ad    0x00f0    240       0b0000000011110000
unknown_0x13ae           0x13ae    0x0000    0         0b0000000000000000
unknown_0x13af           0x13af    0x0001    1         0b0000000000000001
unknown_0x13b0           0x13b0    0x00f0    240       0b0000000011110000
unknown_0x13b1           0x13b1    0x0000    0         0b0000000000000000
current                  0x13b2    0.0 A
voltage                  0x13b3    13.9 V
remaining_charge         0x13b4    99.72 Ah
charge_capacity          0x13b6    100.0 Ah
unknown_0x13b7           0x13b7    0x86a0    34464     0b1000011010100000
unknown_0x13b8           0x13b8    0x0000    0         0b0000000000000000
maximum_voltage?         0x13b9    14.8 V
minimum_voltage?         0x13ba    10.0 V
unknown_0x13bb           0x13bb    0x1388    5000      0b0001001110001000
unknown_0x13bc           0x13bc    0xd8f0    55536     0b1101100011110000
unknown_0x13ec           0x13ec    0x0000    0         0b0000000000000000
unknown_0x13ed           0x13ed    0x00ff    255       0b0000000011111111
unknown_0x13ee           0x13ee    0x0000    0         0b0000000000000000
unknown_0x13ef           0x13ef    0x0000    0         0b0000000000000000
unknown_0x13f0           0x13f0    0x0000    0         0b0000000000000000
unknown_0x13f1           0x13f1    0x0000    0         0b0000000000000000
unknown_0x13f2           0x13f2    0x000e    14        0b0000000000001110
unknown_0x13f3           0x13f3    0x000a    10        0b0000000000001010
unknown_0x13f4           0x13f4    0x0000    0         0b0000000000000000
unknown_0x13f5           0x13f5    0x00c0    192       0b0000000011000000
unknown_0x13f6           0x13f6    0x5050    20560     0b0101000001010000
unknown_0x13f7           0x13f7    0x5441    21569     0b0101010001000001
unknown_0x13f8           0x13f8    0x4830    18480     0b0100100000110000
unknown_0x13f9           0x13f9    0x3130    12592     0b0011000100110000
unknown_0x13fa           0x13fa    0x3531    13617     0b0011010100110001
unknown_0x13fb           0x13fb    0x3133    12595     0b0011000100110011
unknown_0x13fc           0x13fc    0x3332    13106     0b0011001100110010
unknown_0x13fd           0x13fd    0x3039    12345     0b0011000000111001
unknown_0x13fe           0x13fe    0x3031    12337     0b0011000000110001
unknown_0x13ff           0x13ff    0x3030    12336     0b0011000000110000
unknown_0x1400           0x1400    0x3031    12337     0b0011000000110001
unknown_0x1401           0x1401    0x3032    12338     0b0011000000110010
unknown_0x1402           0x1402    0x5242    21058     0b0101001001000010
unknown_0x1403           0x1403    0x5431    21553     0b0101010000110001
unknown_0x1404           0x1404    0x3030    12336     0b0011000000110000
unknown_0x1405           0x1405    0x4c46    19526     0b0100110001000110
unknown_0x1406           0x1406    0x5031    20529     0b0101000000110001
unknown_0x1407           0x1407    0x3253    12883     0b0011001001010011
unknown_0x1408           0x1408    0x2d47    11591     0b0010110101000111
unknown_0x1409           0x1409    0x3100    12544     0b0011000100000000
unknown_0x140a           0x140a    0x3030    12336     0b0011000000110000
unknown_0x140b           0x140b    0x3138    12600     0b0011000100111000
unknown_0x140c           0x140c    0x5245    21061     0b0101001001000101
unknown_0x140d           0x140d    0x4e4f    20047     0b0100111001001111
unknown_0x140e           0x140e    0x4759    18265     0b0100011101011001
unknown_0x140f           0x140f    0x0000    0         0b0000000000000000
unknown_0x1410           0x1410    0x0000    0         0b0000000000000000
unknown_0x1411           0x1411    0x0000    0         0b0000000000000000
unknown_0x1412           0x1412    0x0000    0         0b0000000000000000
unknown_0x1413           0x1413    0x0000    0         0b0000000000000000
unknown_0x1414           0x1414    0x0000    0         0b0000000000000000
unknown_0x1415           0x1415    0x0000    0         0b0000000000000000
unknown_0x1450           0x1450    0x0025    37        0b0000000000100101
unknown_0x1451           0x1451    0x0023    35        0b0000000000100011
unknown_0x1452           0x1452    0x001e    30        0b0000000000011110
unknown_0x1453           0x1453    0x0019    25        0b0000000000011001
unknown_0x1454           0x1454    0x0226    550       0b0000001000100110
unknown_0x1455           0x1455    0x01f4    500       0b0000000111110100
unknown_0x1456           0x1456    0x0032    50        0b0000000000110010
unknown_0x1457           0x1457    0x0000    0         0b0000000000000000
unknown_0x1458           0x1458    0x2ee0    12000     0b0010111011100000
unknown_0x1459           0x1459    0x2710    10000     0b0010011100010000
unknown_0x145a           0x145a    0x1770    6000      0b0001011101110000
unknown_0x145b           0x145b    0x0094    148       0b0000000010010100
unknown_0x145c           0x145c    0x008e    142       0b0000000010001110
unknown_0x145d           0x145d    0x0078    120       0b0000000001111000
unknown_0x145e           0x145e    0x0064    100       0b0000000001100100
unknown_0x145f           0x145f    0x0258    600       0b0000001001011000
unknown_0x1460           0x1460    0x01f4    500       0b0000000111110100
unknown_0x1461           0x1461    0xff9c    65436     0b1111111110011100
unknown_0x1462           0x1462    0xff06    65286     0b1111111100000110
unknown_0x1463           0x1463    0xc568    50536     0b1100010101101000
unknown_0x1464           0x1464    0xcd38    52536     0b1100110100111000
unknown_0x1465           0x1465    0xd508    54536     0b1101010100001000
unknown_0x1466           0x1466    0x0000    0         0b0000000000000000
device_address?          0x1467    0x0030    48        0b0000000000110000
```
