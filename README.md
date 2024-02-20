```markdown
# Inverse Kinematics Solver

This software simulates the movement of a robotic arm by solving the inverse kinematics problem. It provides a visual representation of the arm's movement within its work envelope, based on user-defined parameters and target positions.

## Features

- **Dynamic Input**: Accepts lengths of the robotic arm segments and target coordinates.
- **Directional Control**: Allows for clockwise or counter-clockwise final arm orientation.
- **Visual Simulation**: Projects the movement of the robotic arm on a Cartesian plane.

## Getting Started

### Initial Data Reading

The software requires the user to input the following parameters:

- `L1`, `L2`: Lengths of the first and second segments of the robotic arm. It is essential to ensure these values allow the arm to be projected within the screen's dimensions.
- **Direction**: Specify the arm's final projection direction (clockwise or counter-clockwise).
- `x2`, `y2`: Coordinates of the end of the arm's second segment, which must be within the external boundary and outside the internal work envelope.

### Cartesian System Projection Routine

A routine projects the Cartesian coordinate system with the horizontal X-axis and the vertical Y-axis at the screen's center.

### Work Space Projection Routine

This routine projects the internal and external work envelope, defining the operational area of the robotic arm.

### Solution Calculation Routine

Functions to calculate two pairs of solutions (`x1a,y1a` & `x1b,y1b`) for the arm's base positions, representing counter-clockwise and clockwise orientations.

### Solution Discrimination

The software distinguishes between the counter-clockwise and clockwise solution pairs. Based on the user's initial choice, it retains the appropriate pair for the final arm projection.

### User Input for Movement

Users specify target coordinates (`xt`, `yt`) for the robotic arm's movement, implying a straight-line motion. The software validates the feasibility of the motion and requests new coordinates if necessary.

### Animation Process

Upon validating the target coordinates, the software animates the robotic arm's movement from the initial position to the final target in a straight line.


