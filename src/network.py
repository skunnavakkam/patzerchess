from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, Add
from tensorflow.keras import models, layers
from tensorflow import keras
from game import Board
import numpy
from config import TrainConfig


def build_residual_block(config: TrainConfig, x, index):

    in_x = x

    x = Conv2D(
        filters=config.num_filters,
        kernel_size=config.kernel_size,
        data_format="channels_first",
    )(x)
    x = BatchNormalization(axis=1)(x)
    x = Activation("relu")(x)
    x = Conv2D(
        filters=config.num_filters,
        kernel_size=config.kernel_size,
        data_format="channels_first",
    )(x)
    x = BatchNormalization(axis=1)(x)
    x = Add()([in_x, x])
    x = Activation("relu")(x)

    return x


class Network:
    def __init__(self, config: TrainConfig):
        self.config = config
        self.pv_model = None
        self.dynamics_model = None
        self.update_model = None

        input_size = (8, 8, 11)

        in_x = x = keras.Input(input_size)

        x = Conv2D(
            filters=config.num_filters,
            kernel_size=config.first_kernel_size,
            data_format="channels_first",
        )(x)
        x = BatchNormalization(axis=1)(x)
        x = Activation("relu")(x)

        pv = dynamics = x

        for i in range(config.num_residual_blocks):
            pv = build_residual_block(config, pv, i)

        for i in range(config.dynamics_split):
            dynamics = build_residual_block(config, dynamics, i)

        x = Conv2D(
            filters=2, kernel_size=1, data_format="channels_first", use_bias=False
        )(pv)
        x = BatchNormalization(axis=1)(x)
        x = Activation("relu")(x)
        x = layers.Flatten()(x)
        policy = layers.Dense(config.move_space, Activation="softmax")(x)

        x = Conv2D(
            filters=4,
            kernel_size=1,
            data_format="channels_first",
            use_bias=False,
            name="value_conv-1-4",
        )(pv)
        x = BatchNormalization(axis=1, name="value_batchnorm")(x)
        x = Activation("relu", name="value_relu")(x)
        x = layers.Flatten(name="value_flatten")(x)
        x = layers.Dense(config.value_fc_size, Activation="relu", name="value_dense")(x)
        value = layers.Dense(1, Activation="tanh", name="value_out")(x)

        self.pv_model = keras.Model(in_x, [policy, value])

        update = x = keras.Input(
            8, 8, 14
        )  # additional two input planes for start and end location of pieces
        x = Conv2D(
            filters=config.num_filters,
            kernel_size=config.first_kernel_size,
            data_format="channels_first",
        )(x)
        x = BatchNormalization(axis=1)(x)
        x = Activation("relu")(x)

        for i in range(config.num_update_residual_blocks):
            x = build_residual_block(config, x, i)

        x = Conv2D(filters=128, kernel_size=2)

        self.dynamics_model = keras.Model(in_x, dynamics)

        self.update_model = keras.Model(update, x)


Network(TrainConfig())
