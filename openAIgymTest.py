import gym
import numpy as np

env = gym.make('FrozenLake-v0')
#
# env.reset()
# env.render()
#
# print env.step(1)
# env.render()
#
# env.step(1)
# env.render()
#
# env.step(2)
# env.render()
#
# env.step(2)
# env.render()
#
# env.step(1)
# env.render()
#
# env.step(2)
# env.render()
#
# exit()


# for every state (row), put a Q value on every possible action (col)
Q = np.zeros([env.observation_space.n, env.action_space.n])

# learning params
lr = .8
y = .95
num_episodes = 5000

# reward list, for each episode
rList = []

for i in range(num_episodes):
    # Reset environment and get first new observation
    s = env.reset()
    # s = np.random.randint(env.observation_space.n)
    rAll = 0
    d = False
    j = 0
    # the Q-table learning algorithm
    while j < 99:
        j += 1
        # Choose an action by greedily (with noise) picking from Q table
        a = np.argmax(Q[s, :] + np.random.randn(1, env.action_space.n) * (1. / (i + 1)))
        # Get new state and reward from environment
        s1, r, d, _ = env.step(a)
        # Update Q-Table with new knowledge
        Q[s, a] = Q[s, a] + lr * (r + y * np.max(Q[s1, :]) - Q[s, a])
        rAll += r
        s = s1
        if d == True:
            break
    rList.append(rAll)

print "Score over time:", str(sum(rList) / num_episodes)
print "Final Q-table values"
print Q

state = env.reset()
print "state:", state
env.render()
done = False
stepcount = 0
while not done:
    action = np.argmax(Q[state, :])
    print "action:", action
    state, reward, done, info = env.step(action)
    print "state:", state
    print Q[state,:]
    env.render()
    stepcount+=1
    if stepcount%10 ==0:
        print "Steps so far:",stepcount

env.render()

"""
env = gym.make("Taxi-v2")

env.reset()

print env.observation_space.n

env.render()

print env.action_space.n

env.env.s = 114
env.render()

print "manuall step", env.step(1)
# (14, -1, False, {'prob': 1.0})
# state, reward, done, info
# These four variables are: the new state (St+1 = 14), reward (Rt+1 = -1), a boolean stating whether the environment is terminated or done, and extra info for debugging.
env.render()

print "random action", env.action_space.sample()
env.render()  # to visualize

state = env.reset()
counter = 0
reward = None
while reward != 20:
    state, reward, done, info = env.step(env.action_space.sample())
    counter += 1
print "Number of random steps:", counter

# Q learning
import numpy as np

# action value table (the values for each position?)
Q = np.zeros([env.observation_space.n, env.action_space.n])

# total accumulated reward for each episode
G = 0

# learning rate
alpha = 0.618

for episode in range(1,1001):
    done = False
    G,reward =0,0
    state = env.reset()
    while not done:
        action = np.argmax(Q[state])
        state2, reward, done, info = env.step(action)
        Q[state,action]+=alpha *(reward +np.max(Q[state2]) - Q[state,action])
        G+=reward
        state = state2
        if episode %50 ==0 :
            print('Episode {} Total Reward: {}'.format(episode, G))
"""
