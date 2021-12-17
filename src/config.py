
class Config:
    def __init__(self): 

        ### Self-Play 
        self.num_actors = 5000 

        self.num_sampling_moves = 30 
        self.max_moves = 512  # for chess and shogi, 722 for Go. 
        self.num_simulations = 800 

        # Root prior exploration noise. 
        self.root_dirichlet_alpha = 0.3  # for chess, 0.03 for Go and 0.15 for shogi. 
        self.root_exploration_fraction = 0.25 

        # UCB formula 
        self.pb_c_base = 19652 
        self.pb_c_init = 1.25 

        ### Training 
        self.training_steps = int(700e3)
        self.checkpoint_interval = int(1e3) 
        self.window_size = int(1e6) 
        self.batch_size = 4096 

        self.weight_decay = 1e-4 
        self.momentum = 0.9 

        self.min_depth = 6
        self.difference_offset = 4
        self.pruned_moves = 5
        
class GameConfig:
    def __init__(self):
        self.action_space = 4972 # action space for chess
        
class TrainConfig:
    def __init__(self):
        self.num_residual_blocks = 20
        
        self.dynamics_split = 10
        self.inference_split = self.num_residual_blocks - self.dynamics_split
        
        self.num_filters = 256
        self.first_kernel_size = 3
        
        self.kernel_size = 5
        
        self.num_update_residual_blocks = 5
        
        self.value_fc_size = 256