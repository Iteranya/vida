Okay, I honestly have no idea what I'm doing...

What I want:

- An Endpoint To Interact With Waifu
- Waifu Manages Her Own Memory
- No Sending Entire Chat History (that shit's ignored by default)
- Automatic Memory Management with all sorts of features
- But for now, just context

For MVP:

- Automatic Context Management
- Basically just the short term context for now
- Nothing else??? Maybe???
- Waifu Swapping and Routing Shenanigans
- Unit Test (lol, lmao)

TODO:
- Make the required component (everything in controller folder)
- Recommended Order
    - llm.py
    - prompt.py <- | combine
    - history.py  <- | this two
    - pipeline.py (final assembly)
    - interface (final abstraction before router)
- Figure out the CRUD with the data and directory
- Get an AI to make the User Interface (or convince user that manually editing Json is cool?)
- Make the routers
- Test the routers (lol, lmao)
- Testing and such, maybe pause development for intergrated test with the front end.
- Since this is made for a very flexible front end, we can pull off a... Agnai? Yeah, Agnai sounds good for testing the front end.