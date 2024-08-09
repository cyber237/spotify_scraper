# Spotify Scraper

This is a repository for a Spotify scraper project. 
The project aims to extract, transform and load data from the Spotify website.

## Installation

To install the Spotify scraper, follow these steps:

1. Clone the repository: `git clone https://github.com/cyber237/spotify_scraper.git`
2. Install the required dependencies: `poetry install -no-root`
3. Install browser for playright: `playwright install chromium`
4. Create env file `api/.env` using `api/example.env` as template.

## Usage

To use the Spotify scraper, follow these steps:

1. `cd api`
2. Run migrations: `python manage.py migrate`
3. Run server: `python manage.py runserver` 

## Contributing

Contributions are welcome! If you would like to contribute to the Spotify scraper project, please follow these guidelines:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m "Add your changes"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
