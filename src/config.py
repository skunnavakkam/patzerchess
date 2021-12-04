
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

        # minimum depth that the engine will calculate to
        self.min_depth = 6