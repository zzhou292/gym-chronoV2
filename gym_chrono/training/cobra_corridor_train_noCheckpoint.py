import gymnasium as gym

from typing import Callable
import os

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.callbacks import BaseCallback


from gym_chrono.envs.driving.cobra_corridor import cobra_corridor


def make_env(rank: int, seed: int = 0) -> Callable:
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environment you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    :return: (Callable)
    """

    def _init() -> gym.Env:
        env = cobra_corridor()
        env.reset(seed=seed + rank)
        return env

    set_random_seed(seed)
    return _init


if __name__ == '__main__':
    # env = cobra_corridor()
    ####### PARALLEL ##################

    num_cpu = 8
    # Create the vectorized environment
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])

    model = PPO('MlpPolicy', env, learning_rate=1e-3, verbose=1).learn(2000000)

    mean_reward, std_reward = evaluate_policy(
        model, env, n_eval_episodes=100)
    print(f"mean_reward:{mean_reward:.2f} +/- {std_reward:.2f}")


###############################

####### SEQUENTIAL ##################
# model = PPO('MlpPolicy', env, verbose=1).learn(100)
###########################
# model.save(f"PPO_cobra")
# mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=100)
# print(f"mean_reward:{mean_reward:.2f} +/- {std_reward:.2f}")