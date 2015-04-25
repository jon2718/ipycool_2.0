from modeledcommandparameter import ModeledCommandParameter

class Field(ModeledCommandParameter):

    """
    A Field is a:
    FTAG - A tag identifying the field.  Valid FTAGS are:
    NONE, ACCEL, BLOCK, BROD, BSOL, COIL, DIP, EFLD, FOFO, HDIP, HELI(
        X), HORN, KICK, QUAD,
    ROD, SEX, SHEE(T), SOL, SQUA, STUS, WIG

    FPARM - 15 parameters describing the field.  The first parameter is the model.
    """

    def __init__(self, **kwargs):
        pass

    def __call__(self, **kwargs):
        pass

    def __setattr__(self, name, value):
        pass

    def __str__(self):
    	pass
        #return self.begtag + ':' + 'Field:' + \
        #    ModeledCommandParameter.__str__(self)

    def gen_fparm(self):
        self.fparm = [0] * 10
        cur_model = self.get_model_dict(self.model)
        for key in cur_model:
            pos = int(cur_model[key]['pos']) - 1
            if key == self.get_model_descriptor_name():
                val = self.get_icool_model_name()
            else:
                val = getattr(self, key)
            self.fparm[pos] = val
        print self.fparm
