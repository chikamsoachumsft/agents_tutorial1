# Tailspin Toys Crowd Funding Development Guidelines

This is a crowdfunding platform for games with a developer theme. The application uses a Flask backend API with SQLAlchemy ORM for database interactions, and an Astro/Svelte frontend with Tailwind CSS[...]

## Code standards

### Required Before Each Commit

- Run Python tests to ensure backend functionality
- For frontend changes, run builds in the client directory to verify build success and the end-to-end tests, to ensure everything works correctly
- When making API changes, update and run the corresponding tests to ensure everything works correctly
- When updating models, ensure database migrations are included if needed
- When adding new functionality, make sure you update the README
- Make sure all guidance in the Copilot Instructions file is updated with any relevant changes, including to project structure and scripts, and programming guidance

### Code Review Instructions

- All new pull requests must be reviewed by at least one other contributor before merging.
- Reviewers should check for adherence to code formatting requirements and project patterns described in this file.
- Confirm that all tests pass and the relevant scripts have been used (see "Required Before Each Commit" and "Scripts" sections).
- Ensure new functionality includes documentation updates, if applicable.
- Review API changes for RESTful design and use of Flask blueprints.
- Validate frontend changes for proper use of Svelte/Astro patterns and Tailwind CSS styling guidelines.
- Check for security best practices, especially in workflows and dependencies.
- Add comments to code and workflows where necessary for clarity.
- Provide constructive feedback to improve code quality and maintainability.
- Code review comments should be in spanish

### Code formatting requirements

- When writing Python, you must use type hints for return values and function parameters.

### Python and Flask Patterns

- Use SQLAlchemy models for database interactions
- Use Flask blueprints for organizing routes
- Follow RESTful API design principles
- Use the standardized response format from `utils.response_formatter` for all API endpoints
- Implement proper error handling with appropriate HTTP status codes

### Authentication and Security

- Use JWT tokens for authentication (utilities in `utils.jwt_utils`)
- Apply `@require_auth` decorator for protected routes
- Hash passwords with bcrypt (minimum 12 salt rounds)
- Validate and sanitize all user input
- Never expose sensitive data (passwords, tokens) in logs or responses
- Use environment variables for sensitive configuration (see `.env.example`)

### Svelte and Astro Patterns

- Use Svelte for interactive components
- Follow Svelte's reactive programming model
- Create reusable components when functionality is used in multiple places
- Use Astro for page routing and static content

### Styling

- Use Tailwind CSS classes for styling
- Maintain dark mode theme throughout the application
- Use rounded corners for UI elements
- Follow modern UI/UX principles with clean, accessible interfaces

### GitHub Actions workflows

- Follow good security practices
- Make sure to explicitly set the workflow permissions
- Add comments to document what tasks are being performed

## Scripts

- Several scripts exist in the `scripts` folder
- Use existing scripts to perform tasks rather than performing them manually
- Existing scripts:
    - `scripts/setup-env.sh`: Performs installation of all Python and Node dependencies
    - `scripts/run-server-tests.sh`: Calls setup-env, then runs all Python tests
    - `scripts/start-app.sh`: Calls setup-env, then starts both backend and frontend servers

## Repository Structure

- `server/`: Flask backend code
  - `models/`: SQLAlchemy ORM models
    - `user.py`: User authentication model
  - `routes/`: API endpoints organized by resource
    - `auth.py`: Authentication endpoints (register, login, logout, refresh)
    - `users.py`: User management endpoints (profile CRUD)
    - `health.py`: Health check endpoint
    - `games.py`: Game catalog endpoints
  - `tests/`: Unit tests for the API
    - `test_auth.py`: Authentication tests (20 tests)
    - `test_health.py`: Health endpoint tests
    - `test_games.py`: Game endpoint tests
  - `utils/`: Utility functions and helpers
    - `jwt_utils.py`: JWT token generation and verification
    - `auth_middleware.py`: Authentication decorator
    - `response_formatter.py`: Standardized API response formatting
    - `validation.py`: Input validation and sanitization
    - `database.py`: Database initialization utilities
- `client/`: Astro/Svelte frontend code
  - `src/components/`: Reusable Svelte components
  - `src/layouts/`: Astro layout templates
  - `src/pages/`: Astro page routes
  - `src/styles/`: CSS and Tailwind configuration
- `scripts/`: Development and deployment scripts
- `data/`: Database files (SQLite by default)
- `docs/`: Project documentation
  - `API.md`: Complete API documentation
- `README.md`: Project documentation
- `.env.example`: Environment variable template

## API Standards

All API endpoints should:
1. Use the `/api/v1/` prefix for versioning
2. Return responses using `success_response()` or `error_response()` from `utils.response_formatter`
3. Include proper HTTP status codes (200, 201, 400, 401, 404, 409, 500)
4. Validate input data appropriately
5. Handle errors gracefully with meaningful messages

See `docs/API.md` for complete API documentation.

