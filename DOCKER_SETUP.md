# Docker Setup Required

## Install Docker Desktop

This project requires Docker to run PostgreSQL. 

### macOS Installation

1. Download Docker Desktop for Mac:
   - **Apple Silicon (M1/M2/M3)**: https://desktop.docker.com/mac/main/arm64/Docker.dmg
   - **Intel**: https://desktop.docker.com/mac/main/amd64/Docker.dmg

2. Install Docker Desktop:
   ```bash
   open ~/Downloads/Docker.dmg
   ```
   Drag Docker to Applications folder

3. Open Docker Desktop from Applications
   - Grant permissions when requested
   - Wait for Docker Engine to start (icon in menu bar will show "Docker Desktop is running")

4. Verify installation:
   ```bash
   docker --version
   docker compose version
   ```

## Starting the Application

Once Docker is installed:

```bash
# Start PostgreSQL
docker compose up -d

# Verify PostgreSQL is running
docker compose ps

# Start the application
./dev.sh
```

## Stopping the Services

```bash
# Stop application (Ctrl+C in terminal running ./dev.sh)

# Stop PostgreSQL
docker compose down

# Stop PostgreSQL and remove data (clean slate)
docker compose down -v
```

## Troubleshooting

### Docker not found
- Ensure Docker Desktop is installed and running
- Check the Docker icon in your menu bar
- Restart Docker Desktop if needed

### PostgreSQL connection error
- Wait 5-10 seconds after `docker compose up -d` for PostgreSQL to initialize
- Check logs: `docker compose logs postgres`
- Verify container is running: `docker compose ps`

### Port 5432 already in use
- Another PostgreSQL instance might be running
- Stop it: `brew services stop postgresql` (if installed via Homebrew)
- Or change the port in `docker-compose.yml`
