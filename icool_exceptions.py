def valid_command(command_dict, command, value, namelist):
    """
    Checks whether command is valid in the following respects:
        (1) It is a valid variable for a namelist;
        (2) The type assigned to the variable is the correct type.
    """
    try:
        if command in command_dict.keys():
            dictionary_entry = command_dict[command]
            command_type = dictionary_entry['type']
            try:
                if check_type(command_type, value.__class__.__name__):
                    return 0
                else:
                    raise IncorrectType('Incorrect type', command_type, value.__class__.__name__)
            except IncorrectType as e:
                print e
                return -1
        else:
            raise UnknownVariable('Unknown variable', command, namelist)
    except UnknownVariable as e:
        print e
        return -1


def check_namelists(title, cont, bmt, ints, nhs, nsc, nzh, nrh, nem, ncv, sec, name, metadata):
    """
    Checks namelists are correct type.
    """
    try:
        if cont is not None and cont.__class__.__name__ is not 'Cont':
            raise NamelistObjectTypeError('Namelist object type error', cont, 'Cont')
        if sec is not None and sec.__class__.__name__ is not 'Section':
            raise NamelistObjectTypeError('Namelist object type error', sec, 'Section')
    except NamelistObjectTypeError as e:
        print e
        return -1


def check_type(icool_type, provided_type):
    """Checks types comparing ICOOL required types with python types
    """
    if icool_type == 'Real':
        if provided_type == 'int' or provided_type == 'long' or provided_type == 'float':
            return True
        else:
            return False

    if icool_type == 'Integer':
        if provided_type == 'int' or provided_type == 'long':
            return True
        else:
            return False

    if icool_type == 'Logical':
        if provided_type == 'bool':
            return True
        else:
            return False


def check_command_params(cls, input_dict):
    pass


def check_model_keyword_args(input_dict, cls):
    """
    Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError
    If model is not specified, raises ModelNotSpecifiedError.
    Initialization of a model (e.g., Accel, SOL, etc. requires all keywords specified)
    """
    #models = cls.models
    try:
        if not check_model_specified(input_dict):
            actual_dict = {'Unknown': 0}
            raise InputArgumentsError('Model most be specified', input_dict, actual_dict)
        model = input_dict['model']
        actual_dict = cls.models[str(model)]['parms']
        if sorted(input_dict.keys()) != sorted(actual_dict.keys()):
            raise InputArgumentsError('Model parameter specification error', input_dict, actual_dict)
    except InputArgumentsError as e:
        print e
        return -1
    return 0


def check_keyword_in_model(keyword, cls):
    """
    Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError
    If model is not specified, raises ModelNotSpecifiedError.
    Initialization of a model (e.g., Accel, SOL, etc. requires all keywords specified)
    """
    if keyword in cls.get_model_dict(cls.model):
        return True
    else:
        return False


def check_partial_keywords_for_current_model(input_dict, cls):
    """
    Checks whether the keywords specified for a current model correspond to that model.
    """
    actual_dict = (cls, cls.model)
    for key in input_dict:
        if not key in cls.actual:
            raise InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
    return True


def check_partial_keywords_for_new_model(input_dict, cls):
    """
    Checks whether the keywords specified for a new model correspond to that model.
    """
    model = input_dict['model']
    actual_dict = get_model_dict(cls, model)
    for key in input_dict:
        if not key in cls.actual:
            raise InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
    return True


def check_model_specified(input_dict):
    if 'model' in input_dict.keys():
        return True
    else:
        return False


def get_model_dict(cls, model):
    models = cls.models
    return models[str(model)][1]


class Error(Exception):
    """Base class for ICOOL input exceptions."""
    pass


class InputError(Error):
    """General exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        string = self.msg + ' ' + self.expr
        return repr(string)


class InvalidType(InputError):
    """Exception raised for attempt to assign incorrect type to a variable.  Required types for """
    """various variables are indicated in the associated dictionary 'type' field for the """
    """associated namelist."""

    def __init__(self, expected_type, actual_type):
        InputError.__init__(self, 'Incorrect type.', 'Incorrect type.')
        self.expected_type = expected_type
        self.actual_type = actual_type

    def __str__(self):
        msg = "Invalid type.  Expected " + self.expected_type + " but instead got " + self.actual_type
        return repr(msg)


class UnknownVariable(InputError):

    """Exception raised for unknown variable in a given namelist."""

    def __init__(self, variable, namelist):
        InputError.__init__(self, 'Unknown variable', 'Unknown variable.')
        self.variable = variable
        self.namelist = namelist

    def __str__(self):
        msg = 'Unknown variable: ' + self.variable + ' in namelist: ' + self.namelist
        return repr(msg)


class NamelistObjectTypeError(InputError):
    """Exception raised for incorrect type of namelist object.
       This error is raised if the type of a namelist assigned to a namelist variable does not match
       the expected type.
    """

    def __init__(self, expr, namelist, type):
        InputError.__init__(self, expr, 'Namelist object type error.')
        self.namelist = namelist
        self.type = type

    def __str__(self):
        msg = 'Incorrect Namelist type object. Expected: ' + self.type + ' but received: ' + \
            self.namelist.__class__.__name__
        return repr(msg)


class IncorrectObjectCommand(InputError):
    """Exception raised for attempt to add incorrect command to an object.
       For example, Section, Cell and Background only allow certain commands."""

    def __init__(self, expr, object, command):
        self.object = object
        self.command = command

    def __str__(self):
        msg = 'Command: ' + self.command + ' is not supported in object: ' + self.object
        return repr(msg)


class InputArgumentsError(InputError):
    """Exception raised for unsupported input arguments variable."""

    def __init__(self, expr, input_dict, actual_dict):
        InputError.__init__(self, expr, 'Input arguments error.')
        self.input_dict = input_dict
        self.actual_dict = actual_dict

    def __str__(self):
        received = ""
        for key in sorted(self.input_dict.keys()):
            received += str(key)
            received += ' '
        expected = ""
        for key in sorted(self.actual_dict.keys()):
            expected += str(key)
            expected += ' '

        msg = 'Input arguments error.\nReceived: \n' + received + '\nExpected: \n' + expected
        return msg


class SetAttributeError(InputError):
    """Exception raised for attempt to set improper or private attribute for an object."""
    def __init__(self, expr, cls, attribute):
        InputError.__init__(self, expr, 'Input arguments error.')
        self.cls = cls
        self.attribute = attribute

    def __str__(self):
        msg = 'Illegal attempt to set attribute ' + self.attribute + ' on object ' + str(type(self.cls))
        return msg

class InvalidCommandParameters(InputError):
    def __init__(self, specified_parameters, allowed_parameters):
        self.specified_parameters = specified_parameters
        self.allowed_parameters = allowed_parameters

    def __str__(self):
        specified = ' '.join(self.specified_parameters)
        allowed = ' '.join(self.allowed_parameters)
        msg = '\nInvalid command parameter(s).\nYou specified: ' + specified + '\nAllowed command parameters are:\n' + allowed
        return msg

class InvalidCommandParameter(InputError):
    def __init__(self, command_parameter, allowed_parameters):
        self.command_parameter = command_parameter
        self.allowed_parameters = allowed_parameters

    def __str__(self):
        msg = '\nInvalid command parameter: ' + str(self.command_parameter) + '\nAllowed command parameters are:\n' + ' '.join(self.allowed_parameters)
        return msg


class ModelNotSpecified(InputError):
    def __init__(self, models):
        self.allowed_models = models

    def __str__(self):
        msg = '\nModel not specified. ' + '\nAllowed models are:\n' + ' '.join(self.allowed_models)
        return msg


class InvalidModel(InputError):
    def __init__(self, model, allowed_models):
        self.model = model
        self.allowed_models = allowed_models

    def __str__(self):
        msg = '\nInvalid model: ' + str(self.model) + '\nAllowed models are:\n' + ' '.join(self.allowed_models)
        return msg



class MissingCommandParameter(InputError):
    def __init__(self, command_parameter, allowed_parameters):
        self.command_parameter = command_parameter
        self.allowed_parameters = allowed_parameters

    def __str__(self):
        msg = '\nMissing command parameter: ' + str(self.command_parameter)
        return msg


class ContainerCommandError(InputError):
    def __init__(self, command, allowed_commands):
        self.allowed_commands = allowed_commands
        self.command = command

    def __str__(self):
        msg = '\nIllegal container command: ' + str(self.command)
        return msg


class FieldError(InputError):
    pass

