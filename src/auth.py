from os import getenv

from fastmcp.server.auth.providers.jwt import JWTVerifier

# Define development tokens and their associated claims
# verifier = StaticTokenVerifier(
#     tokens={
#         "dev-alice-token": {
#             "client_id": "alice@company.com",
#             "scopes": ["read:data", "write:data", "admin:users"]
#         },
#         "dev-guest-token-null": {
#             "client_id": "guest-user",
#             "scopes": ["read:data"]
#         }
#     },
#     required_scopes=["read:data"]
# )

verifier = JWTVerifier(
    public_key=None,
    jwks_uri=f"{getenv('AUTH_BASE_URL', 'http://localhost:3000')}/.well-known/jwks.json",
    issuer=getenv("AUTH_JWT_ISSUER", 'hospiai-api'),
    audience=getenv("AUTH_JWT_AUDIENCE", 'hospiai-mcp'),
    algorithm="RS256",
    required_scopes=["read:data"]
)
