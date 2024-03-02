from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from bs4 import BeautifulSoup
from opencc import OpenCC
import requests as crawl_requests
from flask_cors import CORS
from flask_mail import Mail, Message
from google.oauth2 import id_token
from google.auth.transport import requests
import secrets
def generate_verification_code():
    return secrets.token_hex(3)

def get_ship_info():
    #crawl start
    #index :5=前後排+類型，7=稀有度，9=陣營，25=頭像src，35=名稱
    #裝備
    equipments=crawl_requests.get('https://wiki.biligame.com/blhx/%E8%A3%85%E5%A4%87%E5%9B%BE%E9%89%B4')
    equipments_info=BeautifulSoup(equipments.text,'html.parser')
    #船
    ship = crawl_requests.get("https://wiki.biligame.com/blhx/%E8%88%B0%E8%88%B9%E5%9B%BE%E9%89%B4")
    shipinfo=BeautifulSoup(ship.text,'html.parser')
    oringnal_data=list(shipinfo.find_all(class_="jntj-1 divsort"))
    cc = OpenCC('s2t')#翻譯
    data=list()#[前後排，船艦類型，稀有度，陣營，頭像網址，名稱]

    for i in range(len(oringnal_data)):
        character_info=str(oringnal_data[i]).split("\"")
        tmp=list()
        frontback_and_type=character_info[5].split(",,")
        if len(frontback_and_type)>1:
            tmp.append(cc.convert(frontback_and_type[0]))
            tmp.append(cc.convert(frontback_and_type[1]))
            tmp.append(cc.convert(character_info[7]))
            tmp.append(cc.convert(character_info[9]))
            tmp.append(cc.convert(character_info[25]))
            tmp.append(cc.convert(character_info[35]))
            data.append(tmp)
    return data

#def get_ship_info():
#    #crawl start
#    #index :5=前後排+類型，7=稀有度，9=陣營，25=頭像src，35=名稱
#    #裝備
#    equipments=crawl_requests.get('https://wiki.biligame.com/blhx/%E8%A3%85%E5%A4%87%E5%9B%BE%E9%89%B4')
#    equipments_info=BeautifulSoup(equipments.text,'html.parser')
#    #船
#    ship_info_xml = crawl_requests.get("https://wiki.biligame.com/blhx/%E8%88%B0%E8%88%B9%E5%9B%BE%E9%89%B4")
#    ship_info_xml_after_BeautifulSoup=BeautifulSoup(ship_info_xml.text,'html.parser')
#    ships_info_wait_for_iter=ship_info_xml_after_BeautifulSoup.find_all(class_="jntj-1 divsort")
#    ships_info=list()
#    for ship in ships_info_wait_for_iter:
#        ship.find()

def send_verification_email(email, verification_code):
    subject = 'Email Verification'
    body = f'Your verification code is: {verification_code}'
    msg = Message(subject, recipients=[email], body=body)
    mail.send(msg)


app = Flask(__name__)
CORS(app)#開發中開放接口
# 連接到 MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['azur_lane']  # 替換為你的資料庫名稱
collection = db['userdata']  # 替換為你的集合名稱

# 定義路由
@app.route('/getshipinfo',methods=['GET'])
def sendjson():
    return jsonify(get_ship_info())

#@app.route('/login',methods=['POST'])
#def login():
#    userinfo = request.get_json()
#    print(userinfo['_value'])
#    user=collection.find_one({'username':userinfo['_value']['username']})
#
#    if user:#找到使用者
#        if user['password']==userinfo['password']:
#            return user['fleet'] 
#        else:
#            jsonify({"message": "wrong_password"})
#    else:#轉跳至註冊
#        return jsonify({"message": "Login successful!"})

@app.route('/google_login',methods=['POST'])
def google_login():
    token=request.get_json()
    try:
        idinfo = id_token.verify_oauth2_token(token['credential'], requests.Request(), token['clientId'])
        user_info={'id':idinfo['sub'],'name':idinfo['name'],'avatar':idinfo['picture'],'user_fleet':[]}
        user=collection.find_one({'id':user_info['id']})
        if user:#有找到
            user_info['user_fleet']=user['user_fleet']
        else:
            collection.insert_one(user_info)
        return jsonify(user_info)
    except:
        return jsonify({"message": "error"})

@app.route('/upload',methods=['POST'])
def upload_fleet():
    user_info=request.get_json()
    query = {'id': user_info['id']}
    update_data = {'$set': {'user_fleet': user_info['user_fleet']}}
    collection.update_one(query, update_data)
    return jsonify({"message": "finish"}) 


if __name__ == '__main__':
    app.run(debug=True)  
    


