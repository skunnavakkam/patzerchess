
##### Evaluates the position, and outputs a chance of winning #####

import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

evaluation = models.Sequential()
evaluation.add(layers.Conv2D(
<<<<<<< Updated upstream
    256, (5, 5), activation="relu", input_shape=(8, 8, 18)))

def build_residual_blocks(x):
    
=======
    256, (5, 5), activation="relu", input_shape=(8, 8, 17)))
evaluation.add()
>>>>>>> Stashed changes
