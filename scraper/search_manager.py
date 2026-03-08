from typing import Any, Union

from core.anime import Anime, Episode
from providers.animefire import Animefire
from providers.animesdigital import AnimesDigital
from providers.base_provider import BaseProvider

class SearchManager:
    providers: list[BaseProvider] = [Animefire(), AnimesDigital()]

    @staticmethod
    def search_anime(raw_anime_name: str) -> list[Anime]:
        animes_list: list[Anime] = []
        for provider in SearchManager.providers:
            provider_anime_results = provider.search_anime(raw_anime_name)
            for provider_anime in provider_anime_results:
                animes_list.append(provider_anime)
        return animes_list

    @staticmethod
    def get_episodes_list(anime: Anime) -> list[Episode]:
        episodes_list = anime.provider.get_episodes_list(anime)
        return episodes_list

    @staticmethod
    def get_episode_url(episode: Episode) -> Union[dict[str, Any], None]:
        episode_url = episode.anime.provider.get_episode_video_url(episode)
        return episode_url




    



        
        
