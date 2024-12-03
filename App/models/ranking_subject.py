from App.models.observer import Subject

class RankingSubject(Subject):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event, data=None):
        for observer in self._observers:
            observer.update(event, data)