from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any
import os


class AbstractUserGuideEntry(ABC):

    def __init__(self, title=None, description=None):
        self.title = title
        self.description = description
        self._children: list[AbstractUserGuideEntry] = []
        self._composite_function = self.default_callable

    def default_callable(self) -> None:
        print("No callable has been set for: {}" .format(self.__class__.__name__))
        return False

    @property
    def composite_function(self) -> Any:
        return self._composite_function()

    @composite_function.setter
    def composite_function(self, function: Callable):
        if self.function is not None and isinstance(function, Callable):
            self._composite_function = function
        else:
            print("The passed argument is not a callable! Setting default callable.")
            self._composite_function = self.default_callable

    @property
    def title(self) -> str:
        if self._title is not None:
            return self._title
        return ""

    @title.setter
    def title(self, title: str) -> None:
        if title is not None:
            title = title.strip()
            self._title = title
        else:
            self._title = "No title."

    @property
    def description(self) -> str:
        if self._description is None:
            self._description = "No description."
        return self._description

    @description.setter
    def description(self, description: str):
        if description is not None:
            self._description = description
        else:
            self._description = "No description."


class ConcreteUserGuideEntryChild(AbstractUserGuideEntry):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ConcreteUserGuideEntryComposite(AbstractUserGuideEntry):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def append_child(self, child: Union[dict, ConcreteUserGuideEntryChild]) -> None:
        if isinstance(child, dict):
            temp = ConcreteUserGuideEntryChild()
            for k, v in child.items():
                setattr(temp, k, v)
        if child not in self._children:
            self._children.append(child)

    def remove_child(self, child) -> None:
        if child in self._children:
            self._children.remove(child)

    def get_children(self) -> list[ConcreteUserGuideEntryComposite]:
        return self._children

    def get_child_at(self, index: int) -> Union[ConcreteUserGuideEntryComposite, ConcreteUserGuideEntryChild]:
        if index >= len(self._children):
            return None
        else:
            return self._children[int(index)]

    def has_children(self) -> bool:
        return len(self._children) > 0


class ContentsBuilder:
    def __init__(self):
        path_to_file = os.path.join(os.getcwd(), "models", "contents")
        if os.path.isfile(path_to_file):
            self._path_to_file = path_to_file
            self.root = ConcreteUserGuideEntryComposite(title="Contents")
        else:
            self._path_to_file = None
            raise FileNotFoundError("Cannot find a file at the provided path.")

    def build_from_txt(self):
        with open(self._path_to_file, "r") as f:
            last_root = -1
            for i, line in enumerate(f.readlines()):
                if " " == line[0] or "\t" in line:
                    self.root.get_child_at(last_root).append_child(ConcreteUserGuideEntryChild(title=line))
                else:
                    self.root.append_child(ConcreteUserGuideEntryComposite(title=line))
                    last_root += 1

    def get_root(self) -> ConcreteUserGuideEntryComposite:
        return self.root
if __name__ == "__main__":
    fp = "contents"
    builder = ContentsBuilder(fp)
    builder.build_from_txt()
