class Subject:
    def __init__(self):
        self._observers = []  # List of observer objects

    def attach(self, observer):
        """Add an observer to the list."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """Remove an observer from the list."""
        self._observers.remove(observer)

    def notify(self, event, data=None):
        """Notify all observers about an event."""
        for observer in self._observers:
            observer.update(event, data)


class Observer:
    def update(self, event, data=None):
        """Respond to a notification."""
        raise NotImplementedError("Subclasses must override update()!")