# Strawberry Django Auth

This app is a pluggable authentication/authorization app for Django using Strawberry GraphQL.
Instead of the server managing the state of someone's session, an access token with a pre-determined lifetime will be issued upon successful authentication.
This allows for stateless authorization, meaning that there is less strain on the server and database since no queries will need to be made to verify that a token is valid.
