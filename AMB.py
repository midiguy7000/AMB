# AMB.py

import customtkinter as ctk
from mido import MidiFile
import AutoMIDIBlacker as amb
import os
import sys
import filedialog


class AutoMIDIBlackerGUI:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title('Auto MIDI Blacker')
        self.app.geometry('500x500')
        self.app.iconbitmap('_internal\\icon.ico')
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('green')

        self.midi1 = MidiFile(amb.midi1_path)
        self.total_measures_base = amb.get_total_measures(self.midi1)

        self.create_art_control_frame()
        self.create_measure_control_frame()
        self.create_finished_frame()

        self.art_ctrl_frame.place(relx=0.5, rely=0.5, anchor='center')

    def create_art_control_frame(self):
        self.art_ctrl_frame = ctk.CTkFrame(master=self.app, fg_color='#242424')
        ctk.CTkLabel(self.art_ctrl_frame, text='Select any art', font=('FOT-Rodin Pro EB', 30)).pack(pady=20)

        self.art_ctrl_ddm = ctk.CTkComboBox(master=self.art_ctrl_frame, values=[
            'Zigzag (88 Keys)', 'Double Zigzag (88 Keys)', 'Short Double Zigzag (88 Keys)',
            'Zigzag (128 Keys)', 'Double Zigzag (128 Keys)', 'Short Double Zigzag (128 Keys)', 'Helix (128 Keys)',
            'Double Helix (128 Keys)', 'Short Double Helix (128 Keys)'],
            font=('FOT-Rodin Pro EB', 15), width=310)
        self.art_ctrl_ddm.pack(pady=10)

        ctk.CTkButton(self.art_ctrl_frame, text='Next', font=('FOT-Rodin Pro EB', 15),
                      command=self.trans_to_measure).pack(pady=10)

    def create_measure_control_frame(self):
        self.measure_ctrl_frame = ctk.CTkFrame(master=self.app, fg_color='#242424')

        ctk.CTkLabel(self.measure_ctrl_frame, text='Measure to insert the art',
                     font=('FOT-Rodin Pro EB', 25)).pack(pady=20)

        self.measure_ctrl_slider = ctk.CTkSlider(master=self.measure_ctrl_frame, from_=1,
                                                 to=int(self.total_measures_base),
                                                 number_of_steps=int(self.total_measures_base),
                                                 command=self.update_label)
        self.measure_ctrl_slider.set(1)
        self.measure_ctrl_slider.pack(pady=10)

        self.measure_ctrl_label2 = ctk.CTkLabel(master=self.measure_ctrl_frame,
                                                text='1', font=('FOT-Rodin Pro EB', 20))
        self.measure_ctrl_label2.pack(pady=20)

        self.entry_button_frame = ctk.CTkFrame(master=self.measure_ctrl_frame, fg_color="transparent")
        self.entry_button_frame.pack(pady=10)

        self.measure_ctrl_entry = ctk.CTkEntry(master=self.entry_button_frame, placeholder_text='Enter value here')
        self.measure_ctrl_entry.pack(side='left', padx=5)

        ctk.CTkButton(self.entry_button_frame, text='Enter', font=('FOT-Rodin Pro EB', 15),
                      command=self.update_from_entry).pack(side='left', padx=5)

        ctk.CTkLabel(self.measure_ctrl_frame, text='Amount of measures to repeat the art',
                     font=('FOT-Rodin Pro EB', 20)).pack(pady=20)

        self.measure_ctrl_entry2 = ctk.CTkEntry(master=self.measure_ctrl_frame,
                                                placeholder_text='Enter value here')
        self.measure_ctrl_entry2.pack(pady=20)

        ctk.CTkButton(self.measure_ctrl_frame, text='Next', font=('FOT-Rodin Pro EB', 15),
                      command=self.trans_to_convert, width=250).pack(pady=20)

    def create_finished_frame(self):
        self.finished_frame = ctk.CTkFrame(master=self.app, fg_color='#242424')
        ctk.CTkLabel(self.finished_frame, text='Your MIDI has been blacked successfully',
                     font=('FOT-Rodin Pro EB', 20)).pack(pady=20)
        ctk.CTkButton(self.finished_frame, text='Show in folder and close', font=('FOT-Rodin Pro EB', 15),
                      command=self.show_in_folder).pack(pady=10)

    def update_label(self, value):
        self.measure_ctrl_label2.configure(text=str(int(float(value))))

    def update_from_entry(self):
        value = int(self.measure_ctrl_entry.get())
        self.measure_ctrl_slider.set(value)
        self.measure_ctrl_label2.configure(text=str(value))

    def trans_to_measure(self):
        self.art_ctrl_frame.place_forget()
        self.measure_ctrl_frame.place(relx=0.5, rely=0.5, anchor='center')
        amb.set_vars_n_shii(str(self.art_ctrl_ddm.get()))

    def trans_to_convert(self):
        self.measure_ctrl_frame.place_forget()
        self.entry_button_frame.pack_forget()
        amb.set_vars_n_shii2(self.measure_ctrl_slider.get(), self.measure_ctrl_entry2.get(), self)

    def show_in_folder(self):
        folder_path = os.path.dirname(filedialog.save_path)
        os.startfile(folder_path)
        sys.exit()

    def show_finished_frame(self):
        self.finished_frame.place(relx=0.5, rely=0.5, anchor='center')

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    app = AutoMIDIBlackerGUI()
    app.run()
