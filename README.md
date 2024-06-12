# PumPyWorm
Pump controller program for flowing salt buffers to C. elegans. Build upon a modified version of Florian Lapp's nesp-lib library. 

This is a GUI-based program for controlling two New Era NE-1000X syringe pumps. I wrote it with the expectation that the two pumps contain buffers with different salt concentrations; these two channels are then combined in line with a static mixer to a chosen concentration. It lets a user easily input protocols consisting of different concentration holds and linear gradients. 

![image](images/screenshot.png)

The pumps must have the X1 firmware upgrade (for the linear gradients) but I don't have any safeguards in place in case you don't have the upgrade, so it will probably just error out if you don't. 

The protocols are saved in the pump as phases in the pump program. Each pump can contain a maximum of 41 phases. If you upgrade to the X2 firmware you can increase that to 340 phases or so. This might be worthwhile for more complex experiments. 

**Note**: phases that consist of one pump being paused (i.e. 0% A or 100% A, etc) enter a "pause" cycle into the appropriate phase. This function has a limit of 99 seconds. Thus, a pause can quickly cause the number of phases to be longer than expected! For example, a run of 30 minutes at 100% A would result in pump B having a pause ~18 phases long. 



