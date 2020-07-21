#  Copycat Drone

> This package enables a drone to copy the movements of another one through a Natural Point  OptiTrack motion capture system.

The project consists of a drone that copies the movement of another one through the Natural Point OptiTrack motion capture system. This was developed within the ROS Kinetic Kame framework making use of the Virtual Reality Peripheral Network protocol  for positioning; proportional-integral-derivative controllers for movement  and the ardrone-autonomy ROS package for drone communication. 

## Requirements

* 2 AR Parrot Drones
* An Natural Point Tracking system with support for **Virtual Reality Peripheral Netowrk Protocol (VRPNP)**
* A computer with Ubuntu 16.04.3 LTS and ROS Kinetic Came
* Dependencies (ROS Packages):
  - ardrone_autonomy
  - vrpn_client_ros
  - pid

## Running

1. Connect your computer to one drone via WiFi.
2. Connect through ethernet to your Natural Motion System.
3. Create a Quad1 object in your VRPNP system.
4. Run master launch file:
```
launch_master.launch
```


# Meta

* **Luis M.**           - [GitHub](https://github.com/lemontyc)
* **Dirk**              -  [dirko17](https://github.com/dirko17)
* **Emiliano Specia**   -  [emiliano50](https://github.com/emiliano50)

This package was developed for the **TC3050-Robot Vision** course at **Instituto Tecnológico de Monterrey campus Querétaro**.
