import os
import argparse
from datetime import datetime
import gym
from dm_control import suite

from env.dm_control import PixelObservationsDmControlWrapper
from agent import SlacAgent


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env_id', type=str, default='HalfCheetah-v2')
    parser.add_argument('--cuda', action='store_true')
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()

    # You can define configs in the external json or yaml file.
    configs = {
        'num_steps': 3000000,
        'batch_size': 256,
        'lr': 0.0003,
        'hidden_units': [256, 256],
        'memory_size': 1e6,
        'gamma': 0.99,
        'tau': 0.005,
        'entropy_tuning': True,
        'ent_coef': 0.2,  # It's ignored when entropy_tuning=True.
        'grad_clip': None,
        'updates_per_step': 1,
        'start_steps': 10000,
        'log_interval': 10,
        'target_update_interval': 1,
        'eval_interval': 10000,
        'cuda': args.cuda,
        'seed': args.seed
    }

    env = suite.load(domain_name="cheetah", task_name="run")
    env = PixelObservationsDmControlWrapper(env)

    # env = gym.make(args.env_id)
    # env = PixelObservationsDmControlWrapper(env)

    log_dir = os.path.join(
        'logs', args.env_id,
        f'slac-seed{args.seed}-{datetime.now().strftime("%Y%m%d-%H%M")}')

    agent = SlacAgent(env=env, log_dir=log_dir, **configs)
    agent.run()


if __name__ == '__main__':
    run()