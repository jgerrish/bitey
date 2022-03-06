from dataclasses import dataclass
import logging


@dataclass
class Listener:
    """
    A basic Listener
    Users can add a listener to an object to get updates when that object is changed.
    """

    def __post_init__(self):
        self.logger = logging.getLogger("bitey.bitey.listener.Listener")

    def update(self, obj):
        """
        Update the listener with the object
        Called when the watched object changes
        """
        if "fun" in self.__dict__:
            self.fun(obj)

    def register_callback(self, fun):
        """
        Register a callback to get called on updates
        """
        self.fun = fun
