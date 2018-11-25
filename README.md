# OpaCache
Redis/Docker based caching layer for Open Policy Agent

# Configuration
Edit config.ini file to connect the cache and your OPA node and to choose a port for the cache. Here you can also setup entries' TTL and switch debug mode.

# Run
You need docker to run the cache. You should export the cache's port when running the container. The easiest way to run it is via 'docker-compose up' and setting your desired properties in the docker-compose.yml file.

# Use
Once the cache is up, (OPA should be running too in server mode) you should replace your OPA's host:port with the cache's host:port when making REST requests. The cache stores entries which:
  - Keys are hash(url + payload) from the incoming request.
  - Values are the response from OPA.

# Warning
This cache is meant to be used for policy evaluation purposes only. While it may work sometimes, you should avoid using it for OPA administration purposes.

New features coming soon!

