from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from percy import percy_snapshot

# start the example app in another thread
httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
thread = Thread(target=httpd.serve_forever)
thread.setDaemon(True)
thread.start()

# launch firefox headless
ff_options = FirefoxOptions()
ff_options.add_argument('-headless')
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = Firefox(options=ff_options)

# go to the example app
browser.get('http://localhost:8000')
browser.implicitly_wait(10)

# snapshot empty state
percy_snapshot(browser, 'Empty Todo State')

# snapshot with a new todo
new_todo_input = browser.find_element(By.CLASS_NAME, 'new-todo')
new_todo_input.send_keys('Try Percy')
new_todo_input.send_keys(Keys.ENTER)
percy_snapshot(browser, 'With a Todo')

# snapshot with a completed todo
todo_toggle = browser.find_element(By.CLASS_NAME, 'toggle')
todo_toggle.click()
percy_snapshot(browser, 'Completed Todo')

# clean up
browser.quit()
httpd.shutdown()
