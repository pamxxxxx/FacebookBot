from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os, base64, json

mantequilla = "https://mbasic.facebook.com/groups/841529052584872"
aw = "https://mbasic.facebook.com/groups/830198010427436"
selfProfile = "https://mbasic.facebook.com/profile.php?fref=pb"


def toBase64(s):
    b = bytes(s, "utf-8")
    s64 = base64.b64encode(b)
    return str(s64).replace("b'", "")


def getWelcome64():
    s = "Unit active at " + str(time.time())
    b = bytes(s, "utf-8")
    s64 = base64.b64encode(b)
    return str(s64).replace("b'", "")


def mfacebookToBasic(url):
    if "m.facebook.com" in url:
        return url.replace("m.facebook.com", "mbasic.facebook.com")
    else:
        return url


class Person():
    def __init__(self):
        self.name = ""
        self.profileLink = ""
        self.addLink = ""

    def __str__(self):
        s = ""
        s += self.name + ":\n"
        s += "Profile Link: " + self.profileLink
        if self.addLink != "":
            s += "Addlink ->: " + self.addLink
        return s

    def __repr__(self):
        self.__str__()


class Post():
    def __init__(self):
        self.posterName = ""
        self.description = ""
        self.numLikes = 0
        self.time = ""
        self.privacy = ""
        self.posterLink = ""
        self.linkToComment = ""
        self.linkToLike = ""
        self.linkToLikers = ""
        self.linkToReport = ""
        self.groupLink = ""
        self.linkToShare = ""
        self.linkToMore = ""
        self.numComents = 0

    def toDict(self):
        return self.__dict__.copy()

    def fromDict(self, d):
        self.__dict__ = d.copy()

    def from_json(self, j):
        self.fromDict(json.loads(j))

    def from_json_file(self, f):
        self.fromDict(json.loads(open(f, "rt").read()))

    def to_json(self):
        return json.dumps(self.toDict())

    def __str__(self):
        s = "\nPost by " + self.posterName + ": "
        s += self.description + "\n"
        s += "Likes: " + str(self.numLikes) + " - "
        s += "Comments: " + str(self.numComents) + " - "
        s += self.time + " "
        s += " - Privacy: " + self.privacy + "\n-"
        s += "\n Comment -> " + self.linkToComment + "\n"
        return s

    def __repr__(self):
        return self.__str__()


class FacebookBot(webdriver.PhantomJS):
    def __init__(self, images=False, pathToPhantomJs=None):
        #pathToPhantomJs = "E:\\ProgramFiles2\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe"
        relativePhatomJs = "\\phantomjs.exe"
        service_args = None
        if images == False:
            service_args = ['--load-images=no', ]
        if pathToPhantomJs == None:
            path = self, os.getcwd() + relativePhatomJs
        else:
            path = pathToPhantomJs
        #webdriver.PhantomJS.__init__(self, path, service_args=service_args)
            webdriver.PhantomJS.__init__(self)

    def get(self, url):
        super().get(mfacebookToBasic(url))

    def getScrenshotName(self, s, screenshot, screenshotPath="\\"):
        if screenshotPath == "\\": screenshotPath = os.getcwd()
        sf = screenshotPath + s + time.strftime("%a-%d-%m-%Y-%H-%M-%S") + ".jpg"
        if screenshot:
            self.save_screenshot(sf)
            return sf
        else:
            return ""

    def login(self, email, password, screenshot=True, screenshotPath="\\"):
        url = "https://mbasic.facebook.com"
        self.get(url)
        email_element = self.find_element_by_name("email")
        email_element.send_keys(email)
        pass_element = self.find_element_by_name("pass")
        pass_element.send_keys(password)
        pass_element.send_keys(Keys.ENTER)
        return self.getScrenshotName("Login_", screenshot, screenshotPath)


    def logout(self, screenshot=True, screenshotPath="\\"):
        url = "https://mbasic.facebook.com/logout.php?h=AffSEUYT5RsM6bkY&t=1446949608&ref_component=mbasic_footer&ref_page=%2Fwap%2Fhome.php&refid=7"
        self.get(url)
        return self.getScrenshotName("Logout_", screenshot, screenshotPath)


    def postText(self, text, screenshot=True, screenshotPath="\\"):
        url = "https://mbasic.facebook.com/"
        self.get(url)
        textbox = self.find_element_by_name("xc_message")
        textbox.send_keys(text)
        submit = self.find_element_by_name("view_post")
        return self.getScrenshotName("Post_", screenshot, screenshotPath)


    def newMessageToFriend(self, friendname, message, image1=None, image2=None, image3=None, screenshot=True,
                           screenshotPath="\\"):
        url = "https://mbasic.facebook.com/friends/selector/?return_uri=%2Fmessages%2Fcompose%2F&cancel_uri=https%3A%2F%2Fm.facebook.com%2Fmessages%2F&friends_key=ids&context=select_friend_timeline&refid=11"
        self.get(url)
        q = self.find_element_by_name("query")
        q.send_keys(friendname)
        q.send_keys(Keys.ENTER)
        id = self.page_source.split("/messages/compose/?ids=")[1].split('"><span>')[0].split('"><span>')[0]
        url = "https://mbasic.facebook.com/messages/compose/?ids=" + id
        self.get(url)
        t = self.find_element_by_name("body")
        t.send_keys(message)
        t.send_keys(Keys.ENTER)
        f1 = self.find_element_by_name("file1")
        f2 = self.find_element_by_name("file2")
        f3 = self.find_element_by_name("file3")
        if image1 != None: f1.send_keys(image1)
        if image2 != None: f2.send_keys(image2)
        if image3 != None: f3.send_keys(image3)
        send = self.find_element_by_name("Send")
        send.send_keys(Keys.ENTER)
        return self.getScrenshotName("MessageTo_" + friendname, screenshot, screenshotPath)

    def getPostInGroup(self, url, deep=2, screenshot=True, screenshotPath="\\"):
        self.get(url)
        ids = [4, 5, 6, 7, 9]
        posts = []
        for n in range(deep):
            for i in ids:
                print(i)
                post = Post()
                try:
                    p = self.find_element_by_id("u_0_" + str(i))
                    # print(p.text)
                    a = p.find_elements_by_tag_name("a")
                    post.posterName = a[1].text
                    try:
                        post.numLikes = int(a[3].text.split(" ")[0])
                    except ValueError:
                        post.numLikes = 0
                    # post.description = p.find_element_by_tag_name("p").text
                    post.time = p.find_element_by_tag_name("abbr").text
                    post.privacy = self.title  # p.text.split("· ")[1].split("\n")[0]
                    post.posterLink = a[0].get_attribute('href')
                    post.linkToComment = a[2].get_attribute('href')  # p.find_element_by_class_name("du").get_attribute('href')
                    post.linkToLike = a[4].get_attribute('href')
                    try:
                        post.numComents = int(a[5].text.split(" ")[0])
                    except ValueError:
                        post.numComents = 0
                    # post.linkToShare = a[5].get_attribute('href')
                    post.linkToLikers = a[1].get_attribute('href')
                    post.linkToMore = a[6].get_attribute('href')
                    posts.append(post)
                except Exception:
                    continue
            try:
                more = self.find_element_by_class_name("dm").find_elements_by_tag_name("a")[0].get_attribute('href')
                self.get(more)
            except Exception:
                print("can't get more :(")
        return posts, self.getScrenshotName("PostsIn" + self.title, screenshot, screenshotPath)


    def postInGroup(self, groupURL, text, screenshot=False, screenshotPath="\\"):
        self.get(groupURL)
        tf = self.find_element_by_name("xc_message")
        tf.send_keys(text)
        self.find_element_by_name("view_post").send_keys(Keys.ENTER)
        return self.getScrenshotName("PostI_" + self.title, screenshot, screenshotPath)

    def postImageInGroup(self, url, text, image1, image2="", image3=""):
        self.get(url)
        print("in url")
        v = self.find_element_by_name("view_photo")
        v.send_keys(Keys.ENTER)
        self.save_screenshot("debug.jpg")
        i1 = self.find_element_by_name("file1")
        i2 = self.find_element_by_name("file2")
        i3 = self.find_element_by_name("file3")
        i1.send_keys(image1)
        i2.send_keys(image2)
        i3.send_keys(image3)
        print("before filters")
        filter = self.find_element_by_name("filter_type")
        filter.value_of_css_property(0)
        print("af¡ter filter")
        self.save_screenshot("debug.jpg")
        pre = self.find_element_by_name("add_photo_done")
        print("click")
        pre.click()
        m = self.find_element_by_name("xc_message")
        m.send_keys(text)
        vp = self.find_element_by_name("view_post")
        vp.click()
        self.save_screenshot("debug.jpg")
        return True

    def commentInPost(self, postUrl, text, screenshot=True, screenshotPath="\\"):
        self.get(postUrl)
        tb = self.find_element_by_name("comment_text")
        tb.send_keys(text)
        tb.send_keys(Keys.ENTER)
        return self.getScrenshotName("CommentingIn_" + self.title, screenshot, screenshotPath)

    def getGroupMembers(self, url, deep=3, start=0):
        seeMembersUrl = url + "?view=members&amp;refid=18"
        groupId = url.split("groups/")[1]
        step = 28
        r = "https://mbasic.facebook.com/browse/group/members/?id=$GROUPID$&start=$n$"
        rg = r.replace("$GROUPID$", groupId)
        members = []
        for d in range(start, start + deep):
            url = rg.replace("$n$", str(d * 30))
            self.get(url)
            # print(self.current_url)
            p = self.find_elements_by_class_name("p")  # BK cada profile
            for b in p:
                person = Person()
                h3 = b.find_elements_by_tag_name("h3")
                person.name = h3[0].text
                person.profileLink = h3[0].find_element_by_tag_name("a").get_attribute('href')
                try:
                    person.addLink = b.find_elements_by_tag_name("a")[1].get_attribute('href')  # puede haber error
                except Exception:
                    # print("No Addlink")
                    pass
                members.append(person)
                # more = self.find_element_by_id("m_more_item").find_element_by_tag_name("a").get_attribute('href')
                # self.get(more)
                # print(more)
        # print(len(members))
        return members

    def addFriend(self, url):
        self.get(url)
        try:
            bz = self.find_element_by_class_name("bz")
            l = bz.get_attribute('href')
            self.get(l)
            return True
        except Exception:
            # print("Can't add friend")
            return False

    def messageToUrl(self, url, text, screenshot=True, screenshotPath="\\"):
        self.get(url)
        name = self.title
        mb = self.find_elements_by_class_name("bx")
        mm = None
        for m in mb:
            if "messages" in m.get_attribute('href'):
                mm = m.get_attribute('href')
                break
        self.get(mm)
        b = self.find_element_by_name("body")
        b.send_keys(text)
        self.find_element_by_name("Send").click()
        return self.getScrenshotName("MessageTo_" + name, screenshot, screenshotPath)

