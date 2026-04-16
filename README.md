Improving RRT* for 2D Parking Route Planning

<b>Developer:</b> Anagha Malladi<br>
<b>Mentors:</b> Prof. Dr. Kin Chung Kwan and Prof. Dr. Haiquan Chen, California State University, Sacramento<br>
<b>Project Duration:</b> Aug 2024 - May 2025<br>
<b>Degree:</b> Master of Science in Computer Science<br>

What This Project Is About:

Autonomous vehicles in structured spaces like parking lots face challenges due to limited space, obstacles, and non-holonomic motion constraints. Traditional methods like A* struggle with scalability, and basic RRT or Dubins paths lack the flexibility needed for tight environments.
This project enhances the RRT* path planning algorithm with three key improvements — spline fitting, node pruning, and two-phase sampling — and compares it against existing methods to find the most practical solution for real-world autonomous parking.

Goal:

To improve 2D path planning for autonomous vehicles in structured parking environments by enhancing RRT* and evaluating it against Dubins and Reeds-Shepp models across multiple parking scenarios, measuring path length, computation time, number of turns, and success rate.

Environments Tested:

Three structured parking environments were simulated:

Compact parking lot — tight spaces with limited maneuverability
Parallel parking setup — narrow lanes requiring reverse motion
Mall-style parking area — larger space with multiple obstacles

Each environment was tested with 10 runs using fixed start coordinates (142, 171) and goal coordinates (384, 176).

Algorithms Compared:

| Algorithm | Distance | Time | Turns | Tree Depth |
|---|---|---|---|---|
| RRT | 302.16 units | 2.70s | 30 | 1106 |
| RRT* | 221.98 units | 1.34s | 3 | 448 |
| RRT + Dubins | 422.32 units | 3.40s | 120 | 574 |
| RRT + Reeds-Shepp | 359.97 units | 2.70s | 107 | 404 |
| RRT* + Dubins | 386.25 units | 0.76s | 67 | 641 |
| RRT* + Reeds-Shepp | 342.64 units | 0.73s | 41 | 273 |
| **Ours + Dubins** | 381.66 units | **0.41s** | 35 | 48 |
| **Ours + Reeds-Shepp** | **225.57 units** | **0.20s** | **16** | **23** |

Key Findings:

Enhanced RRT with Reeds-Shepp* achieved the best overall performance — shortest distance, fastest time, fewest turns, and shallowest tree depth across all three test cases
Spline fitting + node pruning significantly reduced tree depth from 448 (standard RRT*) to just 23 nodes, making the algorithm far more efficient
Dubins paths were faster in open areas but failed frequently in compact environments due to their forward-only motion constraint
Reeds-Shepp support for reverse motion made it ideal for parallel parking and tight spaces
The enhanced approach achieved a parking success rate of 90% or higher in structured scenarios


Results:

Across all three test cases, the enhanced RRT* with Reeds-Shepp steering consistently outperformed all baseline methods:

Up to 15x faster computation time compared to standard RRT
Significantly fewer turns — reduced from 116 (Case 3, RRT* + RS) to 47 with the enhanced approach
Smoother paths due to spline fitting, making them more realistic for actual vehicle execution
Reeds-Shepp with RRT* was identified as the most practical approach for real-world autonomous parking


Tech Stack:

Python — Pygame, NumPy, Matplotlib (simulation and visualization)
MATLAB — Validation and analysis


Enhancements Over Standard RRT*

Spline Fitting — replaces jagged tree paths with smooth curves suitable for vehicle motion
Node Pruning — removes redundant intermediate nodes, reducing tree depth dramatically
Two-Phase Sampling — improves exploration efficiency by combining goal-biased and uniform sampling
