import logging
logger = logging.getLogger(__file__)

logging.basicConfig(level=logging.INFO)


class ChangeTrigger(object):
    def __getattr__(self, name):
        obj = getattr(self.instance, name)

        # KEY idea for catching contained class attributes changes:
        # recursively create ChangeTrigger derived class and wrap
        # object in it if getting attribute is class instance/object

        if hasattr(obj, '__dict__'):
            return self.__class__(obj)
        else:
            return obj 

    def __setattr__(self, name, value):
        if name in self.suscribers:
            if getattr(self.instance, name) != value:
                self._on_change(name, value)
            setattr(self.instance, name, value)

    def __init__(self, obj, suscribers):
        object.__setattr__(self, 'suscribers', suscribers)
        object.__setattr__(self, 'instance', obj)


    def _on_change(self, name, value):
        raise NotImplementedError('Subclasses must implement this method')