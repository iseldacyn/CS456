# Cryptographic Chat Protocol

Client-server chat protocol utilizing RSA and AES encryption. To run, first run

```python server.py```

Then, in another terminal run

```python client.py```

## Cryptographic Specifications

The full specifications for the schema are as follows:

- First, the client connects to the server
- The server sends its public RSA key to the client
- The client encrypts their private RSA key using the servers public key and send its back to the server
- The server generates a shared AES key, encrypts it using the clients public RSA key, and sends its to the client
- The client and server are now able to share information securely

## Known Bugs/Issues

- Disconnecting a client seems to break the server if not closed properly
- Text overflows if messages are sent while typing a response
