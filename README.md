# Strawberry Django Auth

Authentication/Authorization app for [Django](https://www.djangoproject.com/) powered by [Strawberry GraphQL](https://strawberry.rocks/) and [PyJWT](https://pypi.org/project/PyJWT/)

# About
This library allows you to export all authentication logic out of your project, and to import only what you want to use into your project. Using JWTs, the server is able to
handle user sessions without maintaining records of the session on the server. This also allows the server to verify a user without making queries to the database.

# Features
- [x] Works with Django's default user model or a custom one
- [x] Built in exception codes which are returned in the response
- [x] Easily customize JWT (claims, verification, algorithm)
- [x] Refresh tokens with customizable settings (expiry, rotation, families)