import threading
from GUI import ct, base_classes as base
from PIL import Image
from os import path, walk
import py7zr
from zipfile import ZipFile
import psutil


class Widgets(base.TabStarter):
    def __init__(self, master, root, *args, **kwargs):
        super().__init__(master, root, *args, **kwargs)
        self.file_button = None
        self.folder_button = None
        self.btn_frame = None
        self.sel_all_box = None
        self.del_all_btn = None
        self.path_top_label = None
        self.fldr_check = None
        self.fldr_var = ct.ctk.StringVar(self.root)
        self.aocbox = None
        self.sel_all_var = ct.ctk.StringVar(self.root)
        self.num_files = 0
        self.trash_img = (ct.ctk.CTkImage(light_image=Image.open('trash.jpg'),
                                          dark_image=Image.open('trash.jpg'),
                                          size=(30, 30)))

        self.widgets()

    def widgets(self, *args, **kwargs):
        ct.Label(self.container,
                 text='Convert Files',
                 columnspan=3)
        self.btn_frame = ct.Frame(self.container,
                                  row=1,
                                  columnspan=3)
        self.file_button = ct.Button(self.btn_frame,
                                     text='Add File(s)',
                                     command=self.add_files)
        ct.Tooltip(anchor_widget=self.file_button,
                   text='This button will open a file dialog where you can choose files to be added.')
        self.folder_button = ct.Button(self.btn_frame,
                                       text='Add Folder',
                                       column=1,
                                       command=self.select_folder)
        ct.Tooltip(anchor_widget=self.folder_button,
                   text='This button will open a file dialog where you can choose a folder to add. All supported files'
                        '\nfrom the selected folder will be added.\n'
                        'If the checkbox to the right of the button is checked, files from sub-folder will be added.\n'
                        'If the checkbox is unchecked, supported files from only the selected folder will be added.')
        self.fldr_check = ct.CheckBox(self.btn_frame,
                                      text='Drill Into Folder?',
                                      bg_color='transparent',
                                      column=2,
                                      command=self.change_fldr_var)
        self.fldr_var.set('Checking this box, which is currently unchecked, will make it so when you use the\n'
                          '"Add Folder" button, which is to the left, it will drill into sub-folders to find\n'
                          'supported files. Currently, it will only get supported files from the folder you '
                          'select.')
        ct.Tooltip(anchor_widget=self.fldr_check,
                   text='',
                   textvariable=self.fldr_var)

    def add_files(self, *args, **kwargs):
        all_supported = self.root.config_data['supported_extensions'] + self.root.config_data['archive_extensions']
        file_paths = ct.filedialog.askopenfilenames(filetypes=(('All Supported Extensions',
                                                                tuple(f'*{x}' for x in
                                                                      all_supported)),
                                                               ('Supported File Types',
                                                                tuple(f'*{x}' for x in
                                                                      self.root.config_data['supported_extensions'])),
                                                               ('Supported Archive Types',
                                                                tuple(f'*{x}' for x in
                                                                      self.root.config_data['archive_extensions'])),
                                                               ('All Files', '*.*')),
                                                    initialdir=self.root.config_data['base_path_for_conversions'])
        if file_paths:
            self.make_path_check_dict(file_paths)

    def make_path_check_dict(self, file_paths, is_archive=False, archive='', *args, **kwargs):
        if file_paths:
            self.root.next_btn.configure(state='normal')
            if not self.sel_all_box:

                self.sel_all_box = ct.CheckBox(self.container,
                                               row=3,
                                               text='Deselect All',
                                               command=self.select_deselect_all,
                                               ipadx=0,
                                               ipady=0,
                                               padx=0,
                                               pady=0)
                ct.Tooltip(anchor_widget=self.sel_all_box,
                           textvariable=self.sel_all_var,
                           text='')
                self.sel_all_var.set('Unchecking this box, which is currently checked, will deselect all files,\n'
                                     'removing them from the conversion.')
            else:
                self.sel_all_box.grid()
            self.sel_all_box.select()
            if not self.path_top_label:
                self.path_top_label = ct.Label(self.container,
                                               row=3,
                                               column=1,
                                               text='File Path',
                                               fg_color='transparent',
                                               bg_color='transparent',
                                               ipadx=0,
                                               ipady=0,
                                               padx=0,
                                               pady=0)
            else:
                self.path_top_label.grid()
            if not self.del_all_btn:
                self.del_all_btn = ct.Button(self.container,
                                             text='',
                                             row=3,
                                             column=2,
                                             image=self.trash_img,
                                             width=30,
                                             command=lambda: self.ask_remove('all'))
                ct.Tooltip(anchor_widget=self.del_all_btn,
                           text='This button will delete all the files from this conversion,\neffectively starting '
                                'over.')
            else:
                self.del_all_btn.grid()

        cols, rows = self.container.grid_size()
        row = rows + 1
        for file_path in file_paths:
            ext = path.splitext(file_path)[1]
            if ext in self.root.config_data['archive_extensions']:
                self.make_path_check_dict(self.get_zip_info(file_path, ext), is_archive=True, archive=file_path)
                continue
            file_path = path.normpath(file_path)
            filename = path.split(file_path)[1]
            existing_filenames = tuple(path.split(x)[1] for x in self.root.path_check_dict.keys())
            if filename not in existing_filenames:
                self.num_files += 1
                this_font = ct.ctk.CTkFont()
                self.root.path_check_dict[file_path] = {'box': ct.CheckBox(self.container,
                                                                           text='',
                                                                           command=lambda x=file_path: self.check_box(
                                                                               x),
                                                                           row=row,
                                                                           ipadx=0,
                                                                           ipady=0,
                                                                           padx=0,
                                                                           pady=0,
                                                                           sticky='w'),
                                                        'label': ct.Label(self.container,
                                                                          text=f'{str(self.num_files)}. {path.normpath(file_path)}',
                                                                          row=row,
                                                                          column=1,
                                                                          font=this_font,
                                                                          sticky='ew',
                                                                          anchor='w',
                                                                          fg_color='transparent',
                                                                          ipadx=0,
                                                                          ipady=0,
                                                                          padx=0,
                                                                          pady=0),
                                                        'font': this_font,
                                                        'del_btn': ct.Button(self.container,
                                                                             text='',
                                                                             row=row,
                                                                             column=2,
                                                                             image=self.trash_img,
                                                                             command=lambda
                                                                                 x=file_path: self.ask_remove(x),
                                                                             width=30,
                                                                             sticky='e',
                                                                             fg_color='transparent'),
                                                        'convert': True,
                                                        'variable': ct.ctk.StringVar(self.root),
                                                        'zip': None}
                if is_archive:
                    self.root.path_check_dict[file_path]['zip'] = archive
                ct.Tooltip(anchor_widget=self.root.path_check_dict[file_path]['box'],
                           textvariable=self.root.path_check_dict[file_path]['variable'],
                           text='')
                self.root.path_check_dict[file_path]['variable'].set(
                    'Unchecking this box, which is currently checked, will '
                    'deselect its associated file_path,\nremoving it from this '
                    f'conversion. The associated file_path is\n{file_path}')
                ct.Tooltip(anchor_widget=self.root.path_check_dict[file_path]['label'],
                           text='This row allows you to deselect its associated file_path, using the checkbox on the left.\n'
                                'Or delete it from the conversion, using the button to the right. The associated file_path '
                                f'is\n{file_path}')
                ct.Tooltip(anchor_widget=self.root.path_check_dict[file_path]['del_btn'],
                           text=f'Clicking this button will delete only its associated file_path from this conversion. The\n'
                                f'associated file_path is\n{file_path}')
                self.root.path_check_dict[file_path]['box'].select()
                row += 1

    def change_fldr_var(self):
        if self.fldr_check.get() == 1:
            self.fldr_var.set('Unchecking this box, which is currently checked, will make it so when you use the\n'
                              '"Add Folder" button, which is to the left, it will only get supported files from the\n'
                              'folder you select, it will not drill down into sub-folders. Currently, it will drill\n'
                              'into sub-folders.')
        elif self.fldr_check.get() == 0:
            self.fldr_var.set('Checking this box, which is currently unchecked, will make it so when you use the\n'
                              '"Add Folder" button, which is to the left, it will drill into sub-folders to find\n'
                              'supported files. Currently, it will only get supported files from the folder you '
                              'select.')

    def check_box(self, file, *args, **kwargs):
        if self.root.path_check_dict[file]['box'].get() == 0:
            self.root.path_check_dict[file]['font'].configure(overstrike=True)
            self.root.path_check_dict[file]['label'].configure(text_color='gray45')
            self.root.path_check_dict[file]['variable'].set('Checking this box, which is currently unchecked, will '
                                                            'select its associated file,\nadding it back in to this '
                                                            f'conversion. The associated file is\n{file}')
            self.root.path_check_dict[file]['convert'] = False
        else:
            self.root.path_check_dict[file]['font'].configure(overstrike=False)
            self.root.path_check_dict[file]['label'].configure(text_color='gray84')
            self.root.path_check_dict[file]['variable'].set('Unchecking this box, which is currently checked, will '
                                                            'deselect its associated file,\nremoving it from this '
                                                            f'conversion. The associated file is\n{file}')
            self.root.path_check_dict[file]['convert'] = True
        box_states = tuple(set(x['box'].get() for x in self.root.path_check_dict.values()))
        if len(box_states) == 1 and box_states[0] == 1:
            self.sel_all_box.select()
            self.sel_all_box.configure(text='Deselect All')
            self.sel_all_var.set('Unchecking this box, which is currently checked, will deselect all files, removing '
                                 'them from the conversion.')
            self.root.next_btn.configure(state='normal')
        elif len(box_states) == 1 and box_states[0] == 0:
            self.root.next_btn.configure(state='disabled')
            self.sel_all_box.deselect()
            self.sel_all_box.configure(text='Select All')
            self.sel_all_var.set('Checking this box, which is currently unchecked, will select all files, adding them '
                                 'to the conversion.')
        else:
            self.sel_all_box.deselect()
            self.sel_all_box.configure(text='Select All')
            self.root.next_btn.configure(state='normal')

    def ask_remove(self, file, *args, **kwargs):
        def go(f):
            self.remove_file(f)
            self.aocbox.withdraw()

        if file == 'all':
            text = 'You are about to remove all the files and start over. Continue?'
        else:
            # fn = path.split(file)[1]
            text = f'Are you sure you want to remove {file} from the list?'
        if file == 'all':
            btn = self.del_all_btn
        else:
            btn = self.root.path_check_dict[file]['del_btn']

        if not self.aocbox:
            self.aocbox = ct.AskOkCancelBox(self.root,
                                            text=text,
                                            b1_command=lambda x=file: go(x))
        else:
            self.aocbox.deiconify()
            self.aocbox.label.configure(text=text)
            self.aocbox.button1.configure(command=lambda x=file: go(x))
        self.aocbox.geometry(f'+{str(int(btn.winfo_rootx() - (self.aocbox.winfo_width() / 2) + 10))}'
                             f'+{str(int(btn.winfo_rooty() - (self.aocbox.winfo_height() / 2) - 50))}')
        self.aocbox.attributes('-topmost', 1)

    def remove_file(self, file, *args, **kwargs):
        if file == 'all':
            files = tuple(self.root.path_check_dict.keys())
        else:
            files = (file,)

        for f in files:
            self.num_files -= 1
            for wid in self.root.path_check_dict[f].values():
                try:
                    wid.grid_forget()
                except AttributeError:
                    # For attributes in the dict that aren't widgets, like the font
                    pass

            del self.root.path_check_dict[f]
        if file == 'all' or not tuple(self.root.path_check_dict.keys()):
            self.sel_all_box.grid_remove()
            self.path_top_label.grid_remove()
            self.del_all_btn.grid_remove()
            self.root.next_btn.configure(state='disabled')

    def select_deselect_all(self, *args, **kwargs):
        state = self.sel_all_box.get()
        for file in self.root.path_check_dict.keys():
            if self.root.path_check_dict[file]['box'].get() != state:
                self.root.path_check_dict[file]['box'].toggle()
        if state == 0:
            self.root.next_btn.configure(state='disabled')
        else:
            self.root.next_btn.configure(state='normal')

    def select_folder(self, *args, **kwargs):
        fldr_path = ct.filedialog.askdirectory(initialdir=self.root.config_data['base_path_for_conversions'])
        add_files = []
        if fldr_path:
            for dirpath, dirs, files in walk(fldr_path):
                for f in files:
                    if path.splitext(f)[1].lower() in self.root.config_data['supported_extensions'] or \
                            path.splitext(f)[1].lower() in self.root.config_data['archive_extensions']:
                        add_files.append(path.join(dirpath, f))
                if self.fldr_check.get() == 0:
                    break
        self.make_path_check_dict(add_files)

    def get_zip_info(self, file, ext, *args, **kwargs):
        supported_files = []
        if ext == '.7z':
            with py7zr.SevenZipFile(file, 'r') as z:
                files = tuple(z.files)
        elif ext == '.zip':
            with ZipFile(file, 'r') as z:
                files = z.filelist
            z.close()
        else:
            raise NotImplementedError
        for f in files:
            if path.splitext(f.filename)[1] in self.root.config_data['supported_extensions']:
                supported_files.append(f.filename)
        return supported_files

    def get_zip_password(self, file, *args, **kwargs):
        # Won't come into play until accessing the actual files because the list itself is not encrypted in zips
        raise NotImplementedError


class Step2(base.MainBase):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.path_check_dict = self.root.path_check_dict
        self.dropdown = None
        self.dest_path_select = None
        self.dest_path_label = None
        self.dest_path_var = ct.ctk.StringVar(self.root)
        self.dest_path_var.set(None)
        self.spreadsheet_widgets_list = []
        self.db_type_dropdown = None
        self.db_widgets_list = []
        self.select_db_btn = None
        self.db_path_label = None
        self.db_path_var = ct.ctk.StringVar(self.root)
        self.db_path_var.set('')
        self.ext_select = None
        self.widgets()
        self.spreadsheet_widgets()

    def widgets(self, *args, **kwargs):
        ct.Label(self.container,
                 text='Choose Output Extension and Target Path',
                 row=1,
                 column=1)
        self.dropdown = ct.OptionMenu(self.container,
                                      values=('Spreadsheet', 'Database'),
                                      row=2,
                                      column=1,
                                      command=self.change_type)

    def spreadsheet_widgets(self, *args, **kwargs):
        if not self.dest_path_select:
            self.ext_select = ct.OptionMenu(self.container,
                                            values=self.root.config_data['spreadsheet_extensions'],
                                            row=3,
                                            column=1)
            self.dest_path_select = ct.Button(self.container,
                                              row=10,
                                              text='Select Output Path',
                                              command=self.select_dest)
            self.dest_path_label = ct.Label(self.container,
                                            row=10,
                                            column=1,
                                            textvariable=self.dest_path_var)
            self.spreadsheet_widgets_list.append(self.ext_select)
            self.spreadsheet_widgets_list.append(self.dest_path_select)
            self.spreadsheet_widgets_list.append(self.dest_path_label)
        else:
            for wid in self.spreadsheet_widgets_list:
                wid.grid()
        for wid in self.db_widgets_list:
            wid.grid_remove()

    def database_widgets(self, *args, **kwargs):
        if not self.db_type_dropdown:
            self.db_type_dropdown = ct.OptionMenu(self.container,
                                                  values=self.root.config_data['database_types'],
                                                  row=10,
                                                  column=1,
                                                  command=self.change_db_type)
            self.select_db_btn = ct.Button(self.container,
                                           row=20,
                                           text='Select DB File',
                                           command=self.db_select)
            self.db_path_label = ct.Label(self.container,
                                          row=20,
                                          column=1,
                                          textvariable=self.db_path_var)
            self.db_widgets_list.append(self.db_type_dropdown)
            self.db_widgets_list.append(self.select_db_btn)
            self.db_widgets_list.append(self.db_path_label)
        else:
            for wid in self.db_widgets_list:
                wid.grid()
        for wid in self.spreadsheet_widgets_list:
            wid.grid_remove()

    def select_dest(self, *args, **kwargs):
        dest_path = ct.filedialog.askdirectory(initialdir=self.root.config_data['default_output_path'])
        if dest_path:
            self.dest_path_var.set(path.normpath(dest_path))
            self.root.dest_path = dest_path
            self.root.next_btn.configure(state='normal')

    def db_select(self, *args, **kwargs):
        db_extensions = tuple(x for x in self.root.config_data['database_extensions'])
        db_path = ct.filedialog.asksaveasfilename(initialdir=self.root.config_data['default_output_path'],
                                                  filetypes=(('Database Files', db_extensions),
                                                             ('All Files', '*.*')))
        ext = path.splitext(db_path)[1]
        if ext.strip() == '':
            if db_path.strip() != '':
                db_path += '.db'
            else:
                return
        elif ext not in db_extensions:
            try_again = ct.messagebox.askokcancel(title='Unsupported Extension',
                                             message=f'The extension type you entered ({ext}) is not a supported '
                                                     f'database type. Supported types are:\n'
                                                     f'{", ".join(db_extensions[:-1])}, and {db_extensions[-1]}\n'
                                                     f'Click Ok to try again or Cancel to go back to step 2.')
            if try_again:
                self.db_select()
            return
        self.root.db_path = db_path
        self.root.next_btn.configure(state='normal')
        self.db_path_var.set(path.normpath(db_path))

    def db_connect(self, *args, **kwargs):
        services = tuple(psutil.win_service_iter())
        sql_servers = tuple(x.name() for x in services if x.name().lower().startswith('mssql'))
        selector = ServerSelect(self.root, sql_servers)

    def change_type(self, *args, **kwargs):
        if self.dropdown.get() == 'Spreadsheet':
            self.spreadsheet_widgets()
            if not self.root.dest_path:
                self.root.next_btn.configure(state='disabled')
            else:
                self.root.next_btn.configure(state='normal')

        elif self.dropdown.get() == 'Database':
            self.database_widgets()
            db_type = self.db_type_dropdown.get()
            if db_type == 'File_Based SQL':
                if not self.root.db_path:
                    self.root.next_btn.configure(state='disabled')
                else:
                    self.root.next_btn.configure(state='normal')
            elif db_type == 'Server-Based SQL':
                if not self.root.server_data:
                    self.root.next_btn.configure(state='disabled')
                else:
                    self.root.next_btn.configure(state='normal')

    def change_db_type(self, *args, **kwargs):
        db_type = self.db_type_dropdown.get()
        if db_type == 'File-Based SQL':
            self.select_db_btn.configure(text='Select DB File',
                                         command=self.db_select)
            self.db_path_var.set(self.root.db_path)
        elif db_type == 'Server-Based SQL':
            self.select_db_btn.configure(text='Connect to DB',
                                         command=self.db_connect)
            self.db_path_var.set(self.root.server_data)


class ServerSelect(ct.Toplevel):
    def __init__(self, root, sql_servers, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.sql_servers = sql_servers
        self.widgets()

    def widgets(self, *args, **kwargs):
        ct.Label(self,
                 text=f'{self.sql_servers}')


class Step3(base.MainBase):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.root = root
        self.widgets()

    def widgets(self, *args, **kwargs):
        ct.Button(self.container,
                  text='Testing',
                  row=1)


if __name__ == '__main__':
    pass