import sys
sys.path.append('/home/gergo/.local/lib/pypy3.6/site-packages')
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from models.ConfigureMe import MainConfiguration, Theme
    from models.SubjectContainers import DefaultContainer
    from views.PLT.Simulation import ConcreteSimulation
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from views.TkinterPLTFrames import *
    import controllers.TkinterPLTControllers as Controllers

    plt.ioff()

    window = tk.Tk()
    window.title("Pandemic Simulator")
    window.configure({"bg": Theme().default_bg})
    MainConfiguration().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]
    window.geometry(MainConfiguration().get_main_canvas_size_tkinter())


    my_builder = TkinterPLTBuilder(window = window)
    my_builder.build()


    ButtonsController = Controllers.TkinterButtons(my_builder.get_component("SimulationFrame").get_animated_object())
    SlidersController = Controllers.TkinterSimulationSettings()

    ButtonsController.bind_functions(my_builder.components["ScenarioFrame"].buttons)
    SlidersController.bind_functions(my_builder.get_component("ParametersFrame").sliders)
    checkboxes = my_builder.get_component("ScenarioFrame").get_checkboxes()
    window.mainloop()