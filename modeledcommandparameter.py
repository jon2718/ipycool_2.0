from icoolobject import ICoolObject
import icool_exceptions as ie
import inspect
import sys

class ModeledCommandParameter(ICoolObject):

    def __modeled_command_parameter_setattr__(self, name, value, models):
        # Check whether the attribute being set is the model
        if name == self.get_model_descriptor_name(models):
            if self.check_valid_model(value, models) is False:
                return
            new_model = False
            
            # Check whether this is a new model (i.e. model was previously
            # defined)
            if hasattr(self, self.get_model_descriptor_name(models)):
                new_model = True

                # Delete all attributes of the current model
                print 'Resetting model to ', value
                self.reset_model(models)
            object.__setattr__(self, self.get_model_descriptor_name(models), value)

            # If new model, set all attributes of new model to 0.
            if new_model is True:
                self.set_and_init_params_for_model(value, models)
            return
        try:
            command_params_dict = self.get_model_parms_dict(models)
            if self.check_command_param_valid(name, command_params_dict):
                if self.check_command_param_type(name, value, command_params_dict):
                    object.__setattr__(self, name, value)
            else:
                raise ie.SetAttributeError('', self, name)
        except ie.InvalidType as e:
            print e
        except ie.SetAttributeError as e:
            print e

    def __str__(self):
        desc = 'ModeledCommandParameter\n'
        for key in self.get_model_dict(
            getattr(
                self,
                self.get_model_descriptor_name())):
            desc = desc + key + ': ' + str(getattr(self, key)) + '\n'
        return desc

    def set_keyword_args_model_specified(self, **kwargs):
        setattr(
            self,
            self.get_model_descriptor_name(),
            kwargs[
                self.get_model_descriptor_name()])
        for key in kwargs:
            if not key == self.get_model_descriptor_name():
                setattr(self, key, kwargs[key])

    def set_keyword_args_model_not_specified(self, **kwargs):
        for key in kwargs:
            object.__setattr__(self, key, kwargs[key])

    def reset_model(self, models):
        for key in self.get_model_parms_dict(models):
            if hasattr(self, key):
                delattr(self, key)

    def set_and_init_params_for_model(self, model, models):
        # Initializes all parameters for model to 0
        for key in self.get_model_dict(model, models):
            if key is not self.get_model_descriptor_name(models):
                setattr(self, key, 0)

    def check_command_params_init(self, models, **command_params):
        """
        Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError.
        If model is not specified, raises ModelNotSpecifiedError.
        Initialization of a model (e.g., Accel, SOL, etc. requires all keywords specified)
        """
        if self.check_no_model(models):
            return True
        if not self.check_model_specified(models, **command_params):
            return False
        else:
            if not self.check_valid_model(
                    self.get_model_name_in_dict(models, **command_params), models):
                return False
            else:
                command_params_dict = self.get_command_params_for_specified_input_model(models,
                    **command_params)
                if not self.check_command_params_valid(command_params_dict, **command_params) \
                    or not self.check_all_required_command_params_specified(command_params_dict, **command_params) \
                        or not self.check_command_params_type(command_params_dict, **command_params):
                            return False
                else:
                    self.__modeled_command_parameter_setattr__(
                    self.get_model_descriptor_name(models),
                    self.get_model_name_in_dict(models, **command_params),
                    models)
                del command_params[self.get_model_descriptor_name(models)]
                self.setall(self.get_model_parms_dict(models), **command_params)

                return True

    def check_command_params_call(self, command_params):
        """
        Checks to see whether new model specified in call.
        If so, checks that the parameters specified correspond to that model and raises an exception if they dont.
        Does NOT require all parameters specified for new model.  Unspecified parameters are set to 0.
        If model is not specified, checks whether the parameters specified correspond to the current model and
        raises an exception otherwise.
        """
        if not self.get_model_descriptor_name() in command_params.keys():
            command_params_dict = self.get_model_parms_dict()
            if not self.check_command_params_valid(command_params_dict, **command_params) \
                or not self.check_command_params_type(command_params, command_params_dict):
                    return False
            else:
                return True
        else:
            return self.check_command_params_init(command_params)

        def setall(self, command_params_dict, **command_params):
            for key in command_params:
                self.__modeled_command_parameter_setattr__(key, command_params[key], command_params_dict)

    def check_valid_model(self, model, models):
        """
        Checks whether model specified is valid.
        If model is not valid, raises an exception and returns False.  Otherwise returns True.
        """
        try:
            if not str(model) in self.get_model_names(models):
                raise ie.InvalidModel(str(model), self.get_model_names(models))
        except ie.InvalidModel as e:
            print e
            return False
        return True

    def check_partial_keywords_for_current_model(self, input_dict):
        """
        Checks whether the keywords specified for a current model correspond to that model.
        """
        actual_dict = self.get_model_dict(
            getattr(
                self,
                self.get_model_descriptor_name()))
        for key in input_dict:
            if key not in actual_dict:
                raise ie.InputArgumentsError(
                    'Input Arguments Error',
                    input_dict,
                    actual_dict)
        return True

    def check_partial_keywords_for_new_model(self, **input_dict):
        """
        Checks whether the keywords specified for a new model correspond to that model.
        """
        model = input_dict[self.get_model_descriptor_name()]
        actual_dict = self.get_model_dict(model)
        for key in input_dict:
            if key not in actual_dict:
                raise ie.InputArgumentsError(
                    'Input Arguments Error',
                    input_dict,
                    actual_dict)
        return True

    def check_model_specified(self, models, **input_dict):
        """
        Check whether the user specified a model in specifying parameters to Init or Call.
        if so, returns True.  Otherwise, raises an exception and returns False.
        """
        try:
            if not self.get_model_descriptor_name(models) in input_dict.keys():
                raise ie.ModelNotSpecified(self.get_model_names(models))
        except ie.ModelNotSpecified as e:
            print e
            return False
        return True

    def check_no_model(self, models):
        #Returns true if there is no model descriptor name for the models.
        if self.get_model_descriptor_name(models) is None:
            return True
        else:
            return False

    ##################################################
    # Helper functions
    ##################################################

    # Models is a dictionary of the following form:
    # {
    #       model_descriptor: {
    #           'desc': 'Name of model parameter descriptor',
    #           'name': ,
    #           'num_parms':,
    #           'for001_format': {
    #           'line_splits': }},

    #       }

    #        model_1: {

    #        ...

    #           parms: {

    #            }
    #        }

    #       model_2: {
    #            ....
    #            parms: {

    #           }

    #        }
    # }

    # Model Descriptor and Model Descriptor Name
    def get_model_descriptor(self, models):
        """Input:  Models dictionary
           Output: Models descriptor dictionary"""
        return models['model_descriptor']

    def get_model_descriptor_name(self, models):
        """
        The model descriptor name is an alias name for the term 'model', which is specified for each descendent class.
        Returns the current model descriptor name.
        """
        return self.get_model_descriptor(models)['name']

    def get_current_model_name(self, models):
        """Returns the name of the current model for a modeledcommandparameter object."""
        return getattr(self, self.get_model_descriptor_name(models))
    
    #Model Parameters
    def get_model_parms_dict(self, models):
        """
        Returns the parameter dictionary for the current model.
        """
        if self.get_model_descriptor_name(models) is None:
            return {}
        else:
            return self.get_model_dict(self.get_current_model_name(models), models)

    def get_model_dict(self, model, models):
        """
        Given a model and models dictionary, returns the parameter dictionary for model name.
        Input: (1) model and (2) models
        Output: Dictinoary of parameters
        """
        return models[str(model)]['parms']
  
    def get_num_params(self, models=None):
        """
        Returns the number of parameters for model.
        """
        if models is None:
            models = self.models
        return self.get_model_descriptor(models)['num_parms']

    def get_icool_model_name(self, models):
        """Check to see whether there is an alternate icool_model_name from the common name.
        If so return that.  Otherwise, just return the common name."""
        if 'icool_model_name' not in models[
                str(self.get_current_model_name(models))]:
            return self.get_current_model_name(models)
        else:
            return models[str(self.get_current_model_name(models))][
                'icool_model_name']

    def get_model_names(self, models):
        """Returns a list of all model names"""
        ret_list = models.keys()
        pos = ret_list.index('model_descriptor')
        del ret_list[pos]
        return ret_list

    def get_model_name_in_dict(self, models, **dict):
        """Returns the model name in a provided dictionary if it exists.  Otherwise returns None"""
        if self.get_model_descriptor_name(models) not in dict:
            return None
        else:
            return dict[self.get_model_descriptor_name(models)]

    def get_command_params_for_specified_input_model(
            self,
            models,
            **input_command_params):
        specified_model = input_command_params[
            self.get_model_descriptor_name(models)]
        return self.get_model_dict(specified_model, models)

    def get_line_splits(self, models=None):
        if models is None:
            models = self.models
        return self.models['model_descriptor']['for001_format']['line_splits']

    ##################################################

    def set_model_parameters(self):
        parms_dict = self.get_model_parms_dict(self.models)
        high_pos = 0
        for key in parms_dict:
            if key['pos'] > high_pos:
                high_pos = key['pos']
        self.parms = [0] * high_pos


    def gen_parm(self):
        models = self.models
        num_parms = self.get_num_params()
        command_params = self.get_model_parms_dict(self.models)
        parm = [0] * num_parms
        for key in command_params:
            pos = int(command_params[key]['pos']) - 1
            if key == self.get_model_descriptor_name(models):
                val = self.get_icool_model_name(models)
            else:
                val = getattr(self, key)
            parm[pos] = val
        return parm


    def get_command_params(self):
        return self.get_model_parms_dict(self.models)

    def gen_for001(self, file):
        models = self.models
        file.write(self.get_begtag())
        file.write('\n')
        parm = self.gen_parm()
        splits = self.get_line_splits()
        count = 0
        split_num = 0
        cur_split = splits[split_num]
        for i in parm:
            if count == cur_split:
                file.write('\n')
                count = 0
                split_num = split_num + 1
                cur_split = splits[split_num]
            file.write(str(i))
            file.write(' ')
            count = count + 1
        file.write('\n')
        if hasattr(self, 'endtag'):
            #file.write('\n')
            file.write(self.get_endtag())
            file.write('\n')

