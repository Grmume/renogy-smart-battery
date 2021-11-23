## Renogy Smart Battery RS485 Data readout

This python script serves as a playground to determine the register mapping for the renogy smart batteries.
So far I have found two consecutive address regions for which the battery returns values:
0x1388 - 0x13a9 and
0x13ab - 0x13bc

I'm still in the process if figuring out which register contains which value.

### Commandline options
--device: Which serial device to use for the RS485 communication
--address: Address of the battery (247 by default, but can be changed by other devices)
--scan-addresses: Scan all addresses to determine the address of the battery.
--list-devices: List all available serial devices to use for the --device option

Example output for a new battery at idle (no current):

```
Register                 Address   Value     
---------------------------------------------------------------------
test001                  0x1388     4         
test002                  0x1389     33        
test003                  0x138a     33        
test004                  0x138b     33        
test20                   0x138c     33        
test21                   0x138d     0         
test22                   0x138e     0         
test23                   0x138f     0         
test24                   0x1390     0         
test25                   0x1391     0         
test26                   0x1392     0         
test27                   0x1393     0         
test28                   0x1394     0         
test29                   0x1395     0         
test30                   0x1396     0         
test31                   0x1397     0         
test32                   0x1398     0         
test33                   0x1399     3         
test34                   0x139a     180       
test35                   0x139b     180       
test36                   0x139c     180       
test50                   0x139d     180       
test51                   0x139e     0         
test52                   0x139f     0         
test53                   0x13a0     0         
test54                   0x13a1     0         
test55                   0x13a2     0         
test99                   0x13b6     1         
test98                   0x13a4     0         
test97                   0x13a5     0         
test96                   0x13a6     0         
test01                   0x13a7     0         
test02                   0x13a8     0         
test03                   0x13a9     0         
test05                   0x13ab     0         
test06                   0x13ac     1         
test07                   0x13ad     190       
test08                   0x13ae     0         
test09                   0x13af     1         
test10                   0x13b0     190       
test11                   0x13b1     0         
current                  0x13b2     0         
voltage                  0x13b3     133       
capacity                 0x13b4     1         
test12                   0x13b5     3820      
test13                   0x13b7     34464     
test14                   0x13b8     0         
test15                   0x13b9     148       
test16                   0x13ba     100       
test17                   0x13bb     5000      
test18                   0x13bc     55536
```