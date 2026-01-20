from client.main import main
from nicegui import ui

if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(native=True, window_size=(1500, 750), title="Rift")