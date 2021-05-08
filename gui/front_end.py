# front_end.py

# import dependencies
import PySimpleGUI as sg
from collections import defaultdict

from engine import Engine

def create_layout():

    return [
        [sg.Text('Next Unicorn Startup?', pad = ((550,50), (0,0)), size = (30, 1), font = ('helvetica', 40), justification = 'center', text_color = 'yellow', auto_size_text = True)],
        [
            sg.Text('Search here:', font = ('helvetica', 20)),
            sg.Input(key = '-IN-', size = (30, 1), font = ('helvetica', 20)),
            sg.Button('Search', key = '-SEARCH-BUTTON-', font = ('helvetica', 20)),
            sg.Button('Vector-Space', key = '-VECTOR-SPACE-BUTTON-', font = ('helvetica', 20), auto_size_button = True),
            sg.Button('HITS', key = '-HITS-BUTTON-', font = ('helvetica', 20), auto_size_button = True),
            sg.Button('PageRank', key = '-PAGE-RANK-BUTTON-', font = ('helvetica', 20), auto_size_button = True),
            sg.Button('Google', key = '-GOOGLE-BUTTON-', font = ('helvetica', 20), auto_size_button = True),
            sg.Button('Bing', key = '-BING-BUTTON-', font = ('helvetica', 20), auto_size_button = True),
            sg.Button('More', key = '-MORE-BUTTON-', font = ('helvetica', 20), auto_size_button = True)
            ],
        [
            [sg.Text('Vector Space Output', font = ('helvetica', 20))],
            [sg.Multiline(default_text = 'Vector-Space Output', enable_events = True, size = (200, 6), key = '-VECTOR-SPACE-OUTPUT-', font = ('helvetica', 20))],
            [sg.Text('HITS Output', font = ('helvetica', 20))],
            [sg.Multiline(default_text = 'HITS Output', enable_events = True, size = (200, 6), key = '-HITS-OUTPUT-', font = ('helvetica', 20))],
            [sg.Text('PageRank Output', font = ('helvetica', 20))],
            [sg.Multiline(default_text = 'PageRank Output', enable_events = True, size = (200, 6), key = '-PAGE-RANK-OUTPUT-', font = ('helvetica', 20))],
            [sg.Text('Google Output', font = ('helvetica', 20))],
            [sg.Multiline(default_text = 'Google Output', enable_events = True, size = (200, 6), key = '-GOOGLE-OUTPUT-', font = ('helvetica', 20))],
            [sg.Text('Bing Output', font = ('helvetica', 20))],
            [sg.Multiline(default_text = 'Bing Output', enable_events = True, size = (200, 6), key = '-BING-OUTPUT-', font = ('helvetica', 20))]
            ]
    ]

def parse_output(inputs):
    if not inputs:
        return 'No result found'
    else:
        return '\n\n*******\n\n'.join(['=> Title: '+ x['title'] + '\n=> Description:' + x['description'] + '\n=> Link: ' + x['link'] for x in inputs])

def main():
    # define layout
    layout = create_layout()

    # initialize search engine
    engine = Engine()

    # create window
    window = sg.Window(title = 'Find Unicorn', layout = layout, size = (1900, 2048), auto_size_text = True)

    # event loop
    outputs = {
            '-VECTOR-SPACE-OUTPUT-' : None,
            '-HITS-OUTPUT-' : None,
            '-PAGE-RANK-OUTPUT' : None,
            '-GOOGLE-OUTPUT-' : None,
            '-BING-OUTPUT-' : None}

    while True:
        event, values = window.read()

        # end program if user closes window
        if event == sg.WIN_CLOSED:
            break
        elif event == '-SEARCH-BUTTON-':
            #outputs['-VECTOR-SPACE-OUTPUT-'] = parse_output(
            engine.search(values['-IN-'])

        elif event == '-VECTOR-SPACE-BUTTON-':
            # own engine output
            window['-VECTOR-SPACE-OUTPUT-'].update(parse_output(engine.search(values['-IN-'])))

        elif event == '-HITS-BUTTON-':
            window['-HITS-OUTPUT-'].update(
                    parse_output(engine.hits()))

        elif event == '-PAGE-RANK-BUTTON-':
            window['-PAGE-RANK-OUTPUT-'].update(
                    parse_output(engine.pagerank()))

        elif event == '-GOOGLE-BUTTON-':
            # Google engine output
            window['-GOOGLE-OUTPUT-'].update(parse_output(engine.google()))

        elif event == '-BING-BUTTON-':
            # bing engine output
            window['-BING-OUTPUT-'].update(parse_output(engine.bing()))
        elif event == '-MORE-BUTTON-':
            engine.search_page += 1

    # close GUI
    window.close()

if __name__ == '__main__':
    main()
