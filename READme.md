# Nim Game - Minimax AI

## Descripcion

Implementacion del juego de Nim con multiples pilas y un agente inteligente basado en el algoritmo Minimax. El juego incluye una interfaz grafica moderna con visualizacion 3D de los palitos.

---

## Reglas del Juego

| Parametro             | Valor                           |
| --------------------- | ------------------------------- |
| Pilas iniciales       | Fila 1: 3, Fila 2: 5, Fila 3: 7 |
| Movimientos por turno | 1, 2 o 3 palitos de una fila    |
| Condicion de victoria | Tomar el ultimo palito          |

### Como Jugar

1. Selecciona una fila haciendo clic en "Seleccionar"
2. Elige cuantos palitos remover (1, 2 o 3)
3. El jugador que toma el ultimo palito **gana**

---

## Estrategia Matematica

La estrategia optima se basa en el **Nim-sum** (operacion XOR):

```
Nim-sum = Fila1 XOR Fila2 XOR Fila3
```

- Si Nim-sum = 0: Posicion perdedora
- Si Nim-sum != 0: Posicion ganadora

### Estado Inicial (3, 5, 7)

```
  3 = 011
  5 = 101
  7 = 111
  ---------
XOR = 001 = 1  (Posicion ganadora para quien mueve primero)
```

---

## Niveles de Dificultad

| Nivel   | Probabilidad Optimo | Comportamiento       |
| ------- | ------------------- | -------------------- |
| Facil   | 20%                 | Mayormente aleatorio |
| Medio   | 50%                 | Balance              |
| Dificil | 80%                 | Casi siempre optimo  |
| Optimo  | 100%                | Siempre usa Nim-sum  |

---

## Instalacion

```bash
cd nim_minimax_project

# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias

```
PyQt6>=6.4.0
numpy>=1.24.0
matplotlib>=3.7.0
```

---

## Uso

### Ejecutar el Juego

```bash
cd src
python main.py
```

## Estructura del Proyecto

```
nim_minimax_project/
|
+-- src/
|   +-- nim.py          # Logica del juego multi-pila
|   +-- minimax.py      # Algoritmo Minimax con Alpha-Beta
|   +-- game_agent.py   # Agente inteligente
|   +-- graphics.py     # Interfaz PyQt6 con visualizacion 3D
|   +-- main.py         # Punto de entrada
|
+-- docs/
|   +-- documentation.tex   # Documentacion LaTeX
|
+-- requirements.txt
+-- README.md
```

---

## Documentacion

La documentacion completa en LaTeX (`docs/documentation.tex`) incluye:

1. Teoria matematica del Nim multi-pila
2. Demostracion del teorema de Nim-sum
3. Algoritmo Minimax con poda Alpha-Beta
4. Analisis de resultados

### Compilar Documentacion

```bash
cd docs
pdflatex documentation.tex
pdflatex documentation.tex  # Segunda pasada
```

---

## Referencias

1. Bouton, C. L. (1901). *Nim, A Game with a Complete Mathematical Theory*
2. Russell, S., & Norvig, P. (2010). *Artificial Intelligence: A Modern Approach*

---

## Licencia

Proyecto de uso academico.
