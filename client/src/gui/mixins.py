from abc import ABC, abstractmethod

from dearpygui.dearpygui import set_item_height, set_item_pos, set_item_width


class ResizeMixin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    def resize(self, width: int, height: int, position: tuple[int, int]) -> None:
        set_item_width(item=self.name, width=width)
        set_item_height(item=self.name, height=height)
        set_item_pos(item=self.name, pos=position)
