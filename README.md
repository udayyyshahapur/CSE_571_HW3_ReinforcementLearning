# Q-Learning Agents for Pacman

In this project, we compared the Semi-Gradient TD(Lambda) and True Online TD(Lambda) methods
with the Q-Learning method. The code includes several agent implementations, ApproximateQAgent, SemiGradientTDQAgent, and TrueOnlineTDQAgent.


# Setup Instructions

1. Ensure you have Python installed on your machine. Python 3.6.6 is recommended.
2. Clone this repository or download the files to your local environment.

# How To Run Code
1. python pacman.py -p TrueOnlineTDQAgent -a extractor=SimpleExtractor -x 200 -n 210 -l mediumClassic
2.   -p: Specifies the agent class to use. (ApproximateQAgent, TrueOnlineTDQAgent, SemiGradientTDQAgent)
    -a: Provides agent parameters (e.g., extractor, epsilon, gamma, alpha, lambda).
    -x: The number of training episodes.
    -n: The total number of episodes (including testing).
    -l: The Pacman game layout. (customLayoutHard/trickyLayout/capsuleClassic, Check out the layouts folder for more.)
    --frameTime: Adjusts the frame delay for visual output.


This project is based on the Pacman AI project developed at UC Berkeley. 
For more information on the original project, visit http://ai.berkeley.edu/project_overview.html.
