import webbrowser

def openInChrome(url):
    path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(path))
    webbrowser.get('chrome').open_new_tab(url)
    
url = 'https://chatgpt.com'

openInChrome(url)

# im gonna compile this .py into an .exe then link it to a path variable and the damn command will open chatgpt.com in chrome ! automation at it's peak !