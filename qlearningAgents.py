# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        "*** YOUR CODE HERE ***"
        self.qValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.qValues[(state, action)]
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        if not legalActions:
          return 0.0
        return max(self.getQValue(state, action) for action in legalActions)
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return None
        
        maxQValue = float('-inf')
        bestActions = []
        for action in legalActions:
            qValue = self.getQValue(state, action)
            if qValue > maxQValue:
                maxQValue = qValue
                bestActions = [action]
            elif qValue == maxQValue:
                bestActions.append(action)
        return random.choice(bestActions)
        util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if util.flipCoin(self.epsilon): 
            action = random.choice(legalActions)
        else:  
            action = self.computeActionFromQValues(state)
        return action
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        val = reward + self.discount * self.computeValueFromQValues(nextState)
        self.qValues[(state, action)] = (1 - self.alpha) * self.getQValue(state, action) + self.alpha * val
        return
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.01,gamma=0.9,alpha=0.0001, numTraining=0,lambda_=0.8, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.gamma = gamma
        self.lambda_=lambda_
        self.index = 0  # This is always Pacman
        self.z = {}
        self.Vold=0 
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        qValue = sum(self.weights[feature] * features[feature] for feature in features)
        return qValue
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        correction = (reward + self.discount * self.getValue(nextState)) - self.getQValue(state, action)
    
        for feature in features:
          self.weights[feature] += self.alpha * correction * features[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print("Final weights:", self.weights)
            pass


class SemiGradientTDQAgent(PacmanQAgent):
    def __init__(self, extractor='SimpleExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        qValue = sum(self.weights[feature] * features[feature] for feature in features)
        return qValue
        util.raiseNotDefined()
    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return None
        maxQValue = float('-inf')
        bestActions = []
        action=None
        if random.random() < self.epsilon:  # Exploration: Random action
          action = random.choice(legalActions)
        else:
            for action in legalActions:
                qValue = self.getQValue(state, action)
                if qValue > maxQValue:
                    maxQValue = qValue
                    bestActions = [action]
                elif qValue == maxQValue:
                    bestActions.append(action)
            action=random.choice(bestActions)
            self.doAction(state,action)
        return action
    
    def nextBestQValue(self, state,nextState):
        legalActions = self.getLegalActions(state)
        if random.random() < self.epsilon:  # Exploration: Random action
            random_action = random.choice(legalActions)
            return self.getQValue(state, random_action)
        else:
            return max(
            [self.getQValue(nextState, a) for a in legalActions],
            default=0,
            )
      
    def updateWeights(self, state, action, nextState,reward):
        bestNextQvalue = self.nextBestQValue(state,nextState)
        # Calculate the temporal difference (TD) error
        td_error = reward + self.gamma * bestNextQvalue - self.getQValue(state, action)

        features = self.featExtractor.getFeatures(state, action)
        #Update trace vector with semi-gradient TD logic
        for feature in features:
            self.z[feature] = self.gamma * self.lambda_ * self.z.get(feature, 0) + features[feature]
        
        #Update weights vector
        for feature in features:
            if feature not in self.weights:
                self.weights[feature] = 0
            self.weights[feature] += self.alpha * td_error * self.z[feature]

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        self.updateWeights(state, action, nextState,reward)

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print("Final weights:", self.weights)
            pass


class TrueOnlineTDQAgent(PacmanQAgent):
    def __init__(self, extractor='SimpleExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        qValue=0
        features = self.featExtractor.getFeatures(state, action)
        qValue = sum(self.weights[feature] * features[feature] for feature in features)
        return qValue
        util.raiseNotDefined()

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        if not legalActions:
            return None
        maxQValue = float('-inf')
        bestActions = []
        action=None
        if random.random() < self.epsilon:  # Exploration: Random action
            action = random.choice(legalActions)
        else:
            for action in legalActions:
                qValue = self.getQValue(state, action)
                if qValue > maxQValue:
                    maxQValue = qValue
                    bestActions = [action]
                elif qValue == maxQValue:
                    bestActions.append(action)
            action=random.choice(bestActions)
        self.doAction(state,action)
        return action
    
    def nextBestQValue(self, state,nextState):
        legalActions = self.getLegalActions(state)
        if random.random() < self.epsilon:  # Exploration: Random action
            random_action = random.choice(legalActions)
            return self.getQValue(state, random_action)
        else:
            return max(
            [self.getQValue(nextState, a) for a in legalActions],
            default=0,
            )
        
    def updateWeights(self, state, action, nextState,reward):
        V = self.getQValue(state, action)
        V_prime = self.nextBestQValue(state,nextState)
        td_error = reward + self.gamma * V_prime-V

        # Update the eligibility trace  
        features = self.featExtractor.getFeatures(state, action)
        for feature in features:
            if feature not in self.z:
                self.z[feature] = 0
        zTx = sum(self.z[feature] * features[feature] for feature in features)

        for feature in features:
            t1=self.gamma * self.lambda_ * self.z[feature]
            t2= (1 - self.alpha * self.gamma * self.lambda_ * zTx) * features[feature]
            self.z[feature]=t1+t2

      # Update Weights with True Online TD(λ) logic
        for feature in features:
            if feature not in self.weights:
                self.weights[feature] = 0
            w1= self.alpha * (td_error + V - self.Vold) * self.z[feature]
            w2= self.alpha * (V - self.Vold) * features[feature]
            self.weights[feature]+=w1-w2
        self.Vold=V_prime
        

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        self.updateWeights(state, action, nextState,reward)

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            print("Final weights:", self.weights)
            pass
