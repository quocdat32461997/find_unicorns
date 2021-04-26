# front_end.py

# import dependencies
import PySimpleGUI as sg

from engine import Engine

def create_layout():

    return [
        [
            sg.Text('You can search unicorns here.'),
            sg.Input(key = '-IN-'),
            sg.Button('Search')
            ],
        [
            [sg.Text(size = (40, 1), key = '-LOG-')],
            [sg.Text(size = (40, 1), key = '-OUTPUT-')],
            [sg.Text(size = (40, 1), key = '-GOOGLE-OUTPUT-')],
            [sg.Text(size = (40, 1), key = '-BING-OUTPUT-')]
            ]
    ]

def main():
    # define layout
    layout = create_layout()

    # initialize search engine
    engine = Engine()

    # create window
    window = sg.Window(title = 'Find Unicorn', layout = layout)

    # event loop
    while True:
        event, values = window.read()

        # end program if user closes window
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Search':
            window['-LOG-'].update('Search results:') # print results

            # own engine output
            window['-OUTPUT-'].update(' '.join(['By our engine::', engine.search(values['-IN-'])]))

            # Google engine output
            window['-GOOGLE-OUTPUT-'].update(' '.join(['By Google:', engine.google(values['-IN-'])]))

            # bing engine output
            window['-BING-OUTPUT-'].update(' '.join(['By Bing:', engine.bing(values['-IN-'])]))

    # close GUI
    window.close()

if __name__ == '__main__':
    main()
