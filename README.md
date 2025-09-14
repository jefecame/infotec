# 🚀 Infotec - Laravel Docker Development Environment

This Docker Compose setup automatically creates a fresh Laravel installation in an empty `src/` folder and sets up a complete development environment with MariaDB.

## ✨ Features

- 🏗️ **Automatic Laravel Creation**: Creates a fresh Laravel project if `src/` is empty
- 🐳 **Docker-based Development**: Complete containerized environment
- 🗄️ **Database Integration**: Pre-configured MariaDB with automatic migrations
- 🔑 **Environment Management**: Secure credential handling
- 🛠️ **Development Tools**: Integrated Composer, Artisan, and more

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker Desktop installed and running
- Git (optional, for version control)

### 🔄 One-Command Setup

```bash
# 1. Copy and configure environment
cp .env.example .env
# Edit .env with your preferred database credentials

# 2. Initialize everything (creates Laravel + starts services)
make init

# That's it! Open http://localhost:8000
```

### 📝 Manual Step-by-Step

1. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

2. **Create Laravel Project** (if src/ is empty)
   ```bash
   docker compose --profile init up laravel-init
   ```

3. **Start All Services**
   ```bash
   docker compose up -d
   ```

4. **Access Your Application**
   - Laravel App: http://localhost:8000
   - Database: localhost:3306

## 🗂️ Project Structure

```
infotec/
├── src/                    # Laravel application (auto-created)
├── scripts/               # Initialization scripts
│   ├── init-laravel.sh    # Laravel project creator
│   └── start-application.sh # App startup logic
├── docker-compose.yml     # Service definitions
├── .env                   # Environment variables (create from .env.example)
├── .env.example           # Environment template
├── Makefile               # Development shortcuts
└── README.md              # This file
```

## 🗂️ Docker Services

| Service | Description | Port |
|---------|-------------|------|
| **application** | Laravel app with PHP-FPM | 8000 |
| **mariadb** | Database server | 3306 |
| **laravel-init** | Laravel project initializer | - |
| **composer** | Dependency manager | - |

## 🛠️ Development Commands

### Using Make (Recommended)
```bash
make help           # Show all available commands
make init           # Initialize Laravel + start services
make up             # Start services
make down           # Stop services  
make restart        # Restart services
make logs           # View application logs
make shell          # Access Laravel container
make composer       # Run composer install
make artisan CMD    # Run artisan command
make clean          # Remove all containers and data
make status         # Show container status
```

### Using Docker Compose Directly
```bash
# View logs
docker compose logs application

# Access container shell
docker compose exec application bash

# Run artisan commands
docker compose exec application php artisan migrate
docker compose exec application php artisan make:controller HomeController

# Run composer
docker compose --profile tools run --rm composer
```

## 🗂️ Automatic Features

The setup automatically handles:

- ✅ **Laravel Installation**: Creates Laravel 11.x if src/ is empty
- ✅ **Database Configuration**: Configures Laravel to use MariaDB
- ✅ **Environment Setup**: Generates APP_KEY and configures .env
- ✅ **Database Migration**: Runs initial migrations
- ✅ **Dependency Installation**: Installs Composer packages
- ✅ **Permission Management**: Sets correct file permissions
- ✅ **Health Checks**: Ensures database connectivity

## 🐛 Troubleshooting

### Laravel project not created?
```bash
# Run initialization manually
docker compose --profile init up laravel-init
```

### Application not starting?
```bash
# Check logs
docker compose logs application

# Restart services
make restart
```

### Database connection issues?
```bash
# Check MariaDB logs
docker compose logs mariadb

# Verify environment variables
cat .env
```

### Clean slate reset?
```bash
# Remove everything and start fresh
make clean
rm -rf src/*  # Remove Laravel files
make init     # Reinitialize
```

## 🔒 Security Notes

- ⚠️ **Never commit `.env`** - Contains sensitive credentials
- 🔑 **Change default passwords** in `.env` before production use
- 🏠 **Development only** - This setup is for development, not production

## 🔗 Useful Links

- [Laravel Documentation](https://laravel.com/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [MariaDB Documentation](https://mariadb.org/documentation/)

---

**Happy coding!** 🚀 If you encounter any issues, check the logs or create an issue in the repository.
