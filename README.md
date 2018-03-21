# Ubuntu-Kinect2-Vpython
How to use Kinectv2 in Ubuntu 16 to do skeleton tracking and biofeedback information to the user.

Well ... it is a long long long journey. I hope it can same some time from some souls out there.

First of all, the goal is to use Kinect2 in Ubuntu 16 with python. We choose to visualize the data with VPython, because it worked before in Windows and would be lovely to see it work in Linux and in the future with ROS.

BEWARE!!!! To make this work we need something called NiTE2, which can generate skeleton data from the RGBD camera. Remember that the Microsoft SDK that runs on Windows provides more track-able joints. In NiTE2 you don't get the foot toe, for example. No ankle dorsi-flexion for you kiddo.

Moving on....

First of all, we need to make Kinect2 visible in Ubuntu. So, follow the steps in https://github.com/OpenKinect/libfreenect2 to install libfreenect2. That's what make the RGBD data available in Ubuntu. Run the tests, its cool.

WARNING: I have RADEON graphic card, so it is hard to set up properly (in my machine), but give it a try if you are as unfortunate as myself. Go find your light at https://www2.ati.com/relnotes/amd-catalyst-graphics-driver-installer-notes-for-linux-operating-systems.pdf


IF YOUR TEST GOES WRONG CHECK THE LAST WARNING MESSAGE!!!!

Then, it all became clearer when I found this (thanks a lot George Brindeiro): 
http://matrivian.github.io/computer%20vision/2015/04/06/openni2-2-and-nite2-2-on-ubuntu-14-04-lts.html

Just skip the part about libfreenect (watch out the version) and go for the installation of OpenNI. You should have noticed that NiTE2 download is just a sentence, not a link. So my friend, go and get it here on the git folder.

Continue with the installation and voilá! Nice, we can track people movement.

IF YOUR TEST GOES WRONG CHECK THE LAST WARNING MESSAGE!!!!

To make it work with python, I could manage to make it work with my system's python2.7 64bit. My attempts to make it work with anaconda failed.

So, let's install VPython.

Following the excellet post https://ubuntuforum-br.org/index.php?topic=121607.0 . Run the bash file of the git folder. 

sudo bash InstalandoVpython.sh 

Or you could do the chmod thing.

sudo chmod +777 InstalandoVpython.sh
./InstalandoVpython.sh 

If everything worked good, found the "bounce.py" file in your computer and run it. You should see a red ball bouncing.

Now, we are almost done, use this python wrapper for NiTE2 https://github.com/BrainTech/nite2-bindings.

Just remember to set up the proper files path of the OpenNI2 and NiTE2 folders in the Makefile and you are ready to run

make

:D

Try to run some of the tests that it has in the folder.

WARNING: to make it work so far I had to move a lot the folder and libraries (.so and .so0 files) from freenect, OpenNI2 and NiTE2 folders. You should have noticed that some of the tests until here failed because something was missing. Check the print screen in the git folder just to check all the files that need to be together to make it work.

Put the file usertracker2.py from this git folder in the wrapper folder and run it. It should work!

Happy hacking.

