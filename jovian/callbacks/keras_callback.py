from keras.backend import get_value
from keras.callbacks import Callback

from jovian import log_hyperparams, log_metrics


class KerasCallback(Callback):
    """Keras Callback to log hyperparameters and metrics during model training.

    Arguments:
        arch_name :  A name for the architecture that you're using
    """

    def __init__(self, arch_name):
        self.arch_name = arch_name

    def on_train_begin(self, logs=None):
        hyp_dict = {
            'arch_name': self.arch_name,
            'epochs': self.params['epochs'],
            'batch_size': self.params['batch_size'],
            'loss_func': self.model.loss,
            'opt_func': str(self.model.optimizer.__class__).split("'")[1],
            'weight_decay': self.model.optimizer.initial_decay,
            'learning_rate': str(get_value(self.model.optimizer.lr))
        }
        log_hyperparams(hyp_dict, verbose=False)

    def on_epoch_end(self, epoch, logs):
        met_dict = {
            'epoch': epoch
        }
        # logs here is a list that contains all the metrics
        for key, value in logs.items():
            logs[key] = round(value, 4)
        met_dict.update(logs)
        log_metrics(met_dict, verbose=False)