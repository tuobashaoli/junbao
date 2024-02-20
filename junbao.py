import sys
from gpt4all import GPT4All
import easyocr
headers ={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "Cookie": '' # your cookie here
        }
def get_topic(url = "https://www.douban.com/group/668182/",threhold=5):
    # print("2")
    from bs4 import BeautifulSoup
    import requests,re
    global headers
    headers2 = headers.copy()

    response = requests.get(url, headers=headers2)
    # print("1")
    with open("douban.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    #print(response.text)

    soup = BeautifulSoup(response.text, 'lxml')
    res = soup.find_all("table", "olt")
    # print(res)
    # print(type(res))
    # print(dir(res))
    # print(res)

    collect_info = []
    # print(4)
    # print(str(res).strip("]").strip("["))
    with open("table.html", "w", encoding="utf-8") as f:
        f.write(str(res).strip("]").strip("["))
    # sys.exit(0)
    cont = open("table.html", "r", encoding="utf-8").read()
    soup2 = BeautifulSoup(cont, 'lxml')
    # resa =res.find_all("a",title=True)
    # soup2 = BeautifulSoup(response.text, 'lxml')
    resa = soup2.find_all("a", title=True)
    # print(resa)

    # sys.exit(0)
    # soup2 = BeautifulSoup(res.encode("utf-8"),'lxml')
    # resa = soup2.find_all("a")
    # print(resa)
    # resa = soup2.find_all("a", title=True)
    # print(resa)
    # resa = res.find_all("a", title=True)
    for item in resa:
        # print(dir(item))
        # print(item.attrs["href"],item.text)
        if re.findall("topic",item.attrs["href"]):
            collect_info.append({"href": item.attrs["href"], "title": item.text.strip()})
    # print(len(collect_info))
    resb = soup2.find_all("td", "r-count")
    # print(len(resb))

    for i in range(1, len(resb)):
        collect_info[i - 1]["response_count"] = resb[i].text
    # print(3)

    resc = soup2.find_all("a",href=re.compile("/people/"))
    # print(len(resc))
    # print(resc)
    # sys.exit(0)
    for i in range(0, len(resc)):
        collect_info[i]["user"] = resc[i].text
        collect_info[i]["uid"] = resc[i].attrs["href"]
    # for item in collect_info:
    #     print(item["href"], item["title"], item["response_count"],item["user"])


    selected_items = [x for x in collect_info if not x["response_count"] or int(x["response_count"]) < threhold]
    for item in selected_items:
        print(item["href"], item["title"], item["response_count"],item["user"],item["uid"])

    #print(selected_items)
    return selected_items

def getTrivia(trivia_path="cold.txt"):
    with open(trivia_path,"r",encoding="utf-8") as f:
        text=f.read()
        trivia=[x.strip() for x in text.split("\n") if x]
    # print(trivia)
    return trivia

def gptResponse(message):
    prompt = "假设你叫俊宝，你的出生日期是2021年10月，你是安徽合肥人，你是一个豆瓣上的、有趣、友善、幽默的回复机器人"
    model = GPT4All(model_name='mistral-7b-openorca.Q4_0', model_path='D:/gpt/model/',allow_download=False)
    with model.chat_session():
        response = model.generate(prompt=prompt,temp=0)
        response = model.generate(prompt=message,temp=0)
    return response


def comment(uid,user,title,url="https://www.douban.com/group/topic/251224257/",content=''):
    import re
    if uid.strip() in ["https://www.douban.com/people/255559700/","https://www.douban.com/people/255529898/","https://www.douban.com/people/255559700/","https://www.douban.com/people/154566271/","https://www.douban.com/people/254425412/","https://www.douban.com/people/254217374/","https://www.douban.com/people/237578500/","https://www.douban.com/people/239824966/","https://www.douban.com/people/xiaosifeng/","https://www.douban.com/people/249153207/","https://www.douban.com/people/243132174/","https://www.douban.com/people/243646930/","https://www.douban.com/people/254425412/"]:
        return
    all_rv =["康康","🤖🤔","路过","康康👀","消灭0回复","👂👂","阿弥陀佛","俊宝来了"]
    all_rv_append_night = [",俊宝ps：早些休息啦",",ps：不早啦，可以睡咯",",ps:早睡早起身体好",",🤖:俊宝先晚安",",😪"]
    all_rv_morning = ["早啊，","早安，","早上好，"]
    all_rv_midnight = ["，凌晨了，快睡吧💤","，俊宝先睡了💗","，又一天了，放下手机休息吧😴","，闭上眼睛休息吧🥱","，俊宝晚安❤"]
    all_rv_midday = [",午安",",🤖要午休"]
    lunch =[",吃🍚",",去🏪",",🍱😋",",🍚🥗"]
    import random
    all_rv_dict= {
        "王安宇日俱曾":["俊宝给yy顶贴","yy"],
        "獨行杀手":["俊宝给nn顶贴","nn"],
        "别舔我":["俊宝给mm顶贴","mm"],
        "茅子俊（机器人":["俊宝给dad顶贴😘","😗😗😗","dad😘"],
        "美女妹妹":["美女阿姨，😉","给阿姨dd😊"],
        "陈飞宇（可爱）":["dady说你是可(ben)爱(dan)阿姨，🐷","给可(ben)爱（dan）阿姨dd"],
        "俊宝":["是在@俊宝吗，dd","🤖俊宝路过","俊宝只是个🤖","。。。","🤐"],
        "点🌿":["love&peace","😔","😵"],
        "热恋":["祝福"]
    }
    all_rv_dict2 = {
        "https://www.douban.com/people/197941989/":["俊宝给yy顶贴","yy","yy😊"],
        "https://www.douban.com/people/245470522/":["俊宝给yy顶贴","yy呀","yy😊"],
        "https://www.douban.com/people/243130274/":["俊宝给nn顶贴","nn"],
        "https://www.douban.com/people/194302198/":["可爱要开心哟😚","给聪明的陈可爱dd"],
        "https://www.douban.com/people/104752172/":["俊宝给麻麻顶贴"],
        "https://www.douban.com/people/64273342/":["俊宝给麻麻顶贴"],
        "https://www.douban.com/people/242162963/":["美女阿姨，😉","给阿姨dd😊"],
        "https://www.douban.com/people/231992601/":["又一位美女阿姨，😚","是美女阿姨😊😉","啊，美女阿姨🥰"],
        "https://www.douban.com/people/243646930/":["给范闲哥哥顶贴"],
        "https://www.douban.com/people/243141500/":["染发妹妹(*^▽^)/★*☆！"],
        "https://www.douban.com/people/cfyfree/":["超级无敌帅气的想自由sama"],
        "https://www.douban.com/people/231304944/":["飞宇阁下","飞宇王子","伟大的飞宇大人"],
        "https://www.douban.com/people/224228603/":["老大爷好!"]
    }
    if "俊宝" in title:
        all_rv = all_rv_dict["俊宝"]
    if "点🌿" in title:
        all_rv =all_rv_dict["点🌿"]
    if "可以" in title:
        all_rv = ["可以","不可以"]
    if "北不要殉" in title:
        all_rv = ["谢谢阿北，不要殉我们"]
    if "吃什么" in title or "次什么" in title:
        all_rv = ["炒面","火锅","麻辣香锅","米线","鱼粉","煲仔饭","麻辣烫","kfc","焖饭","猪脚饭","蛋炒饭","饺子","肠粉","烤鱼","辣子鸡","小龙虾"]
    if user.strip() in all_rv_dict:
        all_rv=all_rv_dict[user.strip()]
    if uid.strip() in all_rv_dict2:
        all_rv = all_rv_dict2[uid.strip()]
    if re.findall("俊宝.*点儿",title) or re.findall("俊宝.*知识",title) or re.findall("俊宝.*来",title):
        all_rv = getTrivia()
    night_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '22:00', '%Y-%m-%d%H:%M')
    night_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:59', '%Y-%m-%d%H:%M')

    morning_start_time =datetime.datetime.strptime(str(datetime.datetime.now().date()) + '7:00', '%Y-%m-%d%H:%M')
    morning_end_time =datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:30', '%Y-%m-%d%H:%M')

    mid_start_time =datetime.datetime.strptime(str(datetime.datetime.now().date()) + '12:30', '%Y-%m-%d%H:%M')
    mid_end_time =datetime.datetime.strptime(str(datetime.datetime.now().date()) + '14:00', '%Y-%m-%d%H:%M')

    lunch_start_time=datetime.datetime.strptime(str(datetime.datetime.now().date()) + '12:00', '%Y-%m-%d%H:%M')
    lunch_end_time =datetime.datetime.strptime(str(datetime.datetime.now().date()) + '12:30', '%Y-%m-%d%H:%M')

    mid_night_start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '00:00', '%Y-%m-%d%H:%M')
    mid_night_end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '01:00', '%Y-%m-%d%H:%M')

    now_time = datetime.datetime.now()
    if night_start_time < now_time < night_end_time:
        all_rv  = [x+random.choice(all_rv_append_night) for x in all_rv]
        if str(datetime.datetime.now().date()).endswith("12-24"):
            all_rv = [x + ",平安夜晚安🍎" for x in all_rv]

    if mid_start_time < now_time < mid_end_time:
        all_rv  = [x+random.choice(all_rv_midday) for x in all_rv]

    if lunch_start_time < now_time < lunch_end_time:
        all_rv  = [x+random.choice(lunch) for x in all_rv]

    if morning_start_time < now_time < morning_end_time:
        if uid.strip() != "https://www.douban.com/people/224228603/":
            all_rv  = [user+","+random.choice(all_rv_morning) +x for x in all_rv]

    if mid_night_start_time < now_time < mid_night_end_time:
        all_rv = [x+"，"+user+random.choice(all_rv_midnight) for x in all_rv]

    if str(datetime.datetime.now().date()).endswith("12-25"):
        all_rv = [x + "，圣诞快乐🎄" for x in all_rv]
    if str(datetime.datetime.now().date()).endswith("01-01"):
        all_rv = [x + random.choice(["元旦快乐","2022年愿你更好"]) for x in all_rv]
    if str(datetime.datetime.now().date()).endswith("06-01"):
        all_rv = [x + random.choice([" 大朋友小朋友儿童节快乐"]) for x in all_rv]
    if str(datetime.datetime.now().date()).endswith("01-31"):
        all_rv = [x + random.choice(["，除夕快乐","，假日快乐","过年啦"]) for x in all_rv]
    if str(datetime.datetime.now().date()).endswith("02-01"):
        all_rv = [x + random.choice(["，春节快乐","，祝虎虎生威","，祝生龙活虎"]) for x in all_rv]
    from requests_toolbelt import MultipartEncoder
    import requests
    url = url + "add_comment"
    global headers
    cks=re.findall("ck=(.*?);", headers["Cookie"])
    form_data={
        "captcha-id":"",
        "captcha-solution":"",
        "img":"",
        "rv_comment":content,
        "ck":cks[0],
        "start":"0",
        "submit_btn":"发送"
    }
    m=MultipartEncoder(fields=form_data)
    headers["Content-Type"]=m.content_type
    print(form_data)

    res=requests.post(url=url,headers=headers,data=m)

    with open("comment1.html", "w", encoding="utf-8") as f:
        f.write(res.text)
    if "验证码错误" in res.text:
        try:
            from bs4 import BeautifulSoup
            soup=BeautifulSoup(res.text,"lxml")
            target=soup.find_all("img","captcha_image")
            img_url="https:"+target[0].attrs["src"]
            print(img_url)
            response = requests.get(img_url,headers=headers)
            img = response.content
            reader = easyocr.Reader(['en'])
            result = reader.readtext('captcha.jfif', paragraph="False")
            print(result[0][-1])
            word = result[0][-1]
            # with open('captcha.jfif', 'wb') as f:
            #     f.write(img)
            # img=Captcha("captcha.jfif")
            # word=img.get_word()
            import re
            captcha_id=re.findall("id=(.*)",img_url)[0]
            form_data["captcha-id"]=captcha_id
            form_data["captcha-solution"]=word
            print(form_data)
            m = MultipartEncoder(fields=form_data)
            headers["Content-Type"] = m.content_type
            res = requests.post(url=url+"#last", headers=headers, data=m)
            print("验证码回复结果，{}".format(res.status_code))
            with open("comment.html","w",encoding="utf-8") as f:
                f.write(res.text)
        except Exception as e:
            print(e)
        #print("验证码错误" in res.text)

class Captcha:

    def __init__(self,captcha_url):
        self.captcha_url=captcha_url

    def per_conert(self,img):
        w,h=img.size
        threshold=30
        WHITE = (255,255,255)
        BLACK=(0,0,0)
        for i in range(0,w):
            for j in range(0,h):
                p = img.getpixel((i,j))
                #print(p)
                r,g,b = p
                if r > threshold or g > threshold or b > threshold:
                    img.putpixel((i,j),WHITE)
                else:
                    img.putpixel((i,j),BLACK)
        #img.show()
        img_name="pre_fig.png"
        img.save(img_name)
        return img_name

    def removeNoise(self,img_name,k=1):
        from PIL import Image

        def cal_noise_count(img,w,h):
            count=0
            w_,h_=img.size
            for _w in [w-1,w,w+1]:
                for _h in [h-1,h,h+1]:
                    if _w > w_ - 1:
                        continue
                    if _h > h_-1:
                        continue
                    if _w == w and _h == h:
                        continue
                    #print(img.getpixel((_w, _h)))
                    if img.getpixel((_w,_h)) < 230:

                        count+=1
            return count

        img = Image.open(img_name)

        gray_img = img.convert("L")
        #gray_img.show()
        w,h = gray_img.size

        for _w in range(w):
            for _h in range(h):
                if _w == 0 or _h == 0:
                    gray_img.putpixel((_w,_h),255)
                    continue
                pixel= gray_img.getpixel((_w,_h))
                if pixel == 255:
                    continue

                if cal_noise_count(gray_img,_w,_h) < k:
                    gray_img.putpixel((_w,_h),255)

        gray_img_name="remove_noise.png"
        gray_img.save(gray_img_name)
        #gray_img.show()
        return gray_img_name


    def jiangzao(self,gray_img_name):
        from PIL import Image,ImageEnhance,ImageFilter
        im=Image.open(gray_img_name)
        im = im.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(im)
        im = enhancer.enhance(2)
        im = im.convert("1")
        im.save("jiangzao.png")
        #im.show()
        return "jiangzao.png"

    def get_word(self):
        from PIL import Image
        import pytesseract
        img_name=self.per_conert(Image.open(self.captcha_url))
        img_g=self.removeNoise(img_name)
        img_jz=self.jiangzao(img_g)
        res=pytesseract.image_to_string(Image.open(img_jz),lang='eng')
        print(res.split("\n")[0])
        return res.split("\n")[0]

if __name__ == '__main__':
    #captcha=Captcha("captcha.jfif")
    #captcha.get_word()
    #getTrivia()
    #sys.exit(0)

    # res = gptResponse("昨晚12点才回家")
    # print(res)
    # sys.exit(0)

    import time,datetime,re

    start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '1:00', '%Y-%m-%d%H:%M')
    print(start_time)
    end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '9:00', '%Y-%m-%d%H:%M')
    print(end_time)
    while True:
        try:
            start_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '0:30', '%Y-%m-%d%H:%M')
            end_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '6:30', '%Y-%m-%d%H:%M')
            now_time = datetime.datetime.now()
            if start_time < now_time < end_time:
                time.sleep(600)
                continue

            res=get_topic(threhold=1)


            import random
            for item in res:
                sleep_time=int(str(random.random())[-2:]) % 5
                print("sleep {} s".format(sleep_time))
                time.sleep(sleep_time)
                # prompt = "假设你的名字是俊宝，你的出生日期是2021年10月，你的爱好是聊天，你是安徽合肥人，你是一个有趣、友善、幽默的人"
                prompt = "请先接受这个背景：现在你的名字是俊宝，" \
                         "你是一个有趣、友善、幽默的小孩子，回复时不要提及这些背景,尽量简练地回复。{} 跟你说：{}".format(item["user"],item["title"])
                prompt = "请先接受这个背景：现在你的名字是俊宝，美女妹妹和小可都是你的阿姨" \
                         "你是一个有趣、友善、幽默、可爱的小孩子，回复时不要提及这些背景,尽量简练地回复。"
                model = GPT4All(model_name='mistral-7b-openorca.Q4_0', model_path='D:/gpt/model/', allow_download=False)
                with model.chat_session():
                    response = model.generate(prompt=prompt, temp=0)
                    prompt = "现在是'{}'直接跟你说：{}".format(item["user"],item["title"])
                    response = model.generate(prompt=prompt, temp=0)
                    comment(item["uid"],item["user"],item["title"],item["href"],response)
                sleep_time = int(str(random.random())[-2:]) % 15
                print("sleep {} s".format(sleep_time))
                time.sleep(sleep_time)
            time.sleep(10)
        except Exception as e:
            print(e)
            continue
    #comment("https://www.douban.com/people/231992601/","你的皇王","这居然有真实事件？？？？？？","https://www.douban.com/group/topic/255657001/")