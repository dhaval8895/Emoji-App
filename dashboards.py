from math import pi
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import calendar
import datetime as DT
from datetime import datetime, date
import numpy as np
import pandas as pd
import holoviews as hv
from bokeh.plotting import show, figure, curdoc, output_file
from bokeh.models.tools import PanTool, SaveTool
from bokeh.io import output_file, show, curdoc
from bokeh.layouts import layout, widgetbox, column, row
from bokeh.models import ColumnDataSource, HoverTool, BoxZoomTool, ResetTool, PanTool, WheelZoomTool, SaveTool, LassoSelectTool
from bokeh.models import CustomJS, ColumnDataSource, Slider, DateRangeSlider, DatetimeTickFormatter
from bokeh.models.widgets import Slider, Select, TextInput, Div, DataTable, DateFormatter, TableColumn, Panel, Tabs, Toggle
from bokeh.io import output_file, show
from bokeh.models.widgets import RadioButtonGroup, Button
from bokeh.models.widgets.inputs import DatePicker

import emoji
import pandas as pd
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from bokeh.io import show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import TextInput

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Button

from bokeh.models.widgets import Paragraph

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import datetime
import threading

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/home/dsawlani/chromedriver',chrome_options=chrome_options)


def init_driver():
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome('/home/dsawlani/chromedriver',chrome_options=chrome_options)
     
    # set a default wait time for the browser [5 seconds here]:
	driver.wait = WebDriverWait(driver, 5)
 
    return driver


def close_driver(driver):
 
    driver.close()
 
    return

def login_twitter(driver, username, password):
 
    # open the web page in the browser:
    driver.get("https://twitter.com/login")
 
    # find the boxes for username and password
    username_field = driver.find_element_by_class_name("js-username-field")
    password_field = driver.find_element_by_class_name("js-password-field")
 
    # enter your username:
    username_field.send_keys(username)
    driver.implicitly_wait(1)
 
    # enter your password:
    password_field.send_keys(password)
    driver.implicitly_wait(1)
 
    # click the "Log In" button:
    driver.find_element_by_class_name("EdgeButtom--medium").click()
 
    return


class wait_for_more_than_n_elements_to_be_present(object):
    def __init__(self, locator, count):
        self.locator = locator
        self.count = count
 
    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            return len(elements) > self.count
        except StaleElementReferenceException:
            return False
        
        
def search_twitter(driver, query):
 
    # wait until the search box has loaded:
    box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
 
    # find the search box in the html:
    driver.find_element_by_name("q").clear()
 
    # enter your search string in the search box:
    print(query)
    box.send_keys(query)
 
    # submit the query (like hitting return):
    box.submit()
 
    # initial wait for the search results to load
    wait = WebDriverWait(driver, 5)
 
    try:
        # wait until the first search result is found. Search results will be tweets, which are html list items and have the class='data-item-id':
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li[data-item-id]")))
 
        # scroll down to the last tweet until there are no more tweets:
        while True:
 
            # extract all the tweets:
            tweets = driver.find_elements_by_css_selector("li[data-item-id]")
 
            # find number of visible tweets:
            number_of_tweets = len(tweets)
            #print(number_of_tweets)
 
            
            # keep scrolling:
            #driver.execute_script("arguments[0].scrollIntoView();", tweets[-1])
            #print(tweets)"arguments[0].scrollIntoView();"//*[@class='session[username_or_email]']"
            wait = WebDriverWait(driver, 15)
            #elm = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@class='Icon Icon--large Icon--logo']")))
            #driver.execute_script("arguments[0].scrollIntoView();", elm)
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            #element = driver.find_element_by_class_name("Icon Icon--large Icon--logo")
            #driver.findElement(By.id("home_search_input")).sendKeys("demo");
            #driver.execute_script("arguments[0].scrollIntoView();", element)
            '''
            c = []
            for i in range(75):
                c.append(i)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(0.8)
            '''
            SCROLL_PAUSE_TIME = 2

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            
            try:
                # wait for more tweets to be visible:
                wait.until(wait_for_more_than_n_elements_to_be_present(
                    (By.CSS_SELECTOR, "li[data-item-id]"), number_of_tweets))
 
            except TimeoutException:
                # if no more are visible the "wait.until" call will timeout. Catch the exception and exit the while loop:
                break
           
        # extract the html for the whole lot:
        page_source = driver.page_source
 
    except TimeoutException:
 
        # if there are no search results then the "wait.until" call in the first "try" statement will never happen and it will time out. So we catch that exception and return no html.
        page_source=None
 
    return page_source


def extract_tweets(page_source):
    start = time.clock()
    soup = bs(page_source, 'lxml')
 
    tweets = []
    for li in soup.find_all("li", class_='js-stream-item'):
 
        # If our li doesn't have a tweet-id, we skip it as it's not going to be a tweet.
        if 'data-item-id' not in li.attrs:
            continue
 
        else:
            tweet = {
                'emoji':None,
                'tweet_id': li['data-item-id'],
                'text': None,
                #'user_id': None,
                #'user_screen_name': None,
                #'user_name': None,
                'created_at': None,
                #'retweets': 0,
                #'likes': 0,
                #'replies': 0
            }
 
            
            #Emojis
            escratch = []
            emoji_p = li.find_all("img", class_="Emoji--forText")
            for e in emoji_p:
                escratch.append(e.get("alt"))
            tweet['emoji'] = "".join(escratch)
            
            # Tweet Text
            text_p = li.find("p", class_="tweet-text")
            if text_p is not None:
                tweet['text'] = text_p.get_text()
            '''
            # Tweet User ID, User Screen Name, User Name
            user_details_div = li.find("div", class_="tweet")
            if user_details_div is not None:
                tweet['user_id'] = user_details_div['data-user-id']
                tweet['user_screen_name'] = user_details_div['data-screen-name']
                tweet['user_name'] = user_details_div['data-name']
             '''
            # Tweet date
            date_span = li.find("span", class_="_timestamp")
            if date_span is not None:
                tweet['created_at'] = datetime.datetime.fromtimestamp(int(date_span['data-time-ms']) / 1e3).date()
            '''
            # Tweet Retweets
            retweet_span = li.select("span.ProfileTweet-action--retweet > span.ProfileTweet-actionCount")
            if retweet_span is not None and len(retweet_span) > 0:
                tweet['retweets'] = int(retweet_span[0]['data-tweet-stat-count'])
 
            # Tweet Likes
            like_span = li.select("span.ProfileTweet-action--favorite > span.ProfileTweet-actionCount")
            if like_span is not None and len(like_span) > 0:
                tweet['likes'] = int(like_span[0]['data-tweet-stat-count'])
 
            # Tweet Replies
            reply_span = li.select("span.ProfileTweet-action--reply > span.ProfileTweet-actionCount")
            if reply_span is not None and len(reply_span) > 0:
                tweet['replies'] = int(reply_span[0]['data-tweet-stat-count'])
             '''
            tweets.append(tweet)
    stop = time.clock()
    return tweets

noptions = Select(title="Number of Tweets", options=['100', '500', '1000', '5000'], value='100', width = 200)
radio_button_group = RadioButtonGroup(labels=["Hashtag", "Search Term"], active=0, width = 200)
text_input = TextInput(value="", width = 200, title = "Search Term")
button = Button(label="Submit", width = 200)
buttoncomb = row(button, Div(text = ""))

t = []
def logic(query):
    start = time.clock()
    driver = init_driver()
    username = 'dhavalsawlani1995@gmail.com'
    password = 'iloveugod'
    login_twitter(driver, username, password)
    #query = "#trump since:2018-10-01"
    page_source = search_twitter(driver, query)
    tweets = extract_tweets(page_source)
    close_driver(driver)
    end = time.clock()
    print((end-start)/60)
    t.append(tweets)

def get_tweets():
    N = 6
    dates = []
    startdate = (datetime.datetime.now() - datetime.timedelta(1))
    for i in range(N):
        dates.append((startdate - datetime.timedelta(i)).date())
    query = []
    searchterm = text_input.value
    for i in range(N):
        try:
            query.append(searchterm + " since:" + str(dates[i+1]) + " until:" + str(dates[i]))
        except:
            pass
    # Number of browsers to spawn
    thread_list = list()
    tt = []
    # Start test
    NN = len(query)
    for i in range(NN):
        th = threading.Thread(name='Test {}'.format(i), target=logic, args = [query[i]])
        th.start()
        time.sleep(2)
        print(th.name + ' started!')
        thread_list.append(th)
    
    # Wait for all thre<ads to complete
    for thread in thread_list:
        thread.join()
    print('Test completed!')
    print("Tweets extracted: " + str(sum([len(t[i]) for i in range(len(t))])))
    return t

source = ColumnDataSource(data=dict(Hashtag = [], Date = [], Tweet = []))
columns = [
TableColumn(field="Hashtag", title="Hashtag"),
TableColumn(field="Date", title="Date", formatter = DateFormatter()),
TableColumn(field="Tweet", title="Tweet"),
]
data_table = DataTable(source=source, columns=columns, width=550, height=400)

source_emoji = ColumnDataSource(data=dict(emoji = [], Count = [], Rank = []))
columns_emoji = [
TableColumn(field="emoji", title="emoji"),
TableColumn(field="Count", title="Count"),
TableColumn(field="Rank", title="Rank")
]
data_table_emoji = DataTable(source=source_emoji, columns=columns_emoji, width=550, height=400)
p = figure(title="Popular Emojis", toolbar_location=None, tools="",
          plot_height = 450, plot_width = 700)
def on_buttonpress():
    if text_input.value != "":
        tweets = get_tweets()
        allemojis = []
        ef = []
        for i in range(len(t)):
            rr = len(t[i])
            for j in range(rr):
                allemojis = "".join(t[i][j]['emoji'])
                emoji_list = emoji.emoji_lis(allemojis)
                if emoji_list != []:
                    ef.append(emoji_list)
                em = []
                for k in range(len(ef)):
                    for l in range(len(ef[k])):
                        em.append(ef[k][l]['emoji'])
                emoji_series = pd.Series(em)
                emojis = pd.DataFrame(emoji_series.value_counts()).reset_index().rename(columns = {'index':'emoji', 0: 'Count'})
                emojis['Rank'] = pd.Series(range(1, len(emojis)))
        emojis = emojis.head(10)
        emojis['Rank'] = emojis['Rank'].apply(lambda x: int(x))
        source_emoji.data = dict(
            emoji = emojis['emoji'],
            Count = emojis['Count'],
            Rank  = emojis['Rank']
        )
        labels = LabelSet(x="Rank", y="Count", text="emoji", level='glyph', render_mode='canvas', source = source_emoji, x_offset = -12,
                 text_font_size="12pt")
        p.vbar(x="Rank", top="Count", width = 0.95, source = source_emoji)
        p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
        p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
        p.y_range.start = 0
        p.x_range.start = 0
        p.xaxis[0].ticker.desired_num_ticks = 10
        p.add_layout(labels)
    else:
        pass
button.on_click(on_buttonpress)
#data_table.on_change('value', lambda attr, old, new: update_dt())
#status.on_change('value', lambda attr, old, new: pchange())
div1 = Div(text="""<img width="314" height="100" src="https://i0.wp.com/prismoji.com/wp-content/uploads/2016/12/cropped-emojis_only_logo.jpg?zoom=2.75&amp;fit=829%2C264&amp;ssl=1" class="custom-logo" alt="PRISMOJI" itemprop="logo" data-attachment-id="236" data-permalink="https://prismoji.com/cropped-emojis_only_logo-jpg/" data-orig-file="https://i0.wp.com/prismoji.com/wp-content/uploads/2016/12/cropped-emojis_only_logo.jpg?fit=829%2C264&amp;ssl=1" data-orig-size="829,264" data-comments-opened="1" data-image-meta="{&quot;aperture&quot;:&quot;0&quot;,&quot;credit&quot;:&quot;&quot;,&quot;camera&quot;:&quot;&quot;,&quot;caption&quot;:&quot;&quot;,&quot;created_timestamp&quot;:&quot;0&quot;,&quot;copyright&quot;:&quot;&quot;,&quot;focal_length&quot;:&quot;0&quot;,&quot;iso&quot;:&quot;0&quot;,&quot;shutter_speed&quot;:&quot;0&quot;,&quot;title&quot;:&quot;&quot;,&quot;orientation&quot;:&quot;0&quot;}" data-image-title="cropped-emojis_only_logo.jpg" data-image-description="<p>https://prismoji.com/wp-content/uploads/2016/12/cropped-emojis_only_logo.jpg</p>
" data-medium-file="https://i0.wp.com/prismoji.com/wp-content/uploads/2016/12/cropped-emojis_only_logo.jpg?fit=300%2C96&amp;ssl=1" data-large-file="https://i0.wp.com/prismoji.com/wp-content/uploads/2016/12/cropped-emojis_only_logo.jpg?fit=712%2C227&amp;ssl=1" src-orig="https://i0.wp.com/prismoji.com/wp-content/uploads/2016/12/cropped-emojis_only_logo.jpg?fit=829%2C264&amp;ssl=1" scale="2.75">
 <a href="https://www.prismoji.com">""",
width=320, height=100)
div2 = Div(text = """<div class="bottom_alligner" style="text-align:bottom; position:absolute; bottom:0px;"</div><h1>PRISMOJI EMOJI APP</h1>""",
           width = 300, height = 100)
layout = column(row(div1, div2), column(row(widgetbox(text_input, width = 220), column(Div(text = ""), buttoncomb)) ,
                                        row(p)))
curdoc().add_root(layout)
curdoc().title = "PRISMOJI EMOJI APP"

