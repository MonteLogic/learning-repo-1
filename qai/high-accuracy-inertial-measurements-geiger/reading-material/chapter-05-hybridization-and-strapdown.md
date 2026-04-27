# Chapter 5: The Best of Both Worlds - Hybridization and the Atom Strapdown

We have established a seemingly impossible paradox. We possess a classical Inertial Measurement Unit that can handle the violent, high-speed maneuvers of a fighter jet but slowly loses its mind over time due to drift. We possess a quantum Cold Atom Interferometer that never drifts and is anchored to the fundamental constants of the universe, but is completely blinded by the slightest vibration due to the fringe ambiguity problem.

The solution, as proposed by Benjamin Tennstedt and his colleagues in their academic paper, is hybridization. We must fuse the two systems together. We must use the fast, tough classical sensor to guide the slow, delicate quantum sensor. 

But how, exactly, do you plug a physical, macro-scale gyroscope into a cloud of ultra-cold rubidium atoms floating in a vacuum chamber?

You don't plug them in physically. You plug them in mathematically. You use software to build a bridge between the macroscopic world and the quantum realm. The architecture of that mathematical bridge is what the authors call the "Atom Strapdown" method. 

To understand the Atom Strapdown method, we must first understand the fundamental concept of a classical strapdown algorithm.

### The Classical Strapdown Algorithm

In the early days of inertial navigation—think of the Apollo spacecraft flying to the moon—the accelerometers and gyroscopes were mounted on complex mechanical structures called gimbals. These gimbals consisted of multiple concentric metal rings, driven by electric motors, designed to keep the sensors pointing in exactly the same direction regardless of how the spacecraft rolled, pitched, or yawed. 

If the spacecraft rolled left, the motors would physically spin the gimbals to the right, keeping the sensor platform perfectly level. 

This mechanical stabilization was incredibly heavy, expensive, and prone to failure. If a motor broke, or if the spacecraft maneuvered so violently that the metal rings locked up—a condition known as gimbal lock—the navigation system was dead.

As computers became smaller and more powerful in the late twentieth century, engineers realized they could get rid of the heavy metal rings entirely. Instead of physically stabilizing the sensors, they could just bolt the sensors directly to the frame of the vehicle. They could "strap them down."

In a strapdown system, the accelerometers and gyroscopes simply tumble through space along with the vehicle. When the vehicle rolls, the sensors roll with it. 

To figure out where the vehicle is going, the onboard computer has to perform a furious, non-stop mathematical calculation. It takes the angular rates from the gyroscopes and uses them to mathematically calculate exactly which way the accelerometers are pointing at any given microsecond. It then takes the acceleration data, mathematically rotates it to match the orientation of the Earth, and integrates it to find velocity and position.

This continuous mathematical rotation and integration of sensor data is the classical strapdown algorithm. It is the heart of every modern navigation system on the planet.

### The Problem of Two Frames

The classical strapdown algorithm is designed to track the position of the vehicle relative to the Earth. 

But our Cold Atom Interferometer doesn't care about the Earth. The phase shift of the atom wave packet depends entirely on the position of the atoms relative to the lasers that are firing at them. 

This is the crux of the hybridization problem. We have two completely different coordinate frames. 

First, we have the "Body Frame." The origin of the Body Frame is the exact physical center of our classical IMU. The classical accelerometers and gyroscopes are measuring forces and rotations strictly within this Body Frame.

Second, we have the "Sensor Frame." The origin of the Sensor Frame is the exact physical location where the atomic wave packet is released into free fall. The lasers that split and recombine the atoms are aligned to this Sensor Frame. The quantum phase shift is measured strictly within this Sensor Frame.

In an ideal, simplified world, you would mount the classical IMU perfectly aligned with the atom vacuum chamber, so the Body Frame and the Sensor Frame were exactly identical. 

But in the real world of engineering, this is often impossible. The classical IMU might be mounted on the floor of the submarine, while the massive vacuum chamber and laser tables of the quantum sensor are mounted to the ceiling. There is a physical distance between them. There might be a slight angular misalignment between them. 

If the submarine turns sharply, the classical IMU on the floor will measure a certain acceleration. But because the vacuum chamber on the ceiling is farther away from the center of rotation, it will experience a slightly different acceleration, much like the outside horse on a merry-go-round travels faster than the inside horse. 

If we just blindly feed the classical IMU data into the quantum math, we will get the wrong answer. 

### The Atom Strapdown Method

The genius of Tennstedt's paper is the creation of a generalized mathematical framework that solves this problem. The Atom Strapdown method is a specialized version of the classical strapdown algorithm, explicitly designed to track the position of a quantum wave packet in the Sensor Frame, using data provided by classical sensors in the Body Frame. 

It is a prediction engine. 

Here is how it works. When the first laser pulse fires, the atom wave packet splits and begins its free fall. For the next ten or twenty milliseconds, the atoms are entirely disconnected from the vehicle. 

During those twenty milliseconds, the classical IMU is working furiously. It is reading the accelerations and rotations of the Body Frame thousands of times per second. 

The computer takes that classical data and runs it through the Atom Strapdown equations. 

First, it mathematically transforms the forces from the Body Frame to the Sensor Frame. It calculates the exact physical distance between the two sensors—a distance called the "lever arm." It uses this lever arm to calculate the fictitious forces created by rotation. It calculates the centrifugal force—the "merry-go-round" effect. It calculates the Euler terms, which deal with angular acceleration. 

Through these complex transformations, the computer determines exactly how the lasers in the Sensor Frame are accelerating and rotating, based entirely on the measurements from the classical IMU in the Body Frame.

Next, the computer uses these transformed accelerations to simulate the flight of the atom. 

It writes a differential equation for the velocity of the atom wave packet. It says that the change in the atom's velocity is equal to the specific forces measured by the lasers, minus the Coriolis force created by the rotation of the frame, minus the constant downward pull of Earth's gravity.

It then integrates this velocity over time to calculate the exact, predicted position of the atom wave packet relative to the lasers at the exact moment the second laser pulse fires. And then it does it again to find the position at the moment the third laser pulse fires.

Finally, the computer takes these predicted positions, plugs them into our phase shift equation—k-sub-one times x-sub-one, minus two k-sub-two times x-sub-two, plus k-sub-three times x-sub-three—and calculates a predicted phase shift. 

### Solving the Ambiguity

This predicted phase shift is the "hour" on our digital watch. 

Because the classical IMU was continuously tracking the high-speed movements of the vehicle during those twenty milliseconds, the predicted phase shift is generally correct. It knows roughly how many wave cycles the phase has been pushed through by the vibrations. 

But because the classical IMU has bias and drift, the predicted phase shift is not perfectly precise. It might predict that the phase is exactly fifteen radians. 

Then, the actual atom interferometer finishes its sequence. The atoms hit the detector. The computer counts the transition probability and calculates the actual, measured phase shift using the inverse cosine function. 

Because of the fringe ambiguity, the actual measurement just gives a position on a single wave slope. It might tell the computer that the phase is point-zero-one radians, plus or minus any number of full wave cycles. 

The computer now compares the two. It looks at the prediction of fifteen radians, and it looks at the actual measurement of point-zero-one radians. It mathematically aligns them. It realizes that the true phase shift must be the specific wave cycle that puts the point-zero-one measurement as close as possible to the fifteen-radian prediction. 

The fringe ambiguity is solved. The sensor is no longer blind.

We have successfully used the classical sensor to keep track of the wave cycles, and we have used the quantum sensor to find the exact, absolute point on the wave. 

But the hybridization is not finished. We have used the classical IMU to help the atom interferometer, but we haven't yet used the atom interferometer to help the classical IMU. We haven't solved the drift problem. 

To do that, we need to take the difference between our predicted phase and our actual phase—an error value we call the "innovation"—and feed it back into the classical IMU to correct its bias. 

We need an algorithm that can take a phase shift of a quantum wave and somehow use it to figure out that a physical gyroscope is drifting by a fraction of a degree per hour. 

To accomplish this seemingly magical feat of reverse engineering, we will need the most powerful statistical tool in the history of navigation. We will need the Extended Kalman Filter. We will explore this algorithm in chapter seven. But first, in chapter six, we must look deeper into the complex math of coordinate frames and the specific physical architecture the researchers used to build a multi-axis quantum compass.
