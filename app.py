if __name__ == "__main__":
    from models.ConfigureMe import MainConfiguration, Theme
    from tkinter import Tk
    from views.TkinterPLTFrames import TkinterPLTBuilder
    from views.Tkinter.MyMenu import MyMenu
    import controllers.TkinterPLTControllers as Controllers

    #plt.ioff()

    window = Tk()
    window.title("Pandemic Simulator")
    window.configure({"bg": Theme().default_bg})

    MainConfiguration().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]

    window.geometry(MainConfiguration().get_main_canvas_size_tkinter())

    view_builder = TkinterPLTBuilder(window=window)
    view_builder.build()

    ButtonsController = Controllers.TkinterButtons(view_builder.get_component("SimulationFrame").get_animated_object())
    SlidersController = Controllers.TkinterSimulationSettings()

    ButtonsController.bind_functions(view_builder.components["ScenarioFrame"].buttons)
    SlidersController.bind_functions(view_builder.get_component("ParametersFrame").sliders)
    m = MyMenu(window)
    window.configure(menu = m)
    window.mainloop()
