import argparse
import transferHMS.envs
import joblib
import tensorflow as tf

from rllab.sampler.utils import rollout

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='Path to the snapshot file.')
    parser.add_argument('--max-path-length', '-l', type=int, default=None)
    parser.add_argument('--speedup', '-s', type=float, default=1)
    parser.add_argument('--deterministic', '-d', dest='deterministic',
                        action='store_true')
    parser.add_argument('--no-deterministic', '-nd', dest='deterministic',
                        action='store_false')
    parser.set_defaults(deterministic=True)

    args = parser.parse_args()

    with tf.Session() as sess:
        data = joblib.load(args.file)
        if 'algo' in data.keys():
            policy = data['algo'].policy
            env = data['algo'].env
        else:
            policy = data['policy']
            env = data['env']

        args.max_path_length = env.horizon if args.max_path_length is None else args.max_path_length

        with policy.deterministic(args.deterministic):
            env.wrapped_env.env.mujoco_render_frames = True
            while True:
                print("Starting new rollout")
                obs = env.reset()
                t = 0
                done = False
                while t < args.max_path_length and done is False:
                    env.wrapped_env.env.mj_render()
                    a = policy.get_action(obs)[0]
                    obs, r, done, ifo = env.step(a)
                    t = t + 1