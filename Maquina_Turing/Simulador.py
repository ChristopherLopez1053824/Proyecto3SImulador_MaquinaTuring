import tkinter as tk
import time

#DFA
dfa_lenguajes = {
    "1) (0+1)*01": {
        "estados": ["q0", "q1", "q2", "qf"],
        "inicio": "q0",
        "final": ["qf"],
        "transiciones": {
            ("q0", "0"): ("q0", "X"),
            ("q0", "1"): ("q1", "Y"),
            ("q1", "0"): ("q2", "X"),
            ("q1", "1"): ("q1", "Y"),
            ("q2", "1"): ("qf", "Y"),
            ("q2", "0"): ("q0", "X")
        }
    },
    "2) (0+1)*0": {
        "estados": ["q0", "qf"],
        "inicio": "q0",
        "final": ["qf"],
        "transiciones": {
            ("q0", "0"): ("qf", "X"),
            ("q0", "1"): ("q0", "Y"),
            ("qf", "0"): ("qf", "X"),
            ("qf", "1"): ("q0", "Y")
        }
    },
    "3) ((0+1)(0+1))*": {
        "estados": ["q0", "q1"],
        "inicio": "q0",
        "final": ["q0"],
        "transiciones": {
            ("q0", "0"): ("q1", "X"),
            ("q0", "1"): ("q1", "Y"),
            ("q1", "0"): ("q0", "X"),
            ("q1", "1"): ("q0", "Y")
        }
    },
    "4) (1+01)*0": {
        "estados": ["q0", "qf"],
        "inicio": "q0",
        "final": ["qf"],
        "transiciones": {
            ("q0", "1"): ("q0", "Y"),
            ("q0", "0"): ("qf", "X"),
            ("qf", "0"): ("qf", "X"),
            ("qf", "1"): ("q0", "Y")
        }
    },
    "5) (ab)+a|(ba)+b": {
        "estados": ["q0", "q_ab", "q_ba", "qf"],
        "inicio": "q0",
        "final": ["qf"],
        "transiciones": {
            ("q0", "a"): ("q_ab", "X"),
            ("q_ab", "b"): ("q_ab", "Y"),
            ("q_ab", "a"): ("qf", "X"),
            ("q0", "b"): ("q_ba", "Y"),
            ("q_ba", "a"): ("q_ba", "X"),
            ("q_ba", "b"): ("qf", "Y")
        }
    },
    "6) (aa)*(bb)*": {
        "estados": ["q0", "q1", "q2", "q3", "rej"],
        "inicio": "q0",
        "final": ["q0", "q2"],
        "transiciones": {
            ("q0", "a"): ("q1", "X"),
            ("q1", "a"): ("q0", "X"),
            ("q1", "b"): ("rej", "Y"),
            ("q3", "a"): ("rej", "X"),
            ("q2", "a"): ("rej", "X"),
            ("q0", "b"): ("q3", "Y"),
            ("q3", "b"): ("q2", "Y"),
            ("q2", "b"): ("q3", "Y")
        }
    },
    "7) a*b*": {
        "estados": ["q0", "qf"],
        "inicio": "q0",
        "final": ["q0", "qf"],
        "transiciones": {
            ("q0", "a"): ("q0", "X"),
            ("q0", "b"): ("qf", "Y"),
            ("qf", "b"): ("qf", "Y")
        }
    },
    "8) (ab)*": {
        "estados": ["q0", "q1"],
        "inicio": "q0",
        "final": ["q0"],
        "transiciones": {
            ("q0", "a"): ("q1", "X"),
            ("q1", "b"): ("q0", "Y")
        }
    },
    "9) ((a+b)(a+b)(a+b))*": {
        "estados": ["q0", "q1", "q2"],
        "inicio": "q0",
        "final": ["q0"],
        "transiciones": {
            ("q0", "a"): ("q1", "X"),
            ("q0", "b"): ("q1", "Y"),
            ("q1", "a"): ("q2", "X"),
            ("q1", "b"): ("q2", "Y"),
            ("q2", "a"): ("q0", "X"),
            ("q2", "b"): ("q0", "Y")
        }
    },
    "10) 0*10*": {
        "estados": ["q0", "qf"],
        "inicio": "q0",
        "final": ["qf"],
        "transiciones": {
            ("q0", "0"): ("q0", "X"),
            ("q0", "1"): ("qf", "Y"),
            ("qf", "0"): ("qf", "X")
        }
    }
}

#Simulacion
def simular_mt(cadena, dfa, canvas, resultado_label, estado_label):
    canvas.delete("all")
    estado_label.config(text="")
    resultado_label.config(text="")

    tape = list(cadena)
    cell_size = 50
    y = 120
    canvas_width = int(canvas.cget("width"))
    total_width = max(len(tape), 1) * cell_size
    start_x = (canvas_width - total_width) // 2

    rects = []
    texts = []
    for i, char in enumerate(tape):
        x = start_x + i * cell_size
        r = canvas.create_rectangle(x, y, x + cell_size, y + cell_size, outline="black", width=2)
        t = canvas.create_text(x + 25, y + 25, text=char, font=("Consolas", 16))
        rects.append(r)
        texts.append(t)

    head_x = start_x + 25
    head = canvas.create_polygon(head_x, y - 30, head_x - 15, y - 10, head_x + 15, y - 10, fill="red")
    canvas.update()
    time.sleep(0.5)

    estado_actual = dfa["inicio"]

    for i, simbolo in enumerate(tape):
        canvas.itemconfig(rects[i], outline="blue", width=3)
        canvas.update()
        time.sleep(0.2)

        key = (estado_actual, simbolo)
        if key in dfa["transiciones"]:
            siguiente_estado, simbolo_escrito = dfa["transiciones"][key]
        else:
            siguiente_estado = "Estado_NO_Aceptado"
            simbolo_escrito = simbolo
        if i > 0:
            canvas.move(head, cell_size, 0)
        canvas.update()
        time.sleep(0.1)
        estado_label.config(
            text=f"Transición: ({estado_actual}, {simbolo}) → ({siguiente_estado}, {simbolo_escrito}, R)"
        )
        estado_label.update()
        time.sleep(0.2)
        tape[i] = simbolo_escrito
        canvas.itemconfig(texts[i], text=simbolo_escrito)
        canvas.update()
        time.sleep(0.2)
        canvas.itemconfig(rects[i], outline="black", width=2)
        estado_actual = siguiente_estado
        if estado_actual == "rej":
            break


    time.sleep(0.5)
    if estado_actual in dfa["final"]:
        resultado_label.config(text="Cadena aceptada", fg="green")
        estado_label.config(text=f"Estado final: {estado_actual} (aceptación)")
    else:
        resultado_label.config(text="Cadena rechazada", fg="red")
        estado_label.config(text=f"Estado final: {estado_actual} (rechazo)")

#APP
root = tk.Tk()
root.title("Simulador de Máquina de Turing")

tk.Label(root, text="Seleccione un lenguaje:", font=("Arial", 12)).pack()
opcion_var = tk.StringVar(value=list(dfa_lenguajes.keys())[6])
menu = tk.OptionMenu(root, opcion_var, *dfa_lenguajes.keys())
menu.pack(pady=5)

tk.Label(root, text="Cadena a evaluar:", font=("Arial", 12)).pack()
entrada = tk.Entry(root, font=("Consolas", 14))
entrada.pack(pady=5)

canvas = tk.Canvas(root, width=900, height=250, bg="white")
canvas.pack(pady=10)

estado_label = tk.Label(root, text="", font=("Consolas", 12), fg="blue")
estado_label.pack(pady=5)

resultado_label = tk.Label(root, text="", font=("Arial", 14))
resultado_label.pack(pady=10)

tk.Button(
    root,
    text="Validar y Simular",
    font=("Arial", 12, "bold"),
    command=lambda: simular_mt(
        entrada.get(),
        dfa_lenguajes[opcion_var.get()],
        canvas,
        resultado_label,
        estado_label
    )
).pack(pady=10)

root.mainloop()
