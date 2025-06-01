# May 30th: Started Fusion Design
Started on the 3D model of the Spider<br>
Decided on a quadraped(for now) and designed a 3dof leg<br>
This leg is around 160 mm long, and I intend to use MG90 servos as SG90s just suck(MG90s still kinda suck, but atleast they suck less)<br>
Will most likely use some form of I2C servo driver, as I will have a **MINIMUM** of twelve servos<br>
![image of robot](foosion.png)<br>
**Total Time Spent - 7h(i redesigned it 4 times)**

# May 31st: Continued Fusion Design
Changed some stuff with the model, including making it far wider<br>
Mounted both picam holders for stereoscopic camera<br>
**Total Time Spent - 1.5h**

# June 1st: Finished Fusion Design
Fixed some dimensions as I had to change my battery voltage for power<br>
Settled on a Raspi 5, [this](https://robu.in/product/24v-12v-to-5v-5a-power-module-dc-dc-xy-3606-power-converter/) awesome power board(have worked with it before) and the PCA9685 for driving the servos<br>
Started attempting to derive the equations for IK, as i have no idea what i'm doing when it comes to math<br>
**Total Time Spent - 3h**

# June 1st(pt 2): Finished firmware
Moved all my stereo camera experiments to here and added an obstacle detector to it<br>
Added a quadraped controller to my exisitng IK program<br>
Did some OOP and made everything look pretty<br>
Also made a main program for the shiggles<br>
Also made a scrappy schematic as there is NO pcb required but ehh, schematic is required so I made it<br>
Now I only have to work on the 'shipping' aspect - adding more pictures, doing a readme and looking at parts sourcing<br>
Should be finished by June 2nd, and then i will ship it<br>
**Total time spent - 3h + ~roughly 6h for the earlier stereo camera stuff so 9h**

**Total across 3 days - 20.5h**