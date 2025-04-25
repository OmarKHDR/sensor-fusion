## Goals
- capture and calibrate camera
- measure distances and direction using ultra sonic and servo
- transform from real world coordinates to camera coordinates
- project the estimated real-world position of an object onto camera image


## setup:
- for now lets assume the hardware part exists and works as expected, that means we have:
	- ultrasonic mounted to a servo motor with the needed microcontroller and code
	- get a 1d image from the altrasonic showing the depth of each point
- assuming we have a camera, lol:
	- calibrate usign checkerboard
	- get K, [R|t]

- now we have the equation to transform real world coordinates to image coordinates u=K[R∣t]X
- fusing both real world coordinates with the camera 2d image

- display camera feed, overlay object position, and compare with the visually detected position
---
## IO

| Input               | Output                                |
|---------------------|---------------------------------------|
| Servo angle value   | Camera feed with projected points shown |
| Ultrasonic value    |                                       |
| Camera feed         |                                       |




## NOTES:
- criteria = (type, maxCount, epsilon)
- type = 1 or 2 or 3, using maxcount only, using min acc only, using both
- max iterations, its 30 minimum accuracy 0.001 stop refining if either 30 terations or 0.001 acc achieved
- mgrid shows all available combinations from a 2d points in a n*m grid 
	- the grid will return an x, y arrays first shows all rows, second shows all columns and both of size n*m
