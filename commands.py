from AppOpener import open, close

# * Open an app
def open_app(name: str) -> str:

    try:
        print("Attempting to open app")
        open(name, match_closest=True, throw_error=True, output=False)
    except Exception as e:
        print(e)
    else:
        output = format("Opening {name}")
        return output

# * Close an app
def close_app(name: str) -> str:

    try:
        close(name, match_closest=True, throw_error=True, output=False)
    except Exception as e:
        print(e)
    else:
        output = format("Closing {name}")
        return output
    
