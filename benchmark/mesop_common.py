import mesop as me

SIDEBAR_WIDTH = 150


def sidebar():
    with me.box(style=me.Style(width=SIDEBAR_WIDTH,
                               padding=me.Padding(top=20, left=20))):
        sidebar_link('Single', '/')
        sidebar_link('Compare', '/compare')


def sidebar_link(text, url):
    with me.box(style=me.Style(height=30)):
        me.link(text=text, url=url)
