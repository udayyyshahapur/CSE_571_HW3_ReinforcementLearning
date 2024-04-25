# Q-Learning Agents for Pacman

In this project, we compared the Semi-Gradient TD(Lambda) and True Online TD(Lambda) methods
with the Q-Learning method. The code includes several agent implementations, ApproximateQAgent, SemiGradientTDQAgent, and TrueOnlineTDQAgent.


# Setup Instructions

1. Ensure you have Python installed on your machine. Python 3.6.6 is recommended.
2. ## Required Libraries
   The script requires the following Python libraries:
   **NumPy**: For numerical operations
   **Plotly**: For creating interactive plots
   **SciPy**: Includes functions for scientific and technical computing, such as statistical tests

## Installation
Run the following commands in your terminal to install the required libraries:
```bash
pip install numpy
pip install plotly
pip install scipy

2. Clone this repository or download the files to your local environment.

# How To Run Code
1. python pacman.py -p TrueOnlineTDQAgent -a extractor=SimpleExtractor -x 200 -n 210 -l mediumClassic
2. -p: Specifies the agent class to use. (ApproximateQAgent, TrueOnlineTDQAgent, SemiGradientTDQAgent)
3. -a: Provides agent parameters (e.g., extractor, epsilon, gamma, alpha, lambda).
4. -x: The number of training episodes.
5. -n: The total number of episodes (including testing).
6. -l: The Pacman game layout. (customLayoutHard/trickyLayout/capsuleClassic, Check out the layouts folder for more.)
7. --frameTime: Adjusts the frame delay for visual output.


This repository contains the Python script `testing.py`, which is designed to evaluate and compare the performance of three reinforcement learning algorithms: SemiGradientTDQAgent, ApproximateQAgent, and TrueOnlineTDQAgent. The evaluations are conducted using the Pac-Man game simulations under different layouts.

- **Simulation Execution**: Run multiple simulations of Pac-Man with varying ghost numbers to gather performance data for each algorithm.
- **Statistical Comparison**: Utilize the paired Student's t-test to statistically analyze the performance differences between the agents on different game layouts.
- **Visualization**: Generate plots to visually compare the performance metrics of the agents, helping in identifying the best configurations under various conditions.

To initiate the testing and visualization process, we use the command: python testing.py


This project is based on the Pacman AI project developed at UC Berkeley. 
For more information on the original project, visit http://ai.berkeley.edu/project_overview.html
