from abc import ABC, abstractmethod

from dearpygui.dearpygui import child_window


class View(ABC):
    def create_view(self) -> None:
        with child_window(label=self.name, tag=self.name):
            self.create()

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def create(self) -> None:
        raise NotImplementedError
