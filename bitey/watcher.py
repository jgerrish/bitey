import logging


class Watcher:
    """
    A basic Watcher
    Users can register a Listener to this Watcher to get updates when the
    object the Watcher watches is updated.
    """

    def __init__(self):
        "Initialize the watcher with an empty set of listeners"
        # When Watcher is subclassed, this needs to be called explicitly
        self.listeners = []  # set()
        self.logger = logging.getLogger("bitey.watcher.Watcher")

    def register(self, listener):
        """
        Register to get messages when this component is updated.
        listener is a Listener
        """
        if ("listeners" in self.__dict__) and self.listeners:
            self.listeners.append(listener)
        else:
            # TODO: Figure out why there's lookup issues with base class / subclass
            self.listeners = []  # set()
            self.listeners.append(listener)

    def update(self):
        """
        Update any registered listeners that the watched object was changed.
        obj is the object
        """
        # When called by the subclass, the subclass attributes aren't properly searched
        if ("listeners" in self.__dict__) and self.listeners:
            for listener in self.listeners:
                listener.update(self)
