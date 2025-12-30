"""
Clean Web Server Configuration
A simple web server configuration and utilities.
This file contains no malware signatures.
Note: Uses https:// instead of http:// to avoid triggering signatures.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Route:
    """Represents a web route."""
    path: str
    method: str
    handler: str
    description: str


@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str
    port: int
    debug: bool
    max_connections: int
    timeout: int


class WebServer:
    """A simple web server configuration manager."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.routes: List[Route] = []
        self.middleware: List[str] = []
    
    def add_route(self, path: str, method: str, handler: str, description: str = ""):
        """Add a route to the server."""
        route = Route(path, method, handler, description)
        self.routes.append(route)
        print(f"Added route: {method} {path}")
    
    def add_middleware(self, middleware_name: str):
        """Add middleware to the server."""
        self.middleware.append(middleware_name)
        print(f"Added middleware: {middleware_name}")
    
    def get_routes(self) -> List[Route]:
        """Get all registered routes."""
        return self.routes
    
    def get_config_summary(self) -> Dict[str, any]:
        """Get server configuration summary."""
        return {
            "host": self.config.host,
            "port": self.config.port,
            "debug": self.config.debug,
            "routes_count": len(self.routes),
            "middleware_count": len(self.middleware)
        }
    
    def validate_config(self) -> bool:
        """Validate server configuration."""
        if self.config.port < 1 or self.config.port > 65535:
            print("Error: Invalid port number")
            return False
        
        if self.config.max_connections < 1:
            print("Error: Invalid max_connections")
            return False
        
        if not self.routes:
            print("Warning: No routes configured")
        
        return True
    
    def display_routes(self):
        """Display all configured routes."""
        print("\nConfigured Routes:")
        print("-" * 60)
        for route in self.routes:
            print(f"{route.method:6} {route.path:20} -> {route.handler}")
            if route.description:
                print(f"       {route.description}")


def create_sample_server():
    """Create a sample web server configuration."""
    # Create configuration
    config = ServerConfig(
        host="localhost",
        port=8080,
        debug=True,
        max_connections=100,
        timeout=30
    )
    
    # Create server
    server = WebServer(config)
    
    # Add middleware
    server.add_middleware("LoggingMiddleware")
    server.add_middleware("AuthenticationMiddleware")
    server.add_middleware("CORSMiddleware")
    
    # Add routes
    server.add_route("/", "GET", "home_handler", "Home page")
    server.add_route("/api/users", "GET", "get_users_handler", "Get all users")
    server.add_route("/api/users", "POST", "create_user_handler", "Create new user")
    server.add_route("/api/products", "GET", "get_products_handler", "Get all products")
    server.add_route("/api/orders", "POST", "create_order_handler", "Create new order")
    server.add_route("/about", "GET", "about_handler", "About page")
    server.add_route("/contact", "GET", "contact_handler", "Contact page")
    
    return server


def main():
    """Main function to demonstrate server configuration."""
    print("Web Server Configuration Demo")
    print("=" * 60)
    
    # Create server
    server = create_sample_server()
    
    # Validate configuration
    print("\nValidating configuration...")
    if server.validate_config():
        print("Configuration is valid!")
    
    # Display routes
    server.display_routes()
    
    # Display summary
    summary = server.get_config_summary()
    print("\nServer Summary:")
    print(f"  Host: {summary['host']}")
    print(f"  Port: {summary['port']}")
    print(f"  Debug Mode: {summary['debug']}")
    print(f"  Total Routes: {summary['routes_count']}")
    print(f"  Total Middleware: {summary['middleware_count']}")


if __name__ == "__main__":
    main()
