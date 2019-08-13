import PySimpleGUI as sg


def alert(title, message, timeout=10):
    timeout_sec = timeout * 1000 if timeout else None

    layout = [[sg.Text(message, font=200)],
              [sg.Ok(font=300)]]

    window = sg.Window(title, layout, disable_minimize=True, keep_on_top=True, size=(800, 300), use_default_focus=False)

    window.Read(timeout=timeout_sec)
    window.Close()
