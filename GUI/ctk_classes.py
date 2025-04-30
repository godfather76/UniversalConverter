# import threading
from abc import ABC
from tkinter import *
import customtkinter as ctk
from tkinter import filedialog, messagebox


def keep_alive():
    print("Feed me a better function as a command!")


class Widget:
    def hide(self, *args, **kwargs):
        self.grid_remove()

    def show(self, *args, **kwargs):
        self.grid()

    def delete(self, *args, **kwargs):
        self.grid_forget()


class TextWidget(Widget):

    ## Currently only works on Entry boxes that I know of
    def replace_all(self, string, *args, **kwargs):
        self.delete('1.0', 'end')
        self.insert('end', string)


class Window:
    def __init__(self, *args, **kwargs):
        pass

    def get_position(self, window, *args, **kwargs):
        x = window.winfo_x()
        y = window.winfo_y()
        return x, y

    def get_dimensions(self, window, *args, **kwargs):
        ht = window.winfo_height()
        wd = window.winfo_width()
        return ht, wd

    def position(self, *args, **kwargs):
        self.update()
        x, y = self.get_position(self.master)
        ht, wd = self.get_dimensions(self.master)
        self_ht = self.winfo_height()
        self_wd = self.winfo_width()
        self.geometry(f"+{str(int(x + ((wd - self_wd) / 2)))}+{str(int(y + ((ht - self_ht) / 2)) - (ht // 4))}")

    def hide(self, *args, **kwargs):
        self.withdraw()

    def show(self, *args, **kwargs):
        self.position()
        self.deiconify()

    def hide_all_widgets(self, *args, **kwargs):
        pass
        # print(self.winfo_children())
        # Find children and grid_remove them


# CustomTkinter classes: Each inherits the base class and the class Widget so we can make our own methods (like hide or
# show)
class Button(ctk.CTkButton, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class CheckBox(ctk.CTkCheckBox, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class ComboBox(ctk.CTkComboBox, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Entry(ctk.CTkEntry, TextWidget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Frame(ctk.CTkFrame, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class InputDialog(ctk.CTkInputDialog, Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Label(ctk.CTkLabel, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class OptionMenu(ctk.CTkOptionMenu, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class ProgressBar(ctk.CTkProgressBar, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.set(0)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class RadioButton(ctk.CTkRadioButton, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class ScrollableFrame(ctk.CTkScrollableFrame, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Scrollbar(ctk.CTkScrollbar, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class SegmentedButton(ctk.CTkSegmentedButton, Widget, ABC):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Slider(ctk.CTkSlider, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Switch(ctk.CTkSwitch, Widget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Tabview(ctk.CTkTabview, Widget, ABC):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class TextBox(ctk.CTkTextbox, TextWidget):
    def __init__(self, master, row=0, column=0, rowspan=1, columnspan=1, sticky='', ipadx=1, ipady=1,
                 padx=10, pady=10, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky, ipadx=ipadx,
                  ipady=ipady, padx=padx, pady=pady)


class Toplevel(ctk.CTkToplevel, Window):
    def __init__(self, master, close_cmd='', *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.update_idletasks()
        self.position()
        if close_cmd == '':
            close_cmd = self.hide
        self.protocol("WM_DELETE_WINDOW", close_cmd)
        self.attributes("-topmost", True)
        # self.after_idle(self.attributes, "-topmost", False)

    def hide(self, *args, **kwargs):
        self.withdraw()


# Below this are my own custom widgets and an adaptation of the CustomToolTip below
class AskOkCancelBox(Toplevel):
    def __init__(self, master, text='Are you sure?', title='Are you sure?', b1_command='', b2_command='',
                 wraplength=400,
                 *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        if b1_command == '':
            b1_command = self.master.destroy
        if b2_command == '':
            b2_command = self.withdraw
        self.b1_command = b1_command
        self.b2_command = b2_command
        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.title(title)
        self.label = Label(self, text=text, columnspan=2, wraplength=wraplength)
        self.button1 = Button(self, text='OK', command=b1_command, row=1, column=0)
        self.button2 = Button(self, text='Cancel', command=b2_command, row=1, column=1)


class CloseApp(AskOkCancelBox):
    def __init__(self, master, *args, **kwargs):
        text = 'Are you sure you would like to exit the program completely?'
        b1_command = self.exit_app
        b2_command = self.hide
        title = 'Exit Program?'
        super().__init__(master, text=text, b1_command=b1_command, b2_command=b2_command,
                         title=title, *args, **kwargs)
        self.master = master
        self.hide()

    def exit_app(self):
        self.master.destroy()


"""Tools for displaying tool-tips.
This includes:
 * an abstract base-class for different kinds of tooltips
 * a simple text-only Tooltip class
"""


class TooltipBase:
    """abstract base class for tooltips"""

    def __init__(self, anchor_widget):
        """Create a tooltip.
        anchor_widget: the widget next to which the tooltip will be shown
        Note that a widget will only be shown when showtip() is called.
        """
        self.anchor_widget = anchor_widget
        self.tipwindow = None

    def __del__(self):
        self.hidetip()

    def showtip(self):
        """display the tooltip"""
        if self.tipwindow:
            return
        self.tipwindow = tw = Toplevel(self.anchor_widget)
        # show no border on the top level window
        tw.wm_overrideredirect(1)
        try:
            # This command is only needed and available on Tk >= 8.4.0 for OSX.
            # Without it, call tips intrude on the typing process by grabbing
            # the focus.
            tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w,
                       "help", "noActivates")
        except TclError:
            pass

        self.position_window()
        self.showcontents()
        self.tipwindow.update_idletasks()  # Needed on MacOS -- see #34275.
        self.tipwindow.lift()  # work around bug in Tk 8.5.18+ (issue #24570)

    def position_window(self):
        """(re)-set the tooltip's screen position"""
        x, y = self.get_position()
        root_x = self.anchor_widget.winfo_rootx() + x
        root_y = self.anchor_widget.winfo_rooty() + y
        self.tipwindow.wm_geometry("+%d+%d" % (root_x, root_y))

    def get_position(self):
        """choose a screen position for the tooltip"""
        # The tip window must be completely outside the anchor widget;
        # otherwise when the mouse enters the tip window we get
        # a leave event and it disappears, and then we get an enter
        # event and it reappears, and so on forever :-(
        #
        # Note: This is a simplistic implementation; sub-classes will likely
        # want to override this.
        return 20, self.anchor_widget.winfo_height() + 1

    def showcontents(self):
        """content display hook for sub-classes"""
        # See ToolTip for an example
        raise NotImplementedError

    def hidetip(self):
        """hide the tooltip"""
        # Note: This is called by __del__, so careful when overriding/extending
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            try:
                tw.destroy()
            except TclError:  # pragma: no cover
                pass


class OnHoverTooltipBase(TooltipBase):
    """abstract base class for tooltips, with delayed on-hover display"""

    def __init__(self, anchor_widget, hover_delay=1000):
        """Create a tooltip with a mouse hover delay.
        anchor_widget: the widget next to which the tooltip will be shown
        hover_delay: time to delay before showing the tooltip, in milliseconds
        Note that a widget will only be shown when showtip() is called,
        e.g. after hovering over the anchor widget with the mouse for enough
        time.
        """
        super(OnHoverTooltipBase, self).__init__(anchor_widget)
        self.hover_delay = hover_delay

        self._after_id = None
        self._id1 = self.anchor_widget.bind("<Enter>", self._show_event)
        self._id2 = self.anchor_widget.bind("<Leave>", self._hide_event)
        self._id3 = self.anchor_widget.bind("<Button>", self._hide_event)

    def __del__(self):
        try:
            self.anchor_widget.unbind("<Enter>", self._id1)
            self.anchor_widget.unbind("<Leave>", self._id2)  # pragma: no cover
            self.anchor_widget.unbind("<Button>", self._id3)  # pragma: no cover
        except TclError:
            pass
        super(OnHoverTooltipBase, self).__del__()

    def _show_event(self, event=None):
        """event handler to display the tooltip"""
        if self.hover_delay:
            self.schedule()
        else:
            self.showtip()

    def _hide_event(self, event=None):
        """event handler to hide the tooltip"""
        self.hidetip()

    def schedule(self):
        """schedule the future display of the tooltip"""
        self.unschedule()
        self._after_id = self.anchor_widget.after(self.hover_delay,
                                                  self.showtip)

    def unschedule(self):
        """cancel the future display of the tooltip"""
        after_id = self._after_id
        self._after_id = None
        if after_id:
            self.anchor_widget.after_cancel(after_id)

    def hidetip(self):
        """hide the tooltip"""
        try:
            self.unschedule()
        except TclError:  # pragma: no cover
            pass
        super(OnHoverTooltipBase, self).hidetip()


class Tooltip(OnHoverTooltipBase):
    """Hover tip for the label widget"""

    def __init__(self, anchor_widget: Widget, text, hover_delay: int = 800, justify=LEFT, relief=SOLID, font=None,
                 anchor=None, width: int = 0, textvariable=None):
        super(Tooltip, self).__init__(anchor_widget=anchor_widget, hover_delay=hover_delay)
        self.text = text
        self.justify = justify
        self.relief = relief
        self.font = font
        self.anchor = anchor
        self.width = width
        self.textvariable = textvariable

    def showcontents(self):
        label = Label(self.tipwindow, text=self.text, justify=self.justify, font=self.font, anchor=self.anchor,
                      textvariable=self.textvariable, width=self.width)
        label.pack()


class TestWin(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("red.json")  # Themes: blue (default), dark-blue, green, red is my own
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.closer = CloseApp(self)
        self.protocol("WM_DELETE_WINDOW", lambda: self.closer.show())
        self.cont = None
        self.widgets()

    def widgets(self):
        self.title("Test Window for Custom Tkinter Classes")
        values = ['Isaac', 'Tina', 'Ellie', 'Soren']
        self.cont = ScrollableFrame(self, sticky='nsew')
        Label(self.cont, row=0, column=0, text='Button (with Tooltip)')
        btn = Button(self.cont, row=0, column=1)
        Tooltip(anchor_widget=btn, text='Test text for the Tooltip')
        Label(self.cont, row=1, text='CheckBox')
        CheckBox(self.cont, row=1, column=1)
        Label(self.cont, row=2, text='ComboBox')
        ComboBox(self.cont, row=2, column=1)
        Label(self.cont, row=3, column=0, text='Entry')
        Entry(self.cont, row=3, column=1)

        # Label(self.cont, text='Frame', row=0, column=2)
        # Frame(self.cont, row=0, column=3)
        Label(self.cont, text='InputDialog', row=1, column=2)
        Button(self.cont, text='Click for InputDialog', command=lambda: self.button_click('InputDialog'),
               row=1, column=3)
        Label(self.cont, row=2, column=2, text='Label')
        Label(self.cont, text="I'm a label!", row=2, column=3)
        Label(self.cont, row=3, column=2, text='OptionMenu')
        OptionMenu(self.cont, row=3, column=3, values=values)

        Label(self.cont, row=4, column=0, text='ProgressBar')
        pb = ProgressBar(self.cont, row=4, column=1)
        pb.start()
        Label(self.cont, text='RadioButton', row=5)
        RadioButton(self.cont, row=5, column=1)
        Label(self.cont, row=6, column=0, text='ScrollableFrame')
        ScrollableFrame(self.cont, row=6, column=1)
        Label(self.cont, row=7, text='Scrollbar')
        Scrollbar(self.cont, row=7, column=1)

        Label(self.cont, row=4, column=2, text='SegmentedButton')
        SegmentedButton(self.cont, row=4, column=3, values=values)
        Label(self.cont, row=5, column=2, text='Slider')
        Slider(self.cont, row=5, column=3, number_of_steps=4)
        Label(self.cont, row=6, column=2, text='Switch')
        Switch(self.cont, row=6, column=3)
        Label(self.cont, text='Tabview', row=7, column=2)
        tab = Tabview(self.cont, row=7, column=3)
        tab.add('Tab1')
        tab.add('Tab2')

        Label(self.cont, row=8, text='TextBox')
        TextBox(self.cont, row=8, column=1)
        Label(self.cont, text='Toplevel', row=9)
        Button(self.cont, text='Click for Toplevel', command=lambda: self.button_click('Toplevel'),
               row=9, column=1)

    def button_click(self, thing):
        if thing == 'InputDialog':
            InputDialog(text='Sample Input Dialog')
        elif thing == 'Toplevel':
            tl = Toplevel(self)
            tl.title("Sample Toplevel Window")
            tl.attributes('-topmost', 1)
            Label(tl, text='This is a sample Toplevel window')


if __name__ == '__main__':
    test_win = TestWin()
    test_win.mainloop()
