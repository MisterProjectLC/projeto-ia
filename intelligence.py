import numpy as np
from tqdm import tqdm
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import pickle
from matplotlib import style
import time, os

style.use("ggplot")

DEATH_PENALTY = 300            # penalty the agent gets for getting in contact with the virus.
PROGRESS_REWARD = 100          # reward the agent gets for finding the bottle of beer.
epsilon = 0.9                  # takes care of the Exploitation-Exploration Tradeoff.
EPS_DECAY = 0.9998             # every self.episode will be epsilon*EPS_DECAY
SHOW_EVERY = 2000              # how often to play through env visually.

LEARNING_RATE = 0.1            # learning rate for updating the q-table 
DISCOUNT = 0.95                # the discount factor



class Intelligence:
    def __init__(self, width, height, image_count, action_count):
        self.width = width
        self.height = height
        self.image_count = image_count
        self.action_count = action_count
        self.episode = 0
        self.episode_rewards = []
        self.q_table = {}
        self.obs = None
        self.action = 1
        
        


    def evaluate_action(self, images):
        self.episode += 1

        if self.episode % SHOW_EVERY == 0:
            print(f"on #{self.episode}, epsilon is {epsilon}")
            print(f"{SHOW_EVERY} ep mean: {np.mean(self.episode_rewards[-SHOW_EVERY:])}")

        self.obs = images
            
        # Exploit
        if np.random.random() > epsilon:
            self.action = self.q_table[self.obs].index(max(self.q_table[self.obs]))
        # Explore
        else:
            self.action = np.random.randint(0, self.action_count-1)

        return self.action



    def receive_reward(self, is_game_over):
        reward = 0
        if is_game_over:
            reward = -DEATH_PENALTY
        else:
            reward = PROGRESS_REWARD
            
        

        if reward == PROGRESS_REWARD:
            new_q = PROGRESS_REWARD
        else:
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)
        self.q_table[self.obs][self.action] = new_q

        self.episode_reward = reward

        self.episode_rewards.append(self.episode_reward)
        epsilon *= EPS_DECAY


    def show_results(self):
        
