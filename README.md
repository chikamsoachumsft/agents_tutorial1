# Tailspin Toys

This repository contains the project for a 1 hour guided workshop to explore GitHub Copilot Agent Mode and related features in Visual Studio Code. The project is a website for a fictional game crowd-funding company, with a [Flask](https://flask.palletsprojects.com/en/stable/) backend using [SQLAlchemy](https://www.sqlalchemy.org/) and [Astro](https://astro.build/) frontend using [Svelte](https://svelte.dev/) for dynamic pages.

To begin the workshop, start at [docs/README.md](./docs/README.md)

Or, if just want to run the app...

## Launch the site

A script file has been created to launch the site. You can run it by:

```bash
./scripts/start-app.sh
```

Then navigate to the [website](http://localhost:4321) to see the site!

## API Documentation

The backend API includes authentication, user management, and game catalog features. For complete API documentation, see [docs/API.md](./docs/API.md).

### Key Features

- **Authentication**: JWT-based authentication with register, login, and token refresh
- **User Management**: Profile management and account operations
- **Security**: Rate limiting, CORS, security headers, password hashing with bcrypt
- **Standardized Responses**: All endpoints return consistent JSON response format
- **Health Check**: Endpoint to verify API status

## Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Update the `.env` file with your configuration (especially `JWT_SECRET` for production)

## Testing

Run all backend tests:

```bash
./scripts/run-server-tests.sh
```

## License 

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) for the full terms.

## Maintainers 

You can find the list of maintainers in [CODEOWNERS](./.github/CODEOWNERS).

## Support

This project is provided as-is, and may be updated over time. If you have questions, please open an issue.
