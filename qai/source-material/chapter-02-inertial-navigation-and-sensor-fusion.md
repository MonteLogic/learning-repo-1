# Chapter 2: Inertial Navigation, Coordinate Frames, and the Kalman Filter

## Introduction: The Dead Reckoning Problem

Before GPS existed, the only way to navigate without visual landmarks was dead reckoning. To perform dead reckoning, you start from a known position, then continuously add up your velocity to estimate how far you have traveled, and add up your angular rate to estimate how much you have turned. If you know your starting point precisely and your sensors are perfect, you can track your position indefinitely. But real sensors are not perfect. They drift. A tiny constant error in your accelerometer output, called a bias, adds up over time into a growing velocity error. That velocity error then adds up even faster into an ever-widening position error. After an hour of navigation with a typical low-cost accelerometer, the position error can reach hundreds of meters. After a day, it could be kilometers.

Inertial navigation systems suffer from precisely this problem. The conventional fix is to periodically correct the navigation system with an external reference, such as GPS, radar altimetry, star trackers, or, as Tennstedt and colleagues propose, an atom interferometer. Understanding how this correction is performed, and the mathematical machinery behind it, is the subject of this chapter.

We will cover five key topics: reference frames, which are the coordinate systems needed to describe navigation in a rotating world; the strapdown algorithm, which is the core computation that converts sensor measurements into position and velocity; sensor errors, like bias, white noise, and random walk, and why they cause navigation to drift; the Kalman filter, the optimal algorithm for fusing imperfect sensor data; and finally, the Extended Kalman Filter, its nonlinear generalization, used throughout the research paper.

## Reference Frames: Getting Your Bearings

To describe the position and motion of anything, you must first choose a coordinate frame. A coordinate frame is a set of mutually perpendicular axes with a well-defined origin. Different situations call for different frames, and translating between them is a core skill in navigation mathematics. The Tennstedt paper uses several specific frames, all of which are standard in inertial navigation.

First is the inertial frame. The inertial frame is a non-rotating, non-accelerating reference frame fixed to the center of the Earth or, more rigorously, to the stars. Newton's laws of motion hold exactly in an inertial frame; there are no fictitious forces. The downside is that the Earth rotates relative to this frame at roughly seven times ten to the negative fifth radians per second, which corresponds to one full rotation every twenty-four hours. For high-precision navigation, this rotation matters enormously.

Next is the Earth frame, or Earth-centered, Earth-fixed frame. It has its origin at the center of the Earth, with one axis pointing toward the prime meridian, and it rotates with the Earth. A GPS receiver typically outputs coordinates in this frame, converted to latitude, longitude, and altitude. However, because the Earth is rotating, this frame is not inertial. There are fictitious forces, like the Coriolis force and the centrifugal force, when you try to apply Newton's laws here.

For local navigation, like a ship or airplane moving over a small patch of the Earth, it is convenient to use a local-level navigation frame with axes pointing North, East, and Down. The origin travels with the vehicle, and the axes stay aligned with the local cardinal directions and the local vertical. Position in this frame corresponds directly to latitude, longitude, and altitude.

Then there is the body frame. The body frame is fixed to the vehicle itself, with axes aligned with the vehicle's forward, right, and down directions. Accelerometers and gyroscopes measure forces and angular rates in the body frame. The central task of the strapdown algorithm is to transform these measurements from the body frame into the navigation frame so that they can be integrated to give position and velocity in meaningful, real-world coordinates.

Finally, in the Tennstedt paper, additional sensor frames are introduced for each individual Cold Atom Interferometer. Each atomic sensor has its own coordinate axes, typically defined so that one axis—the sensitive axis—is aligned with the laser beams that manipulate the atoms. If there are three atomic sensors measuring three orthogonal directions of acceleration, there will be three sensor frames. The relationship between a sensor frame and the body frame is defined by a rotation matrix and a lever arm, which is the physical distance vector from the center of the inertial measurement unit to the center of the atomic sensor. These concepts are deeply explored in the next chapter.

## Rotation Matrices and Direction Cosine Matrices

Transforming a vector from one coordinate frame to another requires a rotation matrix. If you know a vector expressed in one frame and want to know its components in another, you multiply it by the rotation matrix between them. In navigation, rotation matrices between coordinate frames are called direction cosine matrices. The entry in each row and column of this matrix is simply the cosine of the angle between an axis of the first frame and an axis of the second frame. The paper notes that if the atomic sensor is perfectly aligned with the body frame, the transformation matrix is just the identity matrix, making the transformation trivial.

A direction cosine matrix contains nine numbers, but a rotation in three-dimensional space is completely specified by only three numbers, representing three degrees of freedom. The most intuitive parameterization is Euler angles: roll, pitch, and yaw. These represent sequential rotations about three body-fixed axes. However, Euler angles have a notorious problem called gimbal lock: when pitch reaches exactly ninety degrees straight up or down, roll and yaw become indistinguishable, and the mathematics break down. For this reason, navigation systems that must handle arbitrary orientations, like spacecraft or submarines, often use other mathematical representations like quaternions. The paper mentions attitude as a matrix from the navigation to the body frame but does not delve into the parameterization, since the primary focus is on the atom interferometer equations.

## The Strapdown Algorithm

The word "strapdown" refers to the fact that the inertial sensors are strapped down, or rigidly fixed, to the vehicle rather than mounted on a gimbaled stabilized platform. Older inertial navigation systems used mechanical gimbals to keep the accelerometers physically horizontal at all times. Modern systems strap the sensors directly to the vehicle and perform the leveling computationally. This computational leveling is the strapdown algorithm.

The strapdown algorithm takes the accelerometer measurements, which represent specific force in the body frame, and gyroscope measurements, which represent angular rate in the body frame, and adds them up over time to produce position, velocity, and attitude.

Step one is the attitude update. Use the gyroscope measurement to update the vehicle's attitude. The orientation evolves continuously according to the measured rotation rates. In practice, this equation is integrated numerically at a high update rate, often hundreds of times per second, to keep track of the vehicle's orientation.

Step two is the specific force transformation. Transform the accelerometer measurement from the body frame to the navigation frame using the attitude matrix computed in step one. This gives the specific force, which is acceleration minus gravity, in navigation-frame coordinates.

Step three is the velocity update. Add gravity, and account for the Earth's rotation and the vehicle's own angular motion over the curved Earth. These rotational effects cause Coriolis and centripetal forces that must be subtracted. The result is added up over time to give the current velocity.

Step four is the position update. Simply add up the velocity over time to get the current position. In the local navigation frame, this gives the position vector, which is often converted to latitude, longitude, and altitude.

This four-step cycle repeats at the sensor's output rate, typically between one hundred and one thousand times per second for tactical-grade systems. The result is a continuous estimate of the vehicle's position, velocity, and attitude.

## The Coriolis Force: An Unavoidable Complication

The Coriolis force is a fictitious force that appears in rotating reference frames. It acts on any object that is moving within the rotating frame. For the Earth-rotating frame, the Coriolis acceleration depends on the Earth's rotation vector and the velocity of the moving object. For a bullet fired horizontally northward in the Northern Hemisphere, the Coriolis force deflects it to the right, eastward. For a navigation system, ignoring the Coriolis force introduces systematic errors.

The Coriolis force appears in atom interferometry too, but in a different context. When an atom is moving within a rotating sensor frame, such as a laboratory rotating with the Earth, the atom experiences a Coriolis force that shifts its trajectory relative to the laser. This shift accumulates a quantum phase. This is actually the basis of the atomic gyroscope: by measuring the Coriolis-induced phase shift, one can determine the rotation rate. The multi-axis scheme in the Tennstedt paper exploits both the acceleration-sensitive and rotation-sensitive terms to extract full six-degree-of-freedom inertial measurements.

## Inertial Sensor Errors

Real accelerometers and gyroscopes are not perfect. Their outputs deviate from the true quantities in several ways.

First is bias. A bias, or offset, is a constant additive error. The sensor always reads a little bit too high or too low, regardless of what the true acceleration is. Bias is the dominant navigation error source. Because it is constant, it adds up directly into velocity error, and then into a rapidly growing position error. An accelerometer with a tiny bias can accumulate a position error of nearly a kilometer after just one hour. This is why atom interferometers, which have essentially zero long-term drift, are so attractive as a calibration source.

Second is white noise. White noise, or random noise, is a high-frequency random fluctuation in the sensor output. When added up over time, white noise produces a random walk in velocity. This means it wanders randomly, growing slower than the error caused by a constant bias, but it can still become significant over long missions.

Finally, there is random walk. Angular random walk and velocity random walk are terms for the integrated effect of white noise in gyroscopes and accelerometers, respectively. They quantify how much the sensor's integrated output wanders over time purely due to noise. In the paper's mathematical model, the bias of each sensor is modeled as a random walk process. It slowly drifts over time, driven by white noise. This is the standard way to model slow sensor drift in these frameworks.

## The Kalman Filter: Optimal Estimation Under Uncertainty

The Kalman filter is the workhorse of navigation, control, and signal processing. It provides the mathematically optimal way to combine noisy sensor measurements with a predictive model to estimate the hidden state of a system. It is used in virtually every precision navigation system ever built.

The filter operates in two alternating steps. First is the prediction step, or time update. Given the current best estimate of the state and the mathematical model of how the state evolves in time, the filter predicts where the state will be at the next time step. It also calculates a covariance matrix, which is a measure of our uncertainty about the state estimate, taking into account the random process noise added at each step.

Second is the update step, or measurement update. When a new measurement arrives, the filter updates the state estimate. It calculates a Kalman gain, which is a weighting factor that decides how much to trust the measurement versus the prediction. If the prediction is very uncertain or the measurement is very precise, the gain is large, and the filter trusts the measurement. If the prediction is confident or the measurement is noisy, the gain is small, and the filter trusts the prediction. It then updates the state based on the difference between the actual measurement and the predicted measurement, known as the innovation. This automatic weighting is what makes the Kalman filter optimal.

## The Error-State Extended Kalman Filter

The standard Kalman filter assumes that the equations describing the system are linear. Real navigation systems are highly nonlinear, involving rotation matrices and trigonometric functions. The Extended Kalman Filter handles nonlinearity by approximating the system equations as linear around the current best estimate.

In navigation, the most common approach is the Error-State Extended Kalman Filter. Instead of estimating the full navigation state directly, the filter estimates the error in the navigation solution. The full state is calculated at high speed using the raw sensor data. The filter then estimates a small correction that accounts for sensor biases and accumulated errors. When the filter receives a measurement from an external reference like an atom interferometer, it updates the error estimate and feeds that correction back into the main trajectory.

This is exactly the architecture used in the Tennstedt paper. The state vector includes the position error, velocity error, accelerometer bias, and gyroscope bias. The atom interferometer provides the measurement that updates this state. Specifically, it provides an observation of the interferometer phase that depends on the sensor biases through the strapdown equations. 

## Connecting the Atom Sensor to Sensor Errors

The most mathematically challenging part of the paper is the derivation of the observation matrix, the matrix that connects the atomic phase shift measurement to the conventional sensor bias states. This is how the atom interferometer tells the filter about errors in the conventional sensors.

The key insight is that the predicted phase shift, computed using the atom strapdown equations, depends on the accelerations and angular rates measured by the conventional sensors. If those sensors have a bias, the predicted atomic phase will be slightly wrong. By comparing the predicted phase to the actual measured phase from the atom interferometer, the filter can mathematically work backward to find the bias.

The mathematical derivation involves taking the partial derivative of the predicted phase with respect to each element of the bias vector. For the acceleration bias, the phase is sensitive to the bias scaled by the square of the interrogation time, plus an extra term that accounts for rotation when the conventional sensor is physically separated from the atomic sensor. The gyroscope bias observation is considerably more complex, involving terms from the Coriolis force, the centrifugal force, and other fictitious forces. This complexity reflects the rich physics of a rotating, accelerating sensor system.

## Why Combine Both Sensors?

At this point, you may wonder: if atom interferometers are so stable, why use conventional sensors at all? And conversely, if conventional sensors drift, why not just use the atomic ones? The answer lies in their complementary strengths.

Conventional sensors have a high update rate, often hundreds of times per second. They can handle highly dynamic environments with large, sudden movements. However, they suffer from high short-term noise and terrible long-term drift.

Atom interferometers, on the other hand, have a low update rate, often taking seconds per measurement due to the time required to trap and cool the atoms. They have a very limited dynamic range because of the fringe ambiguity problem discussed in Chapter One. But they possess extremely low noise and essentially zero long-term drift.

The conventional sensor provides the high-rate, high-dynamic-range data needed to resolve the atomic sensor's fringe ambiguity. The atomic sensor provides the long-term stability needed to correct the conventional sensor's accumulating bias. Together, they form a system that is better than either alone, providing navigation-grade precision over extended periods, even in dynamic environments. This combination reduces position drift by a factor of thirty, proving the immense value of this hybrid approach. In Chapter Three, we will explore exactly how the atom strapdown algorithm makes this prediction possible.
