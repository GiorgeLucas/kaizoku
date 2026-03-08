from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

from typing_extensions import Any

from providers.common import Language

if TYPE_CHECKING:
    from core.anime import Anime, Episode

class BaseProvider(ABC):
    title: str
    color: str
    base_url: str
    language: Language
    
    @abstractmethod
    def search_anime(self, raw_anime_name: str) -> list[Anime]:
        pass


    @abstractmethod
    def get_episodes_list(self, anime: Anime) -> list[Episode]:
        pass

    @abstractmethod
    def get_episode_video_url(self, episode: Episode) -> Union[dict[str, Any], None]:
        pass
