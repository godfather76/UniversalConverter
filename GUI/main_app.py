import threading
from GUI import ct, base_classes, sql_to_files, files_to_sql, convert_files
import queue
import screeninfo
import conversion_logic
import database


# MainApp is the hub and is referred to as root for any sub-classes (such as login). It is the main portion of the GUI
class MainApp(ct.ctk.CTk, ct.Window):
    def __init__(self, config_data, *args, **kwargs):
        self.dev = False
        # self.dev = True
        super().__init__(*args, **kwargs)
        self.master = None  # this allows some classes to know this is the root
        self.config_data = config_data
        ct.ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
        ct.ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green, red is my own
        self.title("Ike's Data Conversion Tool")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.wd = 800
        self.ht = 650
        self.x = None
        self.y = None
        self.pri_wid = None
        self.pri_ht = None
        self.create_db_win = None
        self.convert_win = None
        self.get_screen_info()
        self.geometry(f'{str(self.wd)}x{self.ht}+{str(int(((self.pri_wid - self.wd) / 2) + self.x))}+'
                      f'{str(int(((self.pri_ht - self.ht) / 2) + self.y))}')
        # self.geometry(f'+{str(int(((self.pri_wid - self.wd) / 2) + self.x))}+'
        #               f'{str(int(((self.pri_ht - self.ht) / 2) + self.y))}')
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.closer = ct.CloseApp(self)
        self.protocol("WM_DELETE_WINDOW", self.closer.show)
        self.path_check_dict = {}
        self.tabs = None
        self.next_btn = None
        self.next_var = ct.ctk.StringVar(self)
        self.current_step = 1
        self.step2 = None
        self.dest_path = None
        self.db_path = None
        self.server_data = None
        self.step3 = None
        self.widgets()

    def widgets(self):
        ct.Label(self,
                 text='Universal Conversion Tool',
                 wraplength=300)
        self.tabs = ActionTabs(self,
                               row=1,
                               sticky='nsew')
        self.next_btn = ct.Button(self,
                                  text='Next Step',
                                  row=2,
                                  command=self.next)
        ct.Tooltip(anchor_widget=self.next_btn,
                   text='',
                   textvariable=self.next_var)
        self.next_var.set(f'Clicking this button will take you to step {str(self.current_step + 1)}')
        self.next_btn.configure(state='disabled')

    def next(self, *args, **kwargs):
        if self.current_step == 1:
            self.tabs.grid_remove()
            if not self.step2:
                self.step2 = convert_files.Step2(self, self.tabs)
            else:
                self.step2.container.grid()
        elif self.current_step == 2:
            self.step2.container.grid_remove()
            if not self.step3:
                self.step3 = convert_files.Step3(self, self.step2)
            else:
                self.step3.container.grid_remove()
            self.next_btn.configure(state='disabled')
            self.next_var.set('The button that takes you to the next step is currently disabled.')
        self.current_step += 1
        if self.next_btn.cget('state') == 'normal':
            self.next_var.set(f'Clicking this button will take you to step {str(self.current_step + 1)}')

    def get_screen_info(self):
        monitors = screeninfo.get_monitors()
        for mon in monitors:
            if mon.is_primary:
                self.pri_ht = mon.height
                self.pri_wid = mon.width
                self.x = mon.x
                self.y = mon.y


# for reference when I start the new thread for conversion
# def convert(self):
#     self.review_win.destroy()
#     self.withdraw()
#     self.jobq = queue.LifoQueue()
#     event = threading.Event()
#     self.t = convert.Convert(self.src_dict, self.final_dict, self.write_path, self.jobq, event)
#     self.display_win = convert.DisplayWindow(self, event)
#     self.after(50, self.check_queue)
#
# def check_queue(self):
#     try:
#         package = self.jobq.get(block=False)
#     except queue.Empty:
#         self.after(50, self.check_queue)
#         return
#     if package is not None:
#         self.display_win.update_display(package)
#         self.after(50, self.check_queue)
#     else:
#         self.t.join()
#         self.reviewing = False
#         self.deiconify()


class ActionTabs(base_classes.BaseTab):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root

        for act in self.root.config_data['conversion_actions']:
            self.add(act)
            self.tab(act).rowconfigure(0, weight=1)
            self.tab(act).columnconfigure(0, weight=1)
            self.widgets(act)

    def widgets(self, act, *args, **kwargs):
        if act == 'SQL to Files':
            sql_to_files.Widgets(self.tab(act), self.root)
        elif act == 'Files to SQL':
            files_to_sql.Widgets(self.tab(act), self.root)
        elif act == 'Convert Files':
            convert_files.Widgets(self.tab(act), self.root)


if __name__ == '__main__':
    test_win = ct.ctk.CTk()
    test_win.title("Test Window for Custom Tkinter Classes")
    values = ['Isaac', 'Tina', 'Ellie', 'Soren']
    cont = ct.ScrollableFrame(test_win,
                              sticky='NSEW')
    ct.RadioButton(cont,
                   row=0)
    ct.Button(cont,
              row=1)
    ct.CheckBox(cont,
                row=2)
    ct.ComboBox(cont,
                row=3)
    ct.Entry(cont,
             row=4)
    ct.OptionMenu(cont,
                  row=5,
                  values=values)
    pb = ct.ProgressBar(cont,
                        row=6)
    pb.start()
    ct.ScrollableFrame(cont,
                       row=7)
    ct.Scrollbar(cont,
                 row=8)
    ct.SegmentedButton(cont,
                       row=9,
                       values=values)
    ct.Slider(cont,
              row=10,
              number_of_steps=4)
    ct.Switch(cont,
              row=11)
    ct.TextBox(cont,
               row=12)
    test_win.mainloop()
