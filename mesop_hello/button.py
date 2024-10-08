import mesop as me


@me.page(path="/")
def app():
    with me.box():
        me.button('Click me')