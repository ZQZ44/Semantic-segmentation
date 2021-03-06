import os
import sys
import GPUtil
import argparse

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_args():
    """
    Returns a namedtuple with arguments extracted from the command line.
    :return: A namedtuple with arguments
    """
    parser = argparse.ArgumentParser(
        description='settings for the semantic segmentation')

    parser.add_argument('--batch_size', nargs="?", type=int, default=16, help='Batch_size for experiment')
    parser.add_argument('--num_class', nargs="?", type=int, default=21, help='Number of classes in dataset')
    parser.add_argument('--crop_size', nargs="?", type=int, default=513, help='crop_size for image')
    parser.add_argument('--continue_from_epoch', nargs="?", type=int, default=-1, help='continue option for experiment')
    parser.add_argument('--seed', nargs="?", type=int, default=7112018,
                        help='Seed to use for random number generator for experiment')
    parser.add_argument('--learn_rate', nargs="?", type=float, default=0.007, help='base learning rate') 
    parser.add_argument('--num_epochs', nargs="?", type=int, default=100, help='The experiment\'s epoch budget')
    parser.add_argument('--experiment_name', nargs="?", type=str, default="exp_1",
                        help='Experiment name - to be used for building the experiment folder')
    parser.add_argument('--use_gpu', nargs="?", type=str2bool, default=False,
                        help='A flag indicating whether we will use GPU acceleration or not')
    parser.add_argument('--mementum', nargs="?", type=float, default=0.9, help='mementum factor for SGD')
    parser.add_argument('--weight_decay', nargs="?", type=float, default=5e-4,
                        help='Weight decay to use for mementum')
    parser.add_argument('--output_stride', nargs="?", type=int, default=16,
                        help='The output_stride for the network')
    parser.add_argument('--aug', nargs="?", type=str2bool, default=True, help='weather use aug dataset')
    parser.add_argument('--newval', nargs="?", type=str2bool, default=True, help='weather use newval dataset')
    print(sys.argv)
    args = parser.parse_args()
    
    return args
