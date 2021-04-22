
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from models.ConfigureMe import Constants
    from models.SubjectContainers import BoxOfSubjects
    from views.PLT.Simulation import ConcreteSimulation
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from views.PLT.TkinterPLTFrames import *
    import controllers.TkinterPLTControllers as ButtonsController

    plt.ioff()

    window = tk.Tk()

    Constants().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]
    window.geometry(Constants().get_main_canvas_size_tkinter())


    my_builder = TkinterPLTBuilder(window = window)
    my_builder.build()


    ButtonsController = ButtonsController.TkinterButtons(my_builder.get_component("SimulationFrame").get_animated_object())

    ButtonsController.bind_functions(my_builder.components["ButtonsFrame"])

    window.mainloop()