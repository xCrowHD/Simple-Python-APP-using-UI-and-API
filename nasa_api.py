import requests as req
import PySimpleGUI as gui
import io
from PIL import Image as conv
import datetime as date

api_key = "YOUR_API_KEY"
w = 1280
h = 800
datas= {}

chosen_date = "2022-05-05"

def url_call(date):
    data = req.get(f"https://api.nasa.gov/planetary/apod?date={date}&api_key={api_key}").json()

    data_descr = data["explanation"]
    data_img = data["url"]
    data_title  = data["title"]
    #Sometimes they dont have a copyright so we have to check for it
    if data.get("copyright") is not None:
        data_author = data["copyright"]
    else:
        data_author = "No Author"

    data_date = data["date"]
    datas.update({"descr":data_descr, "img":data_img, "title":data_title, "author":data_author, "date":data_date})
   
url_call(chosen_date) 

def img_inbytes():
    #I convert the Img link in bytes, resize it and then convert in PNG couz was i jpg
    url = datas["img"]
    response = req.get(url, stream=True).content
    pil_image = conv.open(io.BytesIO(response))
    pil_image = pil_image.resize((800, 400), conv.ANTIALIAS)
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    return png_bio.getvalue()

layout = [

    [gui.Text("Insert Data (YYYY-MM-DD)",
     background_color="#40739e",
      text_color="#f5f6fa"),
      
       gui.Input(key="-INPUT-"),
       
        gui.Button("Confirm", key="-CONFIRM-")],

    [gui.Text("Chosen Space Image",
     justification="center",
      size=(w , None), 
      background_color="#40739e" )],

    [gui.Text(datas["title"], key = "-TITLE-",
     justification="center",
      size=(w, None),
       font=("Futura PT Book", 18),
        text_color="#e84118" ,
         background_color="#0097e6")],

    [gui.Text(datas["author"], key = "-AUTHOR-",
     background_color="#40739e", 
      text_color="#f5f6fa" ),

      gui.Text(datas["date"], key = "-DATE-",
       background_color="#40739e", 
        text_color="#f5f6fa") ],

    [gui.Image(data=img_inbytes() , key = "-IMG-",)],

    [gui.Text(datas["descr"], key = "-DESCR-",
     size = (120, None),
      background_color="#2f3640",
       text_color="#f5f6fa")],
]

window = gui.Window("simple nasa app", layout, size=(w, h), font=("Futura PT Book", 14), background_color="#40739e")

while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break
    
    if event == "-CONFIRM-":
         chosen_date = values["-INPUT-"]
         url_call(chosen_date)
         window["-TITLE-"].update(datas["title"])
         window["-AUTHOR-"].update(datas["author"])
         window["-DATE-"].update(datas["date"])
         window["-IMG-"].update(img_inbytes())
         window["-DESCR-"].update(datas["descr"])

window.close()