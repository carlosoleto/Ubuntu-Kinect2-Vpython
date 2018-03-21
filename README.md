# Kinect2_Biofeedback
How to use Kinectv2 in Ubuntu/ROS to do skeleton tracking and biofeedback information to the user.

Well ... it is a long long long journey. I hope it can same some time from some souls out there.

First of all, the goal is to use Kinect2 in Ubuntu 16 with python. We choose to visualize the data with VPython, because it worked before in Windows and would be lovely to see it work in Linux and in the future with ROS.

BEWARE!!!! To make this work we need something called NiTE2, which can generate skeleton data from the RGBD camera. Remember that the Microsoft SDK that runs on Windows provides more track-able joints. In NiTE2 you don't get the foot toe, for example. No ankle dorsi-flexion for you kiddo.

Moving on....

First of all, we need to make Kinect2 visible in Ubuntu. So, follow the steps in https://github.com/OpenKinect/libfreenect2 to install libfreenect2. That's what make the RGBD data available in Ubuntu. Run the tests, its cool.

WARNING: I have RADEON graphic card, so it is hard to set up properly (in my machine), but give it a try if you are as unfortunate as myself. Go find your light at https://www2.ati.com/relnotes/amd-catalyst-graphics-driver-installer-notes-for-linux-operating-systems.pdf

Then, it all became clearer when I found this (thanks a lot George Brindeiro): 
http://matrivian.github.io/computer%20vision/2015/04/06/openni2-2-and-nite2-2-on-ubuntu-14-04-lts.html

Just skip the part about libfreenect (watch out the version) and go for the installation of OpenNI. You should have noticed that NiTE2 download is just a sentence, not a link. So my friend, go and get it here:  


https://github.com/BrainTech/nite2-bindings  
