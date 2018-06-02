import argparse
import transferHMS.envs

from rllab.envs.normalized_env import normalize
from rllab.misc.instrument import VariantGenerator

from sac.algos import SAC
from sac.envs.gym_env import GymEnv
from sac.misc.instrument import run_sac_experiment
from sac.misc.utils import timestamp
from sac.misc.sampler import SimpleSampler
from sac.policies.gmm import GMMPolicy
from sac.replay_buffers import SimpleReplayBuffer
from sac.value_functions import NNQFunction, NNVFunction


SHARED_PARAMS = {
    "lr": 3E-4,
    "discount": 0.99,
    "tau": 0.01,
    "K": 4,
    "layer_size": 128,
    "batch_size": 128,
    "max_pool_size": 1E6,
    "n_train_repeat": 1,
    #"epoch_length": 1000,
    "snapshot_mode": 'gap',
    "snapshot_gap": 100,
    "sync_pkl": True,
}

ENV_PARAMS = {
    'allegro_pose': {
        'prefix': 'allegro_pose',
        'env_name': 'allegro_pose-v0',
        'max_path_length': 200,
        'n_epochs': 250,
        'scale_reward': 2.0,
        'epoch_length': 400,
    },

    'dclaw_pose': {
        'prefix': 'dclaw_pose',
        'env_name': 'dclaw_pose-v0',
        'max_path_length': 200,
        'n_epochs': 25,
        'scale_reward': 2.0,
        'epoch_length': 400,
    },

    'dclaw_track': {
        'prefix': 'dclaw_track',
        'env_name': 'dclaw_track-v1',
        'max_path_length': 200,
        'n_epochs': 50,
        'scale_reward': 2.0,
        'epoch_length': 400,
    },
}

DEFAULT_ENV = 'dclaw_pose'
AVAILABLE_ENVS = list(ENV_PARAMS.keys())

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--env',
                        type=str,
                        choices=AVAILABLE_ENVS,
                        default=DEFAULT_ENV)
    parser.add_argument('--exp_name',type=str, default=timestamp())
    parser.add_argument('--mode', type=str, default='local')
    parser.add_argument('--log_dir', type=str, default=None)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--scale_reward', default=None)
    args = parser.parse_args()
    return args


def get_variants(args):
    env_params = ENV_PARAMS[args.env]
    params = SHARED_PARAMS
    params["seed"] = args.seed
    if args.scale_reward is not None:
        params["scale_reward"] = args.scale_reward
    params.update(env_params)
    vg = VariantGenerator()
    for key, val in params.items():
        if isinstance(val, list):
            vg.add(key, val)
        else:
            vg.add(key, [val])

    return vg


def run_experiment(variant):
    #if variant['env_name'] == 'humanoid-rllab':
    #    from rllab.envs.mujoco.humanoid_env import HumanoidEnv
    #    env = normalize(HumanoidEnv())
    #elif variant['env_name'] == 'swimmer-rllab':
    #    from rllab.envs.mujoco.swimmer_env import SwimmerEnv
    #    env = normalize(SwimmerEnv())
    #else:
    #    env = normalize(GymEnv(variant['env_name']))

    env = normalize(GymEnv(variant['env_name']))

    # import mujoco_envs
    # env = normalize(GymEnv('Peg-v2'))

    pool = SimpleReplayBuffer(
        env_spec=env.spec,
        max_replay_buffer_size=variant['max_pool_size'],
    )

    sampler = SimpleSampler(
        max_path_length=variant['max_path_length'],
        min_pool_size=variant['max_path_length'],
        batch_size=variant['batch_size']
    )

    base_kwargs = dict(
        sampler=sampler,
        epoch_length=variant['epoch_length'],
        n_epochs=variant['n_epochs'],
        n_train_repeat=variant['n_train_repeat'],
        eval_render=False,
        eval_n_episodes=1,
        eval_deterministic=True,
    )

    M = variant['layer_size']
    qf1 = NNQFunction(
        env_spec=env.spec,
        hidden_layer_sizes=[M, M],
        # input_skip_connections=variant['input_skip_connections'],
        name='qf1',
    )
    
    qf2 = NNQFunction(
        env_spec=env.spec,
        hidden_layer_sizes=[M, M],
        # input_skip_connections=variant['input_skip_connections'],
        name='qf2',
    )

    vf = NNVFunction(
        env_spec=env.spec,
        hidden_layer_sizes=[M, M],
    )

    policy = GMMPolicy(
        env_spec=env.spec,
        K=variant['K'],
        hidden_layer_sizes=[M, M],
        qf=qf1,
        reg=0.001,
    )

    algorithm = SAC(
        base_kwargs=base_kwargs,
        env=env,
        policy=policy,
        pool=pool,
        qf1=qf1,
        qf2=qf2,
        vf=vf,

        lr=variant['lr'],
        scale_reward=variant['scale_reward'],
        discount=variant['discount'],
        tau=variant['tau'],

        save_full_state=False,
    )

    algorithm.train()


def launch_experiments(variant_generator):
    variants = variant_generator.variants()

    for i, variant in enumerate(variants):
        print('Launching {} experiments.'.format(len(variants)))
        run_sac_experiment(
            run_experiment,
            mode=args.mode,
            variant=variant,
            exp_prefix=variant['prefix'] + '/' + args.exp_name,
            exp_name=variant['prefix'] + '-' + args.exp_name + '-' + str(i).zfill(2),
            n_parallel=1,
            seed=variant['seed'],
            terminate_machine=True,
            log_dir=args.log_dir,
            snapshot_mode=variant['snapshot_mode'],
            snapshot_gap=variant['snapshot_gap'],
            sync_s3_pkl=variant['sync_pkl'],
        )

if __name__ == '__main__':
    args = parse_args()
    variant_generator = get_variants(args)
    launch_experiments(variant_generator)

