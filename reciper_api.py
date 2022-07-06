import requests as req
import PySimpleGUI as gui
import io
from PIL import Image as conv

api_key = 'YOUR_API_KEY'
api_id = 'YOUR_APP_ID'

h = 900
w = 1600
i = 0
img_ui = ''
url =f'https://api.edamam.com/api/recipes/v2?type=public&app_id={api_id}&app_key={api_key}'
t = ''
fotn_name = 'Futura PT Book'

def img_inbytes():
    #I convert the Img link in bytes, resize it and then convert in PNG couz was i jpg
    global img_ui
    url = img_ui
    response = req.get(url, stream=True).content
    pil_image = conv.open(io.BytesIO(response))
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    return png_bio.getvalue()

def checkbox(string, pre):
    return gui.Checkbox(string, key=f'-{pre} {string}-', font=(fotn_name, 11))

def title(title):
    return gui.Text(title, justification='center', size=(w, None), font=(fotn_name, 15))

def i_req(r, i):
    rec = r['hits'][i]

    recipe = rec['recipe']
    name = recipe['label']
    # print(name)
    img = recipe['images']['REGULAR']['url']
    # print(img)
    ingr = recipe['ingredientLines']
    # print(ingr)
    nutr = recipe['totalNutrients']

    nutra = []

    for var in nutr.values():
        i = var['label'] + ' : ' + str(var['quantity']) + var['unit']
        nutra.append(i)
    # print(nutra)    

    return {'name': name, 'img': img, 'ingr': ingr, 'nutr': nutra}

def upd(list):
    #reset the output
    window['-INGR-'].update('')

    window['-TOTALNUTR-'].update('')

    #update the output
    window['-NAME-'].update(list['name'])
    global img_ui
    img_ui = list['img']
    window['-IMG-'].update(img_inbytes())

    ig = list['ingr']
    for var in ig:
        window['-INGR-'].print(var)

    nt = list['nutr']
    for var in nt:
        window['-TOTALNUTR-'].print(var)


layout = [
    [title('Simple Recipe App')],
    [gui.Text('Insert Ingredient'), gui.Input(key='-INGRS-')],
    [gui.Text('Insert Ingredient to Exclude (Optional)'), gui.Input(key='-INGREX-')],
    [gui.Text('Insert Min-Max Time (Optional)'), gui.Input(key='-MinMaxT-')],
    [gui.Text('Insert Min-Max Calories (Optional)'), gui.Input(key='-MinMaxCAL-')],

    [title('Diet Type (Optional)')],

    [checkbox('Balanced', 'DT'),
     checkbox('High-Protein', 'DT'),
      checkbox('High-Fiber', 'DT'),
       checkbox('Low-Carb', 'DT'),
        checkbox('Low-Fat', 'DT'),
         checkbox('Low-Sodium', 'DT'),
    ],

    [title('Health Type (Optional)')],

    [checkbox('Alcohol-Free', 'HT'),
      checkbox('Crustacean-Free', 'HT'), 
       checkbox('Egg-Free', 'HT'), 
        checkbox('Fish-Free', 'HT'),
         checkbox('Gluten-Free', 'HT'),
          checkbox('Immuno-Friendly', 'HT'),
           checkbox('Keto-Friendly', 'HT'),
            checkbox('Kidney-Friendly', 'HT'),
             checkbox('Low Fat-Abs', 'HT'),
              checkbox('Low-Potassium', 'HT'),
               checkbox('Low-Sugar', 'HT'),
                checkbox('Mediterranean', 'HT'),
                 checkbox('Mollusk Free', 'HT')
                  ],
    
    [checkbox('Mustard-Free', 'HT'),
     checkbox('No-Oil-Added', 'HT'),
      checkbox('Penaut-Free', 'HT'),
       checkbox('Pescarian', 'HT'),
        checkbox('Pork-Free', 'HT'),
         checkbox('Red-Meat-Free', 'HT'),
          checkbox('Vegan', 'HT'),
           checkbox('Vegetarian', 'HT'),
            checkbox('Soy-Free', 'HT'), 
             checkbox('ShellFish-Free', 'HT')],

    [title('Cousine Type (Optional)')],

    [checkbox('American', 'CT'),
     checkbox('Asian', 'CT'),
      checkbox('British', 'CT'),
       checkbox('Caribbean', 'CT'),
        checkbox('Central Europe', 'CT'),
         checkbox('Chinese', 'CT'),
          checkbox('Estern Europe', 'CT'),
           checkbox('French', 'CT'),
            checkbox('Indian', 'CT'),
             checkbox('Italian', 'CT'),
              checkbox('Japanese', 'CT'),
               checkbox('Kosher', 'CT'), 
                checkbox('Mediterranean', 'CT'),
                 checkbox('Mexican', 'CT'),
                  checkbox('Middle Estern', 'CT'),
                   ],
    
    [checkbox('South East Asian', 'CT'),
      checkbox('Nordic', 'CT'),
       checkbox('South American', 'CT'),],

    [title('Meal Type (Optional)')],

    [checkbox('BreakFast', 'MT'),
     checkbox('Dinner', 'MT'),
      checkbox('Lunch', 'MT'),
       checkbox('Snack', 'MT'),
        checkbox('TeaTime', 'MT'),],

    [title('Dish Type (Optional)')],

    [checkbox('Biscuites and cookies', 'DiT'),
     checkbox('Bread', 'DiT'),
      checkbox('Cereals', 'DiT'),
       checkbox('Condiments and sauces', 'DiT'),
        checkbox('Deserts', 'DiT'),
         checkbox('Drinks', 'DiT'),
          checkbox('Main course', 'DiT'),
           checkbox('Pancake', 'DiT'),
            checkbox('Side dish', 'DiT'),
             checkbox('Soup', 'DiT'),
              checkbox('Starter', 'DiT'),
               checkbox('Sweets', 'DiT'),],

    [gui.Button(key='-SEND-', button_text = 'Press to Confirm')],

    [gui.Text('Recipe Name',
     key='-NAME-',
      text_color='red',
       size=(w, None), justification='center', font=(fotn_name, 18))],

    [gui.Button('Next Recipe', key='-NEXTRECIPE-')],

    [gui.Image(data='', key='-IMG-'),
     gui.Output(size=(80, 20), key='-INGR-'),
      gui.Output(size=(80, 20), key='-TOTALNUTR-')],


]

window = gui.Window('Simple Recipe App', layout, size=(w,h), )


while True:
    event, value = window.read()
    
    if event == gui.WIN_CLOSED:        
        break

    if(event == '-SEND-'):

        if(value['-INGRS-'] != ''):
            url = url + '&q=' + value['-INGRS-']

        if(value['-INGREX-'] != ''):
            url = url + '&excluded=' + value['-INGREX-']

        if(value['-MinMaxT-'] != ''):
            url = url + '&time=' + value['-MinMaxT-']

        if(value['-MinMaxCAL-'] != ''):
            url = url + '&calories=' + value['-MinMaxCAL-']


        for key, var in value.items():

            if var == True:

                d = key.split()

                if d[0] == '-DT':
                    url = url + '&diet=' + d[1][:-1].lower()
                
                if d[0] == '-HT':
                    url = url + '&health=' + d[1][:-1].lower()

                if d[0] == '-CT':
                    url = url + '&cuisineType=' + d[1][:-1]

                if d[0] == '-MT':
                    url = url + '&mealType=' + d[1][:-1]

                if d[0] == '-DiT':
                    url = url + '&dishType=' + d[1][:-1]

        t = req.get(url).json()
        list = i_req(r = t,i=i)  
        
        upd(list=list)
        
    if(event == '-NEXTRECIPE-'):
    
        if(i == 19):
           urlnew = t['_links']['next']['href']
           t = req.get(urlnew).json()
           i = 0
           list = i_req(r = t, i=i)  
           upd(list=list)

        else:
            i = i + 1
            list = i_req(r = t, i=i)  
            upd(list=list)
        

window.close()




