
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from models.ConfigureMe import Constants
    from models.SubjectContainers import BoxOfSubjects
    from views.PLT.Simulation import MovingSubjects
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from views.TkinterPLTFrames import *
    import controllers.TkinterPLTControllers as ButtonsController

    plt.ioff()

    window = tk.Tk()

    Constants().MAIN_CANVAS_SIZE = [window.winfo_screenwidth(), window.winfo_screenheight()]
    window.geometry(Constants().get_main_canvas_size_tkinter())


    my_builder = TkinterPLTBuilder(window = window)
    my_builder.build()


    ButtonsController = ButtonsController.TkinterButtons(window.ani.event_source.start, window.ani.event_source.start,
                                                         window.ani.event_source.stop, window.ani.event_source.start)

    ButtonsController.bind_functions(my_builder.components["BUTTONS"])

    window.mainloop()