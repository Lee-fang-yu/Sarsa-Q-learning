import sys
import gym
import itertools
import numpy as np
from collections import defaultdict

def epsilon_greedy_policy(Q, epsilon, num_of_action):
    """
    Description:
        Epsilon-greedy policy based on a given Q-function and epsilon.
        Don't need to modify this :) 
    """
    def policy_fn(obs):
        A = np.ones(num_of_action, dtype=float) * epsilon / num_of_action
        best_action = np.argmax(Q[obs])
        A[best_action] += (1.0 - epsilon)
        return A
    
    return policy_fn

def q_learning(env, num_episodes, discount_factor=1.0, alpha=0.5, epsilon=0.1):
    """
    Q-Learning algorithm: Off-policy TD control.

    Inputs:
        env: Environment object.
        num_episodes: Number of episodes to run for.
        discount_factor: Gamma discount factor.
        alpha: TD learning rate.
        epsilon: Chance the sample a random action.

    Returns:
        Q: the optimal action-value function, a dictionary mapping state -> action values.
        episode_rewards: reward array for every episode
        episode_lengths: how many time steps be taken in each episode
    """

    # A nested dictionary that maps state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.action_space.n))

    # Keeps track of useful statistics
    episode_lengths = np.zeros(num_episodes)
    episode_rewards = np.zeros(num_episodes)

    # The policy we're following
    policy = epsilon_greedy_policy(Q, epsilon, env.action_space.n)
    
    # start training
    for i_episode in range(num_episodes):
        # Reset the environment and pick the first action
        state = env.reset()

        for t in itertools.count():
            #Raise NotImplementedError('Q-learning NOT IMPLEMENTED')
            #Choose action from state using policy derived from Q (epsilon greedy)
            action_probs = policy(state)
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            #Derived next state and reward from action we chose
            next_state=env.P[state][action][0][1]
            reward=env.P[state][action][0][2]
            #Calculate the sum of episode rewards and episode lengths
            episode_rewards[i_episode] += reward
            episode_lengths[i_episode] += 1
            #Derived "is done" from action we chose
            is_done = env.P[state][action][0][3]
            #Accoring to "a" to choose the max Q(next state,a) 
            a=np.max(Q[next_state])
            #Update Q(state,action)
            Q[state][action] += alpha*(reward+ discount_factor*a-Q[state][action])
            #Update state
            state=next_state
            #If the episode reach goal we stop loop and break
            if(is_done == True):
                break
    #Return Q, episode_rewards, episode_lengths
    return Q, episode_rewards, episode_lengths

def sarsa(env, num_episodes, discount_factor=1.0, alpha=0.5, epsilon=0.1):
    """
    SARSA algorithm: On-policy TD control.

    Inputs:
        env: environment object.
        num_episodes: Number of episodes to run for.
        discount_factor: Gamma discount factor.
        alpha: TD learning rate.
        epsilon: Chance the sample a random action. Float betwen 0 and 1.

    Returns:
        Q is the optimal action-value function, a dictionary mapping state -> action values.
        episode_rewards: reward array for every episode
        episode_lengths: how many time steps be taken in each episode
    """
    # A nested dictionary that maps state -> (action -> action-value).
    Q = defaultdict(lambda: np.zeros(env.action_space.n))

    # Keeps track of useful statistics
    episode_lengths = np.zeros(num_episodes)
    episode_rewards = np.zeros(num_episodes)

    # The policy we're following
    policy = epsilon_greedy_policy(Q, epsilon, env.action_space.n)

    for i_episode in range(num_episodes):
        # Reset the environment and pick the first action
        state = env.reset()
        #Choose action from state using policy derived from Q (epsilon greedy)
        action_probs = policy(state)
        action = np.random.choice(np.arange(len(action_probs)), p=action_probs)

        for t in itertools.count():
            #raise NotImplementedError('SARSA NOT IMPLEMENTED')
            #Derived next state and reward from action we chose
            next_state=env.P[state][action][0][1]
            reward=env.P[state][action][0][2]
            #Calculate the sum of episode rewards and episode lengths
            episode_rewards[i_episode] += reward
            episode_lengths[i_episode] += 1
            #Derived "is done" from action we chose
            is_done = env.P[state][action][0][3]
            #Choose next action from next state using policy derived from Q (epsilon greedy)
            next_action_probs = policy(next_state)
            next_action = np.random.choice(np.arange(len(next_action_probs)), p=next_action_probs)
            #Update Q(state,action)
            b=Q[next_state][next_action]
            Q[state][action] += alpha*(reward+ discount_factor*b-Q[state][action])
            #Update state
            state=next_state
            #Update action
            action=next_action
            #If the episode reach goal we stop loop and break
            if(is_done == True):
                break
    #Return Q, episode_rewards, episode_lengths
    return Q, episode_rewards, episode_lengths
