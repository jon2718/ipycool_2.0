# -*- coding: utf-8 -*-
import sys
import icool_exceptions as ie
import inspect

class ICoolObject(object):

    """Generic ICOOL object providing methods for"""

    def __init__(self, **kwargs):
        pass

    def __call__(self, **kwargs):
        pass

    def __str__(self, return_str):
        command_parameters_dict = self.command_params
        for key in command_parameters_dict:
            if hasattr(self, key):
                return_str += '\n'
                return_str += key
                return_str += ': '
                return_str += str(getattr(self, key))
        return return_str

    def __repr__(self):
        return '[ICool Object]'

    def __icool_setattr__(self, name, value, command_params_dict = None):
        if command_params_dict is None:
            command_params_dict = self.get_all_ancestor_command_params()
        if (self.check_command_param_valid(name, command_params_dict) and
            self.check_command_param_type(name, value, command_params_dict)):
                object.__setattr__(self, name, value)

    def check_command_param_valid(self, command_param, command_params_dict):
        """
        Checks whether a specific parameter specified for command is valid.
        """
        try:
            if command_param not in command_params_dict:
                raise ie.InvalidCommandParameter(
                    command_param,
                    command_params_dict.keys())
        except ie.InvalidCommandParameter as e:
            print e
            return False
        except ie.InvalidType as e:
            print e
            return False
        return True

    """Checks whether all required command parameters specified in __init__ are provided are valid
    for the command.
    Valid means the parameters are recognized for the command, all required parameters are provided
    and the parameters are the correct type."""
    def check_command_params_valid(
            self,
            command_parameters_dict, **command_params):
        """Returns True if command_params are valid (correspond to the command)
        Otherwise raises an exception and returns False"""
        try:
            for key in command_params:
                if key not in command_parameters_dict:
                    raise ie.InvalidCommandParameter(
                        key,
                        command_parameters_dict)
        except ie.InvalidCommandParameter as e:
            print e
            return False
        return True

    def check_all_required_command_params_specified(
            self,
            command_parameters_dict,
            **command_params
            ):
        """Returns True if all required command parameters were specified
        Otherwise raises an exception and returns False"""
        try:
            for key in command_parameters_dict:
                if self.is_required(key, command_parameters_dict):
                    if key not in command_params:
                        raise ie.MissingCommandParameter(key, command_params)
        except ie.MissingCommandParameter as e:
            print e
            return False
        return True

    def check_command_params_type(self, command_params_dict, **command_params):
        """Checks to see whether all command parameters specified were of the correct type"""
        try:
            for key in command_params:
                if self.check_type(
                        command_params_dict[key]['type'],
                        command_params[key]) is False:
                    raise ie.InvalidType(
                        command_params_dict[key]['type'],
                        command_params[key].__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_param_type(self, name, value, command_params_dict):
        """Checks to see whether a particular command parameter of name with value is of the correct type"""
        try:
            if self.check_type(
                    command_params_dict[name]['type'],
                    value) is False:
                raise ie.InvalidType(
                    command_params_dict[name]['type'],
                    value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_init(self, command_params_dict=None, **kwargs):
        """
        Checks whether the parameters specified for command are valid, all required parameters are
        specified and all parameters are of correct type.  If not, raises an exception.
        """

        if command_params_dict is None:
            command_params_dict = self.get_all_ancestor_command_params()
        check_params = not self.check_command_params_valid(
            command_params_dict, **kwargs) or not self.check_all_required_command_params_specified(
            command_params_dict, **kwargs) or not self.check_command_params_type(
            command_params_dict, **kwargs)
        if check_params:
            return False
        else:
            self.setall(command_params_dict, **kwargs)
            return True

    def check_command_params_call(self, command_params_dict, **command_params):
        """
        Checks whether the parameters specified for command are valid and all required parameters exist.
        """
        return self.check_command_params_valid(command_params, command_params_dict) and\
            self.check_command_params_type(
            command_params,
            command_params_dict)

    def setall(self, command_params_dict, **command_params):
        for key in command_params:
            self.__icool_setattr__(key, command_params[key], command_params_dict)

    def setdefault(self, command_params_dict, **command_params):
        for key in command_params_dict:
            if key not in command_params:
                self.__setattr__(key, command_params_dict[key]['default'])

    def check_type(self, icool_type, provided_type):
        """Takes provided python object and compares with required icool type name.
        Returns True if the types match and False otherwise.
        """
        provided_type_name = provided_type.__class__.__name__
        #print icool_type, provided_type_name
        if icool_type == 'Float':
            if provided_type_name == 'int' or provided_type_name == 'long' or provided_type_name == 'float':
                return True
            else:
                return False

        if icool_type == 'Integer':
            if provided_type_name == 'int' or provided_type_name == 'long':
                return True
            else:
                return False

        if icool_type == 'Logical':
            if provided_type_name == 'bool':
                return True
            else:
                return False

        if icool_type == 'Field':
            if isinstance(provided_type, Field):
                return True
            else:
                return False

        if icool_type == 'Material':
            if isinstance(provided_type, Material):
                return True
            else:
                return False

        if icool_type == 'SubRegion':
            if isinstance(provided_type, SubRegion):
                return True
            else:
                return False

        if icool_type == 'Distribution':
            if isinstance(provided_type, Distribution):
                return True
            else:
                return False

        if icool_type == 'Correlation':
            if isinstance(provided_type, Correlation):
                return True
            else:
                return False
                  
        if icool_type == 'ICoolComposite':
            if isinstance(provided_type, ICoolComposite):
                return True
            else:
                return False

    def is_required(self, command_param, command_parameters_dict):
        if 'req' not in command_parameters_dict[command_param]:
            return True
        else:
            return command_parameters_dict[command_param]['req']

    def gen_parm(self):
        command_params = self.command_params
        #command_params = self.get_all_ancestor_command_params()
        parm = [None] * self.num_params
        for key in command_params:
            pos = int(command_params[key]['pos']) - 1
            val = getattr(self, key)
            parm[pos] = val
        return parm

    def for001_str_gen(self, value):
        if value.__class__.__name__ == 'bool':
            if value is True:
                return '.true.'
            else:
                return '.false.'
        else:
            return str(value)

    def get_begtag(self):
        return self.begtag
        
    def get_endtag(self):
        return self.endtag

    def get_line_splits(self):
        return self.for001_format['line_splits']

    def get_all_ancestor_command_params(self):
        ancestors = inspect.getmro(self.__class__)
        dall = {}
        for a in ancestors:
            if hasattr(a, 'command_params'):
                dall.update(a.command_params)
        return dall

    def get_all_ancestors(self):
        return map(self.name, inspect.getmro(self.__class__))

    def get_command_params(self):
        return self.command_params

    def name(self, cls):
        return cls.__name__

from field import Field
from material import Material
from distribution import Distribution
from correlation import Correlation
from subregion import SubRegion