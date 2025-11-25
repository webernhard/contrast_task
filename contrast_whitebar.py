import tkinter as tk
from datetime import datetime
import os


# ##########################################################
# ### get/read infos from "global parameter file" (gpar) ### 
# #####################################################
with open("../_bio.settings/bips.gpar") as myfile: 				#or 'open("../../_bio.settings/bips.gpar")'
    SessionData = [line.rstrip() for line in myfile]

class ContrastExperiment:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("contrast-task - whitebar")
        self.root.attributes('-fullscreen', True)  # Vollbildmodus aktivieren
        self.root.configure(bg='white')

        # ESC zum Beenden
        self.root.bind('<Escape>', self.exit_program)

        # Mauszeiger unsichtbar machen
        self.root.config(cursor="none")

        # Experimentparameter
        self.bar_brightness = 0  # Schwarze Balken-Helligkeit (fixiert)
        self.background_brightness = 253  # Start mit hellem Hintergrund
        self.bar_width = 1000  # Horizontaler Balken - Breite
        self.bar_height = 150  # Horizontaler Balken - Höhe

        # Datensammlung
        self.results = []
        self.trial_start_time = None
        self.trial_count = 0  # Zähler für die Anzahl der Versuche
        self.max_trials = 2  # Maximale Anzahl der Durchgänge
        self.first_display = True  # Flag für ersten Anzeige
        self.show_instruction = True  # Flag für Instruktionsanzeige

        self.setup_ui()

    def setup_ui(self):
        # Canvas für Stimulus (Vollbild)
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bestätigen Button direkt im Hauptfenster
        self.confirm_button = tk.Button(
            self.root, text="Bestätigen", command=self.confirm_setting,
            font=('Arial', 14), bg='darkgrey', fg='white', padx=5, pady=3
        )
        self.confirm_button.place(relx=0.9905, rely=0.985, anchor='se')  # Positionierung des Buttons

        # Tasteneingaben für die Helligkeit
        self.root.bind('<Up>', self.increase_brightness)
        self.root.bind('<Down>', self.decrease_brightness)
        self.root.bind('<Left>', self.decrease_brightness_fine)
        self.root.bind('<Right>', self.increase_brightness_fine)
        self.root.bind('<Return>', self.confirm_setting)  # Enter-Taste
        self.root.bind('<space>', self.confirm_setting)  # Space-Taste
        self.root.bind('<Button-1>', self.confirm_setting)  # Linke Maustaste

        # Canvas nach dem Rendern aktualisieren - Instruktion zuerst anzeigen
        self.root.after(100, self.show_instructions)

    def show_instructions(self):
        """Zeigt die Instruktionen vor dem Experiment an."""
        # Canvas löschen
        self.canvas.delete("all")
        
        # Schwarzer Hintergrund für Instruktionen
        self.canvas.configure(bg='black')
        
        # Canvas Größe ermitteln
        if self.first_display:
            self.canvas.update_idletasks()
            self.first_display = False
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Instruktionstext
        instruction_text = """
        
        Verwenden Sie die PFEILTASTEN um die Helligkeit des Hintergrundes anzupassen:

        
Für größere Helligkeitsschritte nutzen Sie
   die   ← / →   Pfeiltasten (links / rechts),

für feinere Anpassungen
   die   ↑ / ↓   Pfeiltasten (nach oben / unten).

Es gibt keine richtigen oder falschen Einstellungen.


Bitte stellen Sie die HELLIGKEIT DES HINTERGRUNDES so ein,
dass es für Sie im jetzigen Moment angenehm erscheint
UND Sie den Balken gut erkennen können.






Wenn Sie Ihre Einstellung gefunden haben, bestätigen Sie bitte Ihre Eingabe entweder 
mit der Enter- oder der Leertaste."""


        # Text in der Mitte anzeigen
        if canvas_width > 1 and canvas_height > 1:
            self.canvas.create_text(
                canvas_width // 2, canvas_height // 2,
                text=instruction_text,
                font=('Arial', 26),
                fill='white',
                justify='center',
                anchor='center'
            )

    def increase_brightness(self, event):
        """Erhöht die Hintergrundhelligkeit um 1."""
        if self.show_instruction:
            return  # Keine Helligkeitsänderung während Instruktion
        if self.background_brightness < 255:
            self.background_brightness += 1
            self.update_stimulus()

    def decrease_brightness(self, event):
        """Verringert die Hintergrundhelligkeit um 1."""
        if self.show_instruction:
            return  # Keine Helligkeitsänderung während Instruktion
        if self.background_brightness > 0:
            self.background_brightness -= 1
            self.update_stimulus()

    def increase_brightness_fine(self, event):
        """Erhöht die Hintergrundhelligkeit um 10."""
        if self.show_instruction:
            return  # Keine Helligkeitsänderung während Instruktion
        if self.background_brightness <= 245:  # Maximalwert 255
            self.background_brightness += 10
            self.update_stimulus()

    def decrease_brightness_fine(self, event):
        """Verringert die Hintergrundhelligkeit um 10."""
        if self.show_instruction:
            return  # Keine Helligkeitsänderung während Instruktion
        if self.background_brightness >= 10:  # Minimalwert 0
            self.background_brightness -= 10
            self.update_stimulus()

    def update_stimulus(self):
        """Aktualisiert die Stimulus-Darstellung basierend auf dem aktuellen Wert der Hintergrundhelligkeit."""
        # Canvas löschen
        self.canvas.delete("all")

        # Hintergrundfarbe berechnen
        bg_color = f"#{self.background_brightness:02x}{self.background_brightness:02x}{self.background_brightness:02x}"
        # Canvas Hintergrund setzen
        self.canvas.configure(bg=bg_color)

        # Canvas Größe ermitteln - nur beim ersten Mal update_idletasks() aufrufen
        if self.first_display:
            self.canvas.update_idletasks()
            self.first_display = False
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Balkenfarbe bestimmen
        #if self.trial_count in [3, 4]:  # Für Durchgänge 3 und 4
        #bar_color = 'black'
        #else:  # Für andere Durchgänge
        bar_color = 'white'

        # Weißen oder schwarzen Balken in der Mitte zeichnen
        if canvas_width > 1 and canvas_height > 1:
            x1 = (canvas_width - self.bar_width) // 2
            y1 = (canvas_height - self.bar_height) // 2
            x2 = x1 + self.bar_width
            y2 = y1 + self.bar_height

            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=bar_color,
                outline=bar_color
            )

    def start_trial(self):
        """Startet einen neuen Versuch."""
        self.trial_start_time = datetime.now()
        self.trial_count += 1

        # Überprüfen, ob die maximale Anzahl der Durchgänge erreicht wurde
        if self.trial_count > self.max_trials:
            self.exit_program()  # Programm beenden, wenn die maximale Anzahl erreicht ist
            return

        # Hintergrundfarbe je nach Versuch setzen
        if self.trial_count % 2 == 1:  # Ungerade Versuche (1. Versuch)
            self.background_brightness = 253  # Heller Hintergrund
        else:  # Gerade Versuche (2. Versuch)
            self.background_brightness = 3  # Dunkler Hintergrund

        self.update_stimulus()

    def confirm_setting(self, event=None):
        """Bestätigt die aktuelle Einstellung und speichert sie."""
        # Wenn Instruktionen angezeigt werden, starte das Experiment
        if self.show_instruction:
            self.show_instruction = False
            self.start_trial()
            return
            
        if self.trial_start_time:
            trial_duration = (datetime.now() - self.trial_start_time).total_seconds()
            result = {
                'trial': len(self.results) + 1,
                'timestamp': datetime.now().isoformat(),
                'background_brightness': self.background_brightness,
                'bar_brightness': self.bar_brightness,
                'contrast_difference': abs(self.bar_brightness - self.background_brightness),
                'duration_seconds': round(trial_duration, 2)
            }
            self.results.append(result)
            # Automatisch speichern nach jeder Bestätigung
            self.save_results()
            # Für nächsten Versuch zurücksetzen
            self.reset_setting()
            self.start_trial()

    def reset_setting(self):
        """Setzt die Einstellung auf den Ausgangswert zurück."""
        self.update_stimulus()

    def save_results(self):
        """Speichert alle Ergebnisse in eine TXT-Datei."""
        if not self.results:
            return
        
        # data-Ordner erstellen, falls er nicht existiert
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        #filename = f"data\\contrast_task_whitebar_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        filename = os.path.join(data_dir, f"{SessionData[1]}_whitebar_{SessionData[0]}_{SessionData[2]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Header
                f.write(f"Experiment: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("Trial\tTimestamp\tBackground Brightness\tBar Brightness\tContrast Difference\tDuration (s)\n")
                f.write("\n" + "-" * 80 + "\n")
                # Daten
                for result in self.results:
                    f.write(f"{result['trial']}\t{result['timestamp']}\t{result['background_brightness']}\t{result['bar_brightness']}\t{result['contrast_difference']}\t{result['duration_seconds']}\n")
                # Durchschnittswerte
                f.write("-" * 80 + "\n")
                avg_bg = sum(r['background_brightness'] for r in self.results) / len(self.results)
                avg_contrast = sum(r['contrast_difference'] for r in self.results) / len(self.results)
                avg_duration = sum(r['duration_seconds'] for r in self.results) / len(self.results)
                f.write(f"Durchschnitt Hintergrund: {avg_bg:.1f}\n")
                f.write(f"Durchschnitt Kontrast: {avg_contrast:.1f}\n")
                f.write(f"Durchschnitt Dauer: {avg_duration:.1f}s\n")
        except Exception as e:
            print(f"Fehler beim Speichern der Ergebnisse: {e}")

    def exit_program(self, event=None):
        """Speichert die Ergebnisse und beendet das Programm."""
        self.save_results()  # Ergebnisse speichern
        self.root.quit()  # Programm beenden

    def run(self):
        """Startet das Experiment."""
        self.root.mainloop()

if __name__ == "__main__":
    experiment = ContrastExperiment()
    experiment.run()