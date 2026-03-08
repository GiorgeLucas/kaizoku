# Kaizoku CLI

[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A command-line interface for searching and streaming anime from multiple providers.

## Features

- Search for anime across multiple providers
- Browse episodes with ease
- Stream episodes directly in MPV
- Support for multiple video qualities
- Download episodes (partial implementation)
- Extensible architecture for adding new providers

## Getting Started

### Prerequisites

- Python 3.8 or higher
- MPV media player (for streaming)
- Internet connection

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GiorgeLucas/kaizoku-cli.git
   cd kaizoku-cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the application:

```bash
python main.py
```

The program will guide you through:

1. Entering an anime name to search.
2. Selecting an anime from the results (showing provider and language).
3. Selecting an episode from the list.
4. Choosing to either Watch (opens in MPV) or Download (saves to your configured download directory;
   note that download functionality is not fully implemented yet).

### Configuration

You can configure the download directory by creating a config file at ``~/.config/kaizoku-cli/config.json``
(or the path specified by ``XDG_CONFIG_HOME``). Example:

```json
{
    "download_path": "/path/to/downloads"
}
```

If not configured, downloads will default to ``~/Videos/kaizoku-cli``.

### Supported providers

- Animefire (Portuguese)
- Animes Digital (Portuguese)

More providers can be added by implementing the ``BaseProvider`` class.

## Getting Help

If you need help or have questions:

- **Bug Reports and Feature Requests**: Please open an issue on [GitHub Issues](https://github.com/GiorgeLucas/kaizoku-cli/issues).
- **Documentation**: This README provides basic usage. For more detailed documentation, see the ``docs/`` folder (if available).
- **Discussions**: You can also start a discussion in the GitHub repository's Discussions tab (if enabled).

## Contributing

We welcome contributions from the community! To contribute:

1. Fork the repository and create a new branch for your changes.
2. Make your changes following the existing code style and conventions.
3. Test your changes to ensure they work as expected.
4. Submit a Pull Request with a clear description of your changes.

Please also read [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines, code of conduct, and the contribution process.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for the full license text.

## Acknowledgments

- Thanks to the anime providers (Animefire, Animes Digital) for making content available.
- Built with Python, [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/), and [Questionary](https://github.com/tmbo/questionary).
- Inspired by other CLI tools and the open-source community.
