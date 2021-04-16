
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from models.conf import Constants
    from models.BoxOfSomething import BoxOfSubjects
    from views.MatplotlibView import PlotOfSubjects
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    plt.ioff()
    window = tk.Tk()
    window.geometry("1280x1000")

    cnf = Constants
    ViewBox = PlotOfSubjects(cnf, container=BoxOfSubjects(cnf))

    canvas = FigureCanvasTkAgg(ViewBox.fig, window)
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill="x")


    window.ani = ViewBox.start_animation()
    start = tk.Button(window, text="Start", fg='blue', command = window.ani.event_source.start)
    stop = tk.Button(window, text="Stop", fg='blue', command = window.ani.event_source.stop)

    start.pack(side=tk.LEFT)
    stop.pack(side=tk.LEFT)

    window.mainloop()