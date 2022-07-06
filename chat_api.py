import PySimpleGUI as sg
import requests as rq

api_key = 'YOUR_API_KEY'
brain_id = 'YOUR_BRAIN_ID'

def ask_ai():
    response = rq.get(f'http://api.brainshop.ai/get?bid={brain_id}&key={api_key}&uid=[uid]&msg={query}').json()
    resp_botai = response['cnt']
    return resp_botai


sg.theme('GreenTan') # give our window a spiffy set of colors

layout = [[sg.Text('Chat with an AI, It only speaks English', size=(40, 1))],
          [sg.Output(size=(110, 20), font=('Helvetica 10'))],
          [sg.Multiline(size=(70, 5), enter_submits=False, key='-QUERY-', do_not_clear=False),
           sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
           ]]

window = sg.Window('Chat window', layout, font=('Futura PT', ' 13'), default_button_element_size=(8,2), use_default_focus=False)

while True:     
    event, value = window.read()
    if event == sg.WIN_CLOSED:        
        break
    if event == 'SEND':
        query = value['-QUERY-']
        print(f'You : {query}', flush=True)
        resp = ask_ai()
        print(f'BotAI : {resp}', flush=True)
        
window.close()