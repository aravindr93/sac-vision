nohup python train_sac.py --env allegro_screw --scale_reward 1.0 --log_dir ./allegro_screw_var_1_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 1.0 --log_dir ./allegro_screw_var_1_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 1.0 --log_dir ./allegro_screw_var_1_2 --seed 2 2> log &
#
nohup python train_sac.py --env allegro_screw --scale_reward 10.0 --log_dir ./allegro_screw_var_10_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 10.0 --log_dir ./allegro_screw_var_10_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 10.0 --log_dir ./allegro_screw_var_10_2 --seed 2 2> log &
#
nohup python train_sac.py --env allegro_screw --scale_reward 100.0 --log_dir ./allegro_screw_var_1e2_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 100.0 --log_dir ./allegro_screw_var_1e2_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 100.0 --log_dir ./allegro_screw_var_1e2_2 --seed 2 2> log &
#
nohup python train_sac.py --env allegro_screw --scale_reward 1000.0 --log_dir ./allegro_screw_var_1e3_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 1000.0 --log_dir ./allegro_screw_var_1e3_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 1000.0 --log_dir ./allegro_screw_var_1e3_2 --seed 2 2> log &
#
nohup python train_sac.py --env allegro_screw --scale_reward 0.1 --log_dir ./allegro_screw_var_1e-1_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 0.1 --log_dir ./allegro_screw_var_1e-1_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 0.1 --log_dir ./allegro_screw_var_1e-1_2 --seed 2 2> log &
#
nohup python train_sac.py --env allegro_screw --scale_reward 0.01 --log_dir ./allegro_screw_var_1e-2_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 0.01 --log_dir ./allegro_screw_var_1e-2_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 0.01 --log_dir ./allegro_screw_var_1e-2_2 --seed 2 2> log &
#
nohup python train_sac.py --env allegro_screw --scale_reward 0.001 --log_dir ./allegro_screw_var_1e-3_0 --seed 0 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 0.001 --log_dir ./allegro_screw_var_1e-3_1 --seed 1 2> log &
nohup python train_sac.py --env allegro_screw --scale_reward 0.001 --log_dir ./allegro_screw_var_1e-3_2 --seed 2 2> log &
