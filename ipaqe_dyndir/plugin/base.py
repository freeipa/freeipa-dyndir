# coding: utf-8
# Author: Milan Kubik

class PluginConfigError(ValueError):
    pass


class PluginBase:  # pylint: disable=R0903
    """Dynamic Directory plugin base class

    All plugins must inherit from this class and
    implement the __call__ method.

    This method is later used by the plugin manager
    instance to call the plugin.
    """

    def __call__(self, host):
        """Call magic method

        The host argument is the host dictionary.
        The dictionary is passed directly with all
        its keys. This allows plugins to work with
        the host based on its role.
        """
        raise RuntimeError('You need to subclass this method.')
