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


class CheckpointCallback(BaseCallback):
    def __init__(self, save_freq, save_path, verbose=1):
        super(CheckpointCallback, self).__init__(verbose)
        self.save_freq = save_freq  # Number of training iterations between checkpoints
        self.save_path = save_path  # Directory to save checkpoints

    def _on_step(self) -> bool:
        if self.num_timesteps % self.save_freq == 0:
            self.model.save(os.path.join(
                self.save_path, f"ppo_checkpoint_{self.num_timesteps}"))
        return True


if __name__ == '__main__':
    # env = cobra_corridor()
    ####### PARALLEL ##################

    num_cpu = 12
    # Create the vectorized environment
    env = SubprocVecEnv([make_env(i) for i in range(num_cpu)])

    model = PPO('MlpPolicy', env, learning_rate=1e-3, verbose=1)

    for i in range(100):
        print(i)
        model.learn(30000)
        checkpoint_dir = 'ppo_checkpoints'
        os.makedirs(checkpoint_dir, exist_ok=True)
        model.save(os.path.join(checkpoint_dir, f"ppo_checkpoint{i}"))
        model = PPO.load(os.path.join(
            checkpoint_dir, f"ppo_checkpoint{i}"), env)

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
