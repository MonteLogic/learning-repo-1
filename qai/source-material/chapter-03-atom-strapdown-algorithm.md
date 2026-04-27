# Chapter 3: The Atom Strapdown — Predicting the Quantum Phase with Classical Physics

## Introduction: Bridging Two Worlds

We now arrive at the intellectual heart of the Tennstedt paper: the atom strapdown algorithm. The name is intentionally chosen to echo the classical strapdown algorithm introduced in Chapter Two. But instead of integrating accelerations and angular rates to find the position and velocity of the vehicle, the atom strapdown integrates the exact same sensor measurements to find the predicted position of the atom wave packet within the sensor frame. From that predicted position, the expected quantum phase shift can be calculated and compared to the actual measured phase.

This is the key conceptual leap. The laser pulses that form the atom interferometer act as a spatial ruler, measuring where the atoms are in the sensor frame at specific moments in time. The conventional navigation system provides a high-rate prediction of those exact positions. The difference between the predicted and measured positions, which is encoded as a phase difference, reveals the conventional sensor's internal errors.

In this chapter, we unpack the generalized phase shift formula, the equations of motion for the atomic wave packet, the fictitious forces in rotating frames, the challenge of physical separation between sensors, the multi-axis measurement scheme, the alternative convolution method, and the complete filter architecture.

## Revisiting the Phase Shift Formula

Recall from Chapter One that the fundamental phase shift of an atom interferometer is a combination of the atom's position at the time of each laser pulse. The formula takes the atom's position at the first pulse, subtracts twice the position at the second pulse, and adds the position at the third pulse, all multiplied by the wave number of the laser light. 

For the typical setup where the atom starts at the center of the sensor frame when the first pulse is applied, the initial position is zero. This simplifies the formula. The phase shift becomes negative two times the atom's position at the middle pulse, plus the atom's position at the final pulse, scaled by the wave number. 

A key contribution of the paper is developing a rigorous mathematical framework for calculating those exact positions when the sensor frame is itself rotating and accelerating on a moving vehicle.

## The Atom Wave Packet as a Classical Particle

Here is a profound simplification that makes the whole enterprise possible: we can treat the center of mass of the atom wave packet as a classical particle. We can use classical mechanics to predict its trajectory, as long as three conditions are met. First, the wave packet must remain coherent, meaning the two arms of the interferometer can still interfere. Second, the external forces must change slowly across the physical size of the wave packet. Third, higher-order quantum effects, like changes in gravity across tiny distances, must be small enough to ignore.

Under these assumptions, the center-of-mass motion of the atom wave packet simply obeys Newton's second law within the sensor frame. The paper expresses this as two coupled differential equations. The first says that the change in the atom's position is its velocity. The second says that the change in the atom's velocity, or its acceleration, is equal to the measured specific force, plus gravity, minus the Coriolis force. 

These equations are then integrated mathematically over time to find the exact position of the atom at the time of the second and third laser pulses. This integration is performed numerically in real time, using the conventional sensor's outputs sampled at a very high rate. 

Why is the Coriolis force there? The sensor frame rotates with the vehicle and with the Earth. From the perspective of someone standing in a rotating frame, any moving object appears to experience a sideways force. This is the Coriolis force. The atom wave packet, after the first laser pulse, is moving relative to the sensor frame because it absorbed the momentum of a laser photon. As the sensor frame rotates, the atom's trajectory is deflected by the Coriolis force. This deflection accumulates a phase shift, and this phase shift is the very basis of rotation sensing.

## Fictitious Forces in Rotating Frames

To correctly predict the atom's motion, we must account for all the fictitious forces that arise because the frame is rotating and accelerating. The paper presents a careful derivation of these terms.

The first is the centrifugal force. When a frame rotates, any object that is displaced from the rotation axis appears to experience an outward force. The distance from the center of the conventional sensor to the center of the atomic sensor is called the lever arm. The conventional sensor, sitting at the center, does not feel this force. But the atom wave packet, sitting at a distance, does. If we use the conventional reading without correcting for this geometric effect, we will incorrectly predict the atom's position. This centrifugal term scales with the length of the lever arm and the square of the rotation rate.

The second is the Euler force. If the rotation rate is changing over time, meaning there is an angular acceleration, there is an additional force called the Euler force. It depends on the direction and magnitude of the angular acceleration multiplied by the lever arm. In rapid maneuvers, the Euler force can sometimes exceed the centrifugal force.

The final fictitious force is the coning-sculling mix term. It arises when there is simultaneous linear acceleration and rotation, and neither is constant. When the frame is rotating, the direction of gravity and acceleration is continuously changing relative to the sensor. If we add up the accelerometer output without accounting for this changing orientation, errors accumulate. The mix term corrects for this. For most Earth-bound navigation with short atomic measurement times, this term is small, but for space applications with long measurement times, it becomes significant.

## The Lever Arm: Spatial Separation Between Sensors

The lever arm introduces the fictitious force terms just described. Why should there be a lever arm at all? Why not put both sensors in the exact same spot? 

In practice, a cold atom interferometer requires a vacuum chamber, cooling laser optics, magnetic coils, and large detection systems. A conventional inertial sensor is a compact electronic device. They physically cannot occupy the same space. In a real system, the atomic sensor might be in a separate enclosure a few tens of centimeters away.

The paper investigates the effect of this lever arm on navigation performance. If the conventional sensor has a small bias, the error in the predicted atomic phase scales linearly with the length of the lever arm. This means the larger the physical separation, the larger the navigation error. 

This result has a critical engineering implication. To get the best performance, the two instruments must be as close together as possible, or the exact distance between them must be measured with millimeter-level accuracy. Any uncertainty in the lever arm adds directly to navigation error.

## The Multi-Axis Differential Scheme

A single atomic sensor pointing vertically measures gravity plus vertical acceleration. But to navigate in the real world, you need measurements along three perpendicular axes. More fundamentally, you need to separate the effects of acceleration from the effects of rotation, because both produce phase shifts.

The paper uses a scheme called a differential measurement. The idea is to use a single atomic source and split the initial wave packet into two clouds traveling in opposite directions along the same axis. Because they move in opposite directions, the two clouds experience the same linear accelerations but opposite Coriolis forces. 

By taking the sum of the two phase shifts, the rotation effects cancel out, leaving a pure measurement of acceleration. By taking the difference between the two phase shifts, the acceleration effects cancel out, leaving a pure measurement of rotation. In a full three-dimensional setup, three pairs of these opposite-traveling clouds are launched simultaneously. This provides six independent measurements, from which all three axes of acceleration and all three axes of rotation can be extracted. 

## The Convolution Method: An Alternative Approach

The paper validates its atom strapdown algorithm by comparing it to an alternative preexisting method called the convolution method. The convolution method requires calculating an acceleration sensitivity function for the atomic sensor. This function describes how sensitive the phase shift is to accelerations at every microsecond during the measurement. It peaks in the middle of the sequence, meaning shaking the sensor during the middle mirror pulse has the biggest effect on the phase.

To predict the phase, the conventional acceleration signal is mathematically convolved, or blended, with this sensitivity function and added up over time. 

The authors tested both methods on the same experimental data. The results showed they agree almost perfectly, with only a tiny, negligible difference. However, there are deep conceptual differences between them. The convolution method requires knowing the specific sensitivity function and is primarily designed for linear acceleration. The atom strapdown method is vastly more general. It handles full three-dimensional motion, incorporates rotation naturally through Coriolis and centrifugal terms, mathematically handles multiple sensors placed at different locations, and can even incorporate alternative data sources like wheel speed sensors.

## The Complete Filter Architecture

Let us trace the complete flow of data in the fully integrated system.

Step one is data collection. The conventional sensor continuously outputs acceleration and rotation data hundreds of times a second.

Step two is conventional navigation. The classical strapdown algorithm runs at full speed, calculating position, velocity, and orientation. This solution slowly drifts due to sensor bias.

Step three is phase prediction. During each atomic measurement cycle, the exact same conventional sensor data is fed into the atom strapdown equations. The result is a highly accurate prediction of where the atoms should be, and consequently, a predicted quantum phase shift. 

Step four is the quantum measurement. At the end of the atomic cycle, the atoms are detected by counting the light they emit. The ratio of atoms in the two states gives the true, measured quantum phase.

Step five is the filter update. The filter calculates the difference between the true measured phase and the predicted phase. Using the complex observation math we discussed in Chapter Two, the filter works backward from this difference to figure out exactly what the conventional sensor biases must be.

Finally, step six is the correction. The newly discovered biases are subtracted from the conventional sensor's output, preventing further drift. This loop repeats endlessly, providing navigation that is both highly responsive and perfectly stable.

This entire process encodes the dynamic movement of the vehicle into the quantum phase of an atomic wave function. It is a remarkable bridge between classical physics and the weird world of quantum mechanics, turning the most fundamental building blocks of matter into the ultimate navigation instrument. In the final chapter, we will explore the simulation results that validate this entire framework and look toward the future of the technology.
