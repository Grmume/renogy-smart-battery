## Renogy Smart Battery RS485 Data readout

This python script serves as a playground to determine the register mapping for the renogy smart batteries.
So far I have found two consecutive address regions for which the battery returns values:
0x1388 - 0x13a9 and
0x13ab - 0x13bc

I'm still in the process of figuring out which register contains which value.

### Pinout
Both RJ45 jacks are connected to the same RS485 lines on the PCB, so it does not matter which jack is used to connect to the battery.
The UP port also has lines for the activation button which is connected to lines 3 and 4 and allows putting the battery into shelf mode.
![pinout](https://github.com/Grmume/renogy-smart-battery/blob/main/UP_Pinout.png)

### Commandline options
--device: Which serial device to use for the RS485 communication
--address: Address of the battery (247 by default, but can be changed by other devices)
--scan-addresses: Scan all addresses to determine the address of the battery.
--list-devices: List all available serial devices to use for the --device option

### Sample output


Battery Idle
```
Register                 Address   Value               Binary
----------------------------------------------------------------------------------------------
cell_count               0x1388    4                   00000000 00000100
cellvoltage_1            0x1389    3.30 V              00000000 00100001
cellvoltage_2            0x138a    3.30 V              00000000 00100001
cellvoltage_3            0x138b    3.30 V              00000000 00100001
cellvoltage_4            0x138c    3.30 V              00000000 00100001
unknown_0x138d           0x138d    0                   00000000 00000000
unknown_0x138e           0x138e    0                   00000000 00000000
unknown_0x138f           0x138f    0                   00000000 00000000
unknown_0x1390           0x1390    0                   00000000 00000000
celltemp_1               0x139a    18.00 °C            00000000 10110100
celltemp_2               0x139b    18.00 °C            00000000 10110100
celltemp_3               0x139c    18.00 °C            00000000 10110100
celltemp_4               0x139d    18.00 °C            00000000 10110100
unknown_0x1391           0x1391    0                   00000000 00000000
unknown_0x1392           0x1392    0                   00000000 00000000
unknown_0x1393           0x1393    0                   00000000 00000000
unknown_0x1394           0x1394    0                   00000000 00000000
unknown_0x1395           0x1395    0                   00000000 00000000
unknown_0x1396           0x1396    0                   00000000 00000000
unknown_0x1397           0x1397    0                   00000000 00000000
unknown_0x1398           0x1398    0                   00000000 00000000
unknown_0x1399           0x1399    3                   00000000 00000011
unknown_0x139e           0x139e    0                   00000000 00000000
unknown_0x139f           0x139f    0                   00000000 00000000
unknown_0x13a0           0x13a0    0                   00000000 00000000
unknown_0x13a1           0x13a1    0                   00000000 00000000
unknown_0x13a2           0x13a2    0                   00000000 00000000
unknown_0x13a3           0x13a3    0                   00000000 00000000
unknown_0x13a4           0x13a4    0                   00000000 00000000
unknown_0x13a5           0x13a5    0                   00000000 00000000
unknown_0x13a6           0x13a6    0                   00000000 00000000
unknown_0x13a7           0x13a7    0                   00000000 00000000
unknown_0x13a8           0x13a8    0                   00000000 00000000
unknown_0x13a9           0x13a9    0                   00000000 00000000
unknown_0x13ab           0x13ab    0                   00000000 00000000
unknown_0x13ac           0x13ac    1                   00000000 00000001
unknown_0x13ad           0x13ad    200                 00000000 11001000
unknown_0x13ae           0x13ae    0                   00000000 00000000
unknown_0x13af           0x13af    1                   00000000 00000001
unknown_0x13b0           0x13b0    180                 00000000 10110100
unknown_0x13b1           0x13b1    0                   00000000 00000000
current                  0x13b2    0.00 A              00000000 00000000
voltage                  0x13b3    13.50 V             00000000 10000111
remaining_charge         0x13b4    93.00 Ah            00000000 00000001 01101011 01000111
capacity                 0x13b6    100.00 Ah           00000000 00000001 10000110 10100000
unknown_0x13b7           0x13b7    34464               10000110 10100000
unknown_0x13b8           0x13b8    0                   00000000 00000000
ov_protect               0x13b9    14.80 V             00000000 10010100
uv_protect               0x13ba    10.00 V             00000000 01100100
unknown_0x13bb           0x13bb    5000                00010011 10001000
unknown_0x13bc           0x13bc    55536               11011000 11110000
unknown_0x13ec           0x13ec    0                   00000000 00000000
unknown_0x13ed           0x13ed    0                   00000000 00000000
unknown_0x13ee           0x13ee    0                   00000000 00000000
heater_level             0x13ef    0.00 %              00000000 00000000
unknown_0x13f0           0x13f0    0                   00000000 00000000
unknown_0x13f1           0x13f1    0                   00000000 00000000
unknown_0x13f2           0x13f2    14                  00000000 00001110
unknown_0x13f3           0x13f3    0                   00000000 00000000
unknown_0x13f4           0x13f4    0                   00000000 00000000
unknown_0x13f5           0x13f5    192                 00000000 11000000
serial                   0x13f6    PPTAHXXXXXXXXXXX    01010000 01010000 01010100 01000...
unknown_0x13fe           0x13fe    12337               00110000 00110001
unknown_0x13ff           0x13ff    12336               00110000 00110000
unknown_0x1400           0x1400    12337               00110000 00110001
unknown_0x1401           0x1401    12338               00110000 00110010
model                    0x1402    RBT100LFP12SH-G1    01010010 01000010 01010100 00110...
firmware_version         0x140a    0119                00110000 00110001 00110001 00111001
manufacturer             0x140c    RENOGY              01010010 01000101 01001110 01001...
unknown_0x1410           0x1410    0                   00000000 00000000
unknown_0x1411           0x1411    0                   00000000 00000000
unknown_0x1412           0x1412    0                   00000000 00000000
unknown_0x1413           0x1413    0                   00000000 00000000
unknown_0x1414           0x1414    0                   00000000 00000000
unknown_0x1415           0x1415    0                   00000000 00000000
cell_ov_protect          0x1450    3.70 V              00000000 00100101
cell_ov_recover          0x1451    3.50 V              00000000 00100011
cell_uv_warn             0x1452    3.00 V              00000000 00011110
cell_uv_protect          0x1453    2.50 V              00000000 00011001
hightemp_protect         0x1454    55.00 °C            00000010 00100110
hightemp_warn?           0x1455    50.00 °C            00000001 11110100
hightemp_hysteresis      0x1456    5.00 K              00000000 00110010
unknown_0x1457           0x1457    0                   00000000 00000000
unknown_0x1458           0x1458    12000               00101110 11100000
unknown_0x1459           0x1459    10000               00100111 00010000
unknown_0x145a           0x145a    6000                00010111 01110000
unknown_0x145b           0x145b    148                 00000000 10010100
unknown_0x145c           0x145c    142                 00000000 10001110
unknown_0x145d           0x145d    120                 00000000 01111000
unknown_0x145e           0x145e    100                 00000000 01100100
unknown_0x145f           0x145f    600                 00000010 01011000
unknown_0x1460           0x1460    500                 00000001 11110100
unknown_0x1461           0x1461    65436               11111111 10011100
unknown_0x1462           0x1462    65286               11111111 00000110
unknown_0x1463           0x1463    50536               11000101 01101000
unknown_0x1464           0x1464    52536               11001101 00111000
unknown_0x1465           0x1465    54536               11010101 00001000
unknown_0x1466           0x1466    0                   00000000 00000000
device_address           0x1467    247                 00000000 11110111
```

Battery Charging (14.8 A)
```
Register                 Address   Value               Binary
----------------------------------------------------------------------------------------------
cell_count               0x1388    4                   00000000 00000100
cellvoltage_1            0x1389    3.40 V              00000000 00100010
cellvoltage_2            0x138a    3.40 V              00000000 00100010
cellvoltage_3            0x138b    3.40 V              00000000 00100010
cellvoltage_4            0x138c    3.30 V              00000000 00100001
unknown_0x138d           0x138d    0                   00000000 00000000
unknown_0x138e           0x138e    0                   00000000 00000000
unknown_0x138f           0x138f    0                   00000000 00000000
unknown_0x1390           0x1390    0                   00000000 00000000
celltemp_1               0x139a    18.00 °C            00000000 10110100
celltemp_2               0x139b    18.00 °C            00000000 10110100
celltemp_3               0x139c    18.00 °C            00000000 10110100
celltemp_4               0x139d    18.00 °C            00000000 10110100
unknown_0x1391           0x1391    0                   00000000 00000000
unknown_0x1392           0x1392    0                   00000000 00000000
unknown_0x1393           0x1393    0                   00000000 00000000
unknown_0x1394           0x1394    0                   00000000 00000000
unknown_0x1395           0x1395    0                   00000000 00000000
unknown_0x1396           0x1396    0                   00000000 00000000
unknown_0x1397           0x1397    0                   00000000 00000000
unknown_0x1398           0x1398    0                   00000000 00000000
unknown_0x1399           0x1399    3                   00000000 00000011
unknown_0x139e           0x139e    0                   00000000 00000000
unknown_0x139f           0x139f    0                   00000000 00000000
unknown_0x13a0           0x13a0    0                   00000000 00000000
unknown_0x13a1           0x13a1    0                   00000000 00000000
unknown_0x13a2           0x13a2    0                   00000000 00000000
unknown_0x13a3           0x13a3    0                   00000000 00000000
unknown_0x13a4           0x13a4    0                   00000000 00000000
unknown_0x13a5           0x13a5    0                   00000000 00000000
unknown_0x13a6           0x13a6    0                   00000000 00000000
unknown_0x13a7           0x13a7    0                   00000000 00000000
unknown_0x13a8           0x13a8    0                   00000000 00000000
unknown_0x13a9           0x13a9    0                   00000000 00000000
unknown_0x13ab           0x13ab    0                   00000000 00000000
unknown_0x13ac           0x13ac    1                   00000000 00000001
unknown_0x13ad           0x13ad    200                 00000000 11001000
unknown_0x13ae           0x13ae    0                   00000000 00000000
unknown_0x13af           0x13af    1                   00000000 00000001
unknown_0x13b0           0x13b0    180                 00000000 10110100
unknown_0x13b1           0x13b1    0                   00000000 00000000
current                  0x13b2    14.82 A             00000101 11001010
voltage                  0x13b3    13.60 V             00000000 10001000
remaining_charge         0x13b4    93.00 Ah            00000000 00000001 01101011 01001000
capacity                 0x13b6    100.00 Ah           00000000 00000001 10000110 10100000
unknown_0x13b7           0x13b7    34464               10000110 10100000
unknown_0x13b8           0x13b8    0                   00000000 00000000
ov_protect               0x13b9    14.80 V             00000000 10010100
uv_protect               0x13ba    10.00 V             00000000 01100100
unknown_0x13bb           0x13bb    5000                00010011 10001000
unknown_0x13bc           0x13bc    55536               11011000 11110000
unknown_0x13ec           0x13ec    0                   00000000 00000000
unknown_0x13ed           0x13ed    0                   00000000 00000000
unknown_0x13ee           0x13ee    0                   00000000 00000000
heater_level             0x13ef    0.00 %              00000000 00000000
unknown_0x13f0           0x13f0    0                   00000000 00000000
unknown_0x13f1           0x13f1    0                   00000000 00000000
unknown_0x13f2           0x13f2    14                  00000000 00001110
unknown_0x13f3           0x13f3    0                   00000000 00000000
unknown_0x13f4           0x13f4    0                   00000000 00000000
unknown_0x13f5           0x13f5    192                 00000000 11000000
serial                   0x13f6    PPTAHXXXXXXXXXXX    01010000 01010000 01010100 01000...
unknown_0x13fe           0x13fe    12337               00110000 00110001
unknown_0x13ff           0x13ff    12336               00110000 00110000
unknown_0x1400           0x1400    12337               00110000 00110001
unknown_0x1401           0x1401    12338               00110000 00110010
model                    0x1402    RBT100LFP12SH-G1    01010010 01000010 01010100 00110...
firmware_version         0x140a    0119                00110000 00110001 00110001 00111001
manufacturer             0x140c    RENOGY              01010010 01000101 01001110 01001...
unknown_0x1410           0x1410    0                   00000000 00000000
unknown_0x1411           0x1411    0                   00000000 00000000
unknown_0x1412           0x1412    0                   00000000 00000000
unknown_0x1413           0x1413    0                   00000000 00000000
unknown_0x1414           0x1414    0                   00000000 00000000
unknown_0x1415           0x1415    0                   00000000 00000000
cell_ov_protect          0x1450    3.70 V              00000000 00100101
cell_ov_recover          0x1451    3.50 V              00000000 00100011
cell_uv_warn             0x1452    3.00 V              00000000 00011110
cell_uv_protect          0x1453    2.50 V              00000000 00011001
hightemp_protect         0x1454    55.00 °C            00000010 00100110
hightemp_warn?           0x1455    50.00 °C            00000001 11110100
hightemp_hysteresis      0x1456    5.00 K              00000000 00110010
unknown_0x1457           0x1457    0                   00000000 00000000
unknown_0x1458           0x1458    12000               00101110 11100000
unknown_0x1459           0x1459    10000               00100111 00010000
unknown_0x145a           0x145a    6000                00010111 01110000
unknown_0x145b           0x145b    148                 00000000 10010100
unknown_0x145c           0x145c    142                 00000000 10001110
unknown_0x145d           0x145d    120                 00000000 01111000
unknown_0x145e           0x145e    100                 00000000 01100100
unknown_0x145f           0x145f    600                 00000010 01011000
unknown_0x1460           0x1460    500                 00000001 11110100
unknown_0x1461           0x1461    65436               11111111 10011100
unknown_0x1462           0x1462    65286               11111111 00000110
unknown_0x1463           0x1463    50536               11000101 01101000
unknown_0x1464           0x1464    52536               11001101 00111000
unknown_0x1465           0x1465    54536               11010101 00001000
unknown_0x1466           0x1466    0                   00000000 00000000
device_address           0x1467    247                 00000000 11110111
```
