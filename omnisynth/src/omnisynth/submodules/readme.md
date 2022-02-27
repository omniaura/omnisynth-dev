# Server
* The server will handle requests and return responses in the standard JSON format. The server has the following properties:
	* IP: localhost (127.0.0.1)
	* PORT: 42042
* The server will server forever and is killed with the user's application with a request.
* The server will also start the OmniSynth instance and maintain it's state for the user.

# Server Request Handler
* The request handler will be responsible for parsing requests and performing the requested actions / collect requested data from the OmniSynth instance.