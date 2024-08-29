import threading
import time
import re
import sys
import datetime
import shutil

# Fonction pour calculer la longueur visible d'une chaîne en ignorant les codes d'échappement ANSI
def visible_length(s):
    ansi_escape = re.compile(r'\x1b\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]')
    return len(ansi_escape.sub('', s))

# Fonction pour centrer une chaîne en tenant compte des codes ANSI
def center_with_ansi(s, width):
    vis_len = visible_length(s)
    total_padding = width - vis_len
    if total_padding <= 0:
        return s
    left_padding = total_padding // 2
    right_padding = total_padding - left_padding
    return ' ' * left_padding + s + ' ' * right_padding

# Fonction pour afficher une frame de chargement
def print_loading_frame(symbol, text, position):
    frame = [' '] * 12
    sym_len = visible_length(symbol)
    for i in range(sym_len):
        frame[(position + i) % len(frame)] = symbol
    print(f"[{''.join(frame)}]  {text}", end='\r')

class Print:
    @staticmethod
    def status(align, status, text):
        # Assurez-vous que la longueur du statut est au moins de 12 caractères
        min_length = 12
        status_length = visible_length(status)
        if status_length < min_length:
            padding = (min_length - status_length) // 2
            status = ' ' * padding + status + ' ' * (min_length - status_length - padding)

        # Centre le statut s'il est demandé
        if align == 'c':
            status = center_with_ansi(status, min_length)
        
        # Diviser le texte en plusieurs lignes
        lines = text.split('\n')
        formatted_lines = []
        
        for i, line in enumerate(lines):
            if i == 0:
                formatted_lines.append(f"[{status}]  {line}")
            else:
                formatted_lines.append(f"{' ' * (min_length + 2)}  {line}")
        
        # Affiche le texte avec le formatage spécial
        print('\n'.join(formatted_lines))

    class Loading:
        @staticmethod
        def bar(symbol, text, function, *arg, end_symbol="OK"):
            stop_loading = threading.Event()

            def animate():
                position = 0
                while not stop_loading.is_set():
                    print_loading_frame(symbol, text, position)
                    position = (position + 1) % 12
                    time.sleep(0.2)

            animation_thread = threading.Thread(target=animate)
            animation_thread.start()

            try:
                function(*arg)
            finally:
                stop_loading.set()
                animation_thread.join()
                end_frame = center_with_ansi(end_symbol, 12)  # Ensure the end frame is centered within 12 characters
                print(f"[{end_frame}]  {text}")

        
        def spinner(message, func, *arg):
            # Les symboles pour la roue de chargement
            spinner_symbols = ['|', '/', '-', '\\']
            stop_spinner = threading.Event()

            def animate():
                index = 0
                while not stop_spinner.is_set():
                    sys.stdout.write(f'\r{message} {spinner_symbols[index]}')
                    sys.stdout.flush()
                    index = (index + 1) % len(spinner_symbols)
                    time.sleep(0.1)

            animation_thread = threading.Thread(target=animate)
            animation_thread.start()

            try:
                func(*arg)
            finally:
                stop_spinner.set()
                animation_thread.join()
                # Afficher "Fait" à la fin de l'exécution
                sys.stdout.write(f'\r{message} Fait\n')
                sys.stdout.flush()

class Execute:
    def list(symbol, list, end_symbol="OK"):
        Print.status("c", "info", "start operation...")
        for func in list:
            text = f"function {func.__name__}"
            Print.Loading.bar(symbol, text, func, end_symbol)
        Print.status("c", "info", "operation is finish !")

    def dico(symbol, dico, end_symbol="OK"):
        # Affiche le début de l'opération
        Print.status("c", "info", "start operation...")
        
        for func, text in dico.items():
            # Affiche le texte associé à chaque fonction avec le chargement
            Print.Loading.bar(symbol, text, func, end_symbol)
        
        # Affiche la fin de l'opération
        Print.status("c", "info", "operation is finish !")

class progress:
    def screensize():
        """Returns the appropriate bar length considering the terminal width and space for percentage and elapsed time."""
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        reserved_space = len(" [] 100.0% 00:00:00")
        bar_length = terminal_width - reserved_space
        return max(10, bar_length)  # Ensure bar length is at least 10

    def progress_bar(steps, func, args=(), bar_length=None, symbol_filled='/', symbol_empty='-', color_filled='\033[92m', color_empty='\033[91m', reset_color='\033[0m'):
        """
        Displays a progress bar in the CLI during the execution of the provided function.
        
        Parameters:
            steps (int): Total number of steps the function takes to complete.
            func (callable): The function to execute. This function must accept a single callback argument.
            args (tuple): Additional arguments to pass to the function.
            bar_length (int or None): Length of the progress bar. If None, the bar length is adjusted to fit the terminal width.
            symbol_filled (str): Symbol for the filled part of the progress bar.
            symbol_empty (str): Symbol for the empty part of the progress bar.
            color_filled (str): ANSI color code for the filled part of the progress bar.
            color_empty (str): ANSI color code for the empty part of the progress bar.
            reset_color (str): ANSI color code to reset the color.
        """
        start_time = time.time()

        # Use provided bar_length or calculate dynamic length if bar_length is None
        if bar_length is None:
            terminal_width = shutil.get_terminal_size((80, 20)).columns
            reserved_space = len(" [] 100.0% 00:00:00")
            bar_length = terminal_width - reserved_space
            bar_length = max(10, bar_length)  # Ensure bar length is at least 10

        def update_progress(current_step):
            """Callback function to update the progress bar."""
            elapsed_time = time.time() - start_time
            percent = current_step / steps
            filled_length = int(bar_length * percent)
            bar = (color_filled + symbol_filled * filled_length + reset_color +
                color_empty + symbol_empty * (bar_length - filled_length) + reset_color)
            time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            print(f'\r[{bar}] {percent:.1%} {time_str}', end='', flush=True)

        def wrapper(callback):
            func(callback, *args)

        # Run the function in a separate thread to keep the progress bar updating
        thread = threading.Thread(target=wrapper, args=(update_progress,))
        thread.start()
        thread.join()
        print()  # Move to the next line after the progress bar completes


def timer():
    return f"[{datetime.datetime.now().strftime('%H:%M:%S')}.{datetime.datetime.now().microsecond // 1000:03d}]  "