nohup python train_sac.py --env dclaw_pose --scale_reward 1.0 --log_dir ./dclaw_pose_var1 --seed 0 2> log &
nohup python train_sac.py --env dclaw_pose --scale_reward 2.0 --log_dir ./dclaw_pose_var2 --seed 0 2> log &
nohup python train_sac.py --env dclaw_pose --scale_reward 3.0 --log_dir ./dclaw_pose_var3 --seed 0 2> log &
nohup python train_sac.py --env dclaw_pose --scale_reward 0.1 --log_dir ./dclaw_pose_var4 --seed 0 2> log &
nohup python train_sac.py --env dclaw_pose --scale_reward 0.5 --log_dir ./dclaw_pose_var5 --seed 0 2> log &
nohup python train_sac.py --env dclaw_pose --scale_reward 0.8 --log_dir ./dclaw_pose_var6 --seed 0 2> log &
