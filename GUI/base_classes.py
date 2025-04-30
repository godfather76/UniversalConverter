from GUI import ct
import config as config_data


# MainBase is used for steps 2-
class MainBase:
    def __init__(self, root, prev_step, *args, **kwargs):
        # super().__init__(root, *args, **kwargs)
        self.root = root
        self.container = ct.ScrollableFrame(self.root,
                                            row=1,
                                            sticky='nsew')
        self.bck_btn = ct.Button(self.container,
                                 text='Back',
                                 command=lambda: self.go_back(prev_step))  # Goes to main without asking (clicking the window's x asks)

    def go_back(self, prev_step, *args, **kwargs):
        if self.root.current_step == 2:
            self.root.tabs.grid()
        else:
            prev_step.container.grid()
        self.container.grid_remove()
        self.root.current_step -= 1
        if self.root.current_step != 3:
            self.root.next_btn.configure(state='normal')
        if self.root.next_btn.cget('state') == 'normal':
            self.root.next_var.set(f'Clicking this button will take you to step {str(self.root.current_step + 1)}')


class BaseTab(ct.Tabview):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root


class TabStarter:
    def __init__(self, master, root, *args, **kwargs):
        self.master = master
        self.root = root
        self.container = ct.ScrollableFrame(self.master,
                                            fg_color='transparent',
                                            sticky='nsew')
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.columnconfigure(0, weight=0)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=0)
