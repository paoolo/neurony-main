import traceback

import re

__author__ = 'paoolo'

ENVIRONMENT = {}

import sys


def print_error(line):
    sys.stderr.write(line + '\n')


def interpret(line):
    line = line.split()
    if len(line) > 0:
        if re.match('echo', line[0]):
            print ' '.join(line[1:])
        else:
            try:
                command = commands[line[0]]
                try:
                    function, params = command['function'], command['params']
                    try:
                        kwargs = {key[0]: key[1](value) for (key, value) in zip(params, line[1:])}
                        try:
                            function(**kwargs)
                        except TypeError as e:
                            traceback.print_exc()
                            print_error('Internal error: Error during passing params to function: %s' % e)
                            print 'Usage: %s' % reduce(lambda acc, val: acc + ' ' + val[0], params, line[0])
                        except BaseException as e:
                            traceback.print_exc()
                            print_error('Internal error: Error during executing function: %s' % e)
                    except TypeError as e:
                        # traceback.print_exc()
                        print_error('Internal error: Error during parsing params: %s' % e)
                except KeyError as e:
                    # traceback.print_exc()
                    print_error('Internal error: No function/params descriptor: %s' % e)
            except KeyError as e:
                # traceback.print_exc()
                print 'Command "' + str(e.message) + '" not found.\nAvailable commands:\n\t%s' % reduce(
                        lambda acc, val: acc + '\n\t' + val, sorted(commands))


import command
import parser

commands = {
    'new_neuron': {
        'function': command.new_neuron,
        'params': [
            ('name', parser.parse_string),
            ('activation_func', parser.parse_activation_func),
            ('weights', parser.parse_floats),
            ('bias', parser.parse_float),
            ('location', parser.parse_ints)
        ],
    },
    'new_layer': {
        'function': command.new_layer,
        'params': [
            ('name', parser.parse_string),
            ('neurons', parser.parse_objects)
        ]
    },
    'new_network': {
        'function': command.new_network,
        'params': [
            ('name', parser.parse_string),
            ('layers', parser.parse_objects)
        ]
    },
    'new_kohonen': {
        'function': command.new_kohonen,
        'params': [
            ('name', parser.parse_string),
            ('kohonen_func', parser.parse_activation_func),
            ('inputs', parser.parse_int),
            ('width', parser.parse_int),
            ('height', parser.parse_int)
        ]
    },
    'new_cp': {
        'function': command.new_cp,
        'params': [
            ('name', parser.parse_string),
            ('kohonen_func', parser.parse_activation_func),
            ('grossberg_func', parser.parse_activation_func),
            ('inputs', parser.parse_int),
            ('outputs', parser.parse_int),
            ('width', parser.parse_int),
            ('height', parser.parse_int)
        ]
    },
    'init': {
        'function': command.init,
        'params': [
            ('name', parser.parse_string),
            ('min_value', parser.parse_float),
            ('max_value', parser.parse_float)
        ]
    },
    'init_bias': {
        'function': command.init_bias,
        'params': [
            ('name', parser.parse_string),
            ('min_value', parser.parse_float),
            ('max_value', parser.parse_float)
        ]
    },
    'zero': {
        'function': command.zero,
        'params': [
            ('name', parser.parse_string)
        ]
    },
    'zero_bias': {
        'function': command.zero_bias,
        'params': [
            ('name', parser.parse_string)
        ]
    },
    'locate': {
        'function': command.locate,
        'params': [
            ('name', parser.parse_string),
            ('location', parser.parse_ints)
        ]
    },
    'show_all': {
        'function': command.show_all,
        'params': []
    },
    'show': {
        'function': command.show,
        'params': [
            ('name', parser.parse_string)
        ]
    },
    'compute': {
        'function': command.compute,
        'params': [
            ('name', parser.parse_string),
            ('values', parser.parse_floats)
        ]
    },
    'compute_error': {
        'function': command.compute_error,
        'params': [
            ('name', parser.parse_string),
            ('values', parser.parse_floats),
            ('targets', parser.parse_floats)
        ]
    },
    'compute_normalize': {
        'function': command.compute_normalize,
        'params': [
            ('name', parser.parse_string),
            ('values', parser.parse_floats)
        ]
    },
    'compute_error_normalize': {
        'function': command.compute_error_normalize,
        'params': [
            ('name', parser.parse_string),
            ('values', parser.parse_floats),
            ('targets', parser.parse_floats)
        ]
    },
    'load': {
        'function': command.load,
        'params': [
            ('source', parser.parse_string)
        ]
    },
    'train_c': {
        'function': command.train_c,
        'params': [
            ('name', parser.parse_string),
            ('learning_rate', parser.parse_learning_rate_func),
            ('iterations', parser.parse_int),
            ('signals', parser.parse_signals)
        ]
    },
    'train_n': {
        'function': command.train_n,
        'params': [
            ('name', parser.parse_string),
            ('learning_rate', parser.parse_learning_rate_func),
            ('measurement', parser.parse_measurement_func),
            ('neighborhood_radius', parser.parse_neighborhood_func),
            ('iterations', parser.parse_int),
            ('signals', parser.parse_signals)
        ]
    },
    'train_c_cp': {
        'function': command.train_c,
        'params': [
            ('name', parser.parse_string),
            ('kohonen_learning_rate', parser.parse_learning_rate_func),
            ('grossberg_learning_rate', parser.parse_learning_rate_func),
            ('iterations', parser.parse_int),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals)
        ]
    },
    'train_n_cp': {
        'function': command.train_n,
        'params': [
            ('name', parser.parse_string),
            ('kohonen_learning_rate', parser.parse_learning_rate_func),
            ('measurement', parser.parse_measurement_func),
            ('neighborhood_radius', parser.parse_neighborhood_func),
            ('grossberg_learning_rate', parser.parse_learning_rate_func),
            ('iterations', parser.parse_int),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals)
        ]
    },
    'train_bp': {
        'function': command.train_bp,
        'params': [
            ('name', parser.parse_string),
            ('learning_rate', parser.parse_learning_rate_func),
            ('iterations', parser.parse_int),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals)
        ]
    },
    'train_bp_m': {
        'function': command.train_bp_m,
        'params': [
            ('name', parser.parse_string),
            ('learning_rate', parser.parse_learning_rate_func),
            ('momentum_rate', parser.parse_learning_rate_func),
            ('iterations', parser.parse_int),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals)
        ]
    },
    'multi_train_c': {
        'function': command.multi_train_c,
        'params': [
            ('name', parser.parse_string),
            ('signals', parser.parse_signals),
            ('configs', parser.parse_configs_c)
        ]
    },
    'multi_train_n': {
        'function': command.multi_train_n,
        'params': [
            ('name', parser.parse_string),
            ('signals', parser.parse_signals),
            ('configs', parser.parse_configs_n)
        ]
    },
    'multi_train_c_cp': {
        'function': command.multi_train_c_cp,
        'params': [
            ('name', parser.parse_string),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals),
            ('configs', parser.parse_configs_c_cp)
        ]
    },
    'multi_train_n_cp': {
        'function': command.multi_train_n_cp,
        'params': [
            ('name', parser.parse_string),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals),
            ('configs', parser.parse_configs_n_cp)
        ]
    },
    'multi_train_bp': {
        'function': command.multi_train_bp,
        'params': [
            ('name', parser.parse_string),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals),
            ('configs', parser.parse_configs_bp)
        ]
    },
    'multi_train_bp_m': {
        'function': command.multi_train_bp_m,
        'params': [
            ('name', parser.parse_string),
            ('signals', parser.parse_signals),
            ('targets', parser.parse_signals),
            ('configs', parser.parse_configs_bp_m)
        ]
    }
}
