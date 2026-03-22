# MCP Server Configuration

This document explains how to configure MCP (Model Context Protocol) servers for development within this INFOTEC Laravel project.

## Database MCP Server (SQLite)

The project uses MariaDB in Docker, but you can also configure an SQLite MCP server for local development and testing.

### Setup Instructions

1. **Install MCP Server for SQLite**
   - Visit: https://github.com/modelcontextprotocol/servers/tree/main/src/sqlite
   - Follow installation instructions for your platform

2. **Configure in Cursor/Claude Desktop**

   Add to your MCP configuration file:

   ```json
   {
     "mcpServers": {
       "sqlite": {
         "command": "python",
         "args": ["-m", "mcp_server_sqlite"],
         "env": {
           "MCP_SQLITE_DATABASE": "/path/to/database.sqlite"
         }
       }
     }
   }
   ```

3. **Connecting to Docker MariaDB** (Advanced)

   If you want direct database access instead, use the Database MCP server:

   ```json
   {
     "mcpServers": {
       "mariadb": {
         "command": "npx",
         "args": ["@modelcontextprotocol/server-database"],
         "env": {
           "DATABASE_URL": "mysql://mariadb_user:password@localhost:3306/infotec_db"
         }
       }
     }
   }
   ```

   Note: Requires MariaDB port `3306` exposed and credentials from `.env`.

## Use Cases

- **Query database schema**: "Show me the tables in the eventos database"
- **Test migrations**: "What columns exist in the asistentes table?"
- **Verify data**: "Check if the evento with ID 1 exists"
- **Database debugging**: "List all columns and their types in the ponentes table"

## Manual Database Access

If MCP isn't configured, you can always access the database manually:

```bash
# From host (via Docker)
docker compose exec mariadb mysql -u root -p${MARIADB_ROOT_PASSWORD} ${MARIADB_DATABASE}

# From Laravel container (Tinker)
docker compose exec laravel php artisan tinker
> \DB  # Shows database connection options
> DB::table('eventos')->get();
```

See `.github/copilot-instructions.md` for more database commands.
