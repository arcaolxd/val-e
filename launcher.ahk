#NoEnv
SetWorkingDir %A_ScriptDir%
#SingleInstance Force

; Nota: Si ves caracteres extraños, guarda este archivo con codificación 'UTF-8 with BOM'

; --- Estética del Lanzador ---
Gui, Color, FFFFFF
Gui, Font, s14 Bold, Segoe UI
Gui, Add, Text, x20 y20 w360 h35 Center cCC0000, Val-e: Espacio Colectivo

Gui, Font, s10 Normal, Segoe UI
Gui, Add, Text, x20 y65 w360 h45 Center, Una herramienta para escuchar, cuidar y organizar desde lo colectivo.

; --- Botones ---
Gui, Font, s11 Bold, Segoe UI
Gui, Add, Button, x50 y120 w300 h50 gStartPublic, Entrar al espacio publico
Gui, Add, Button, x50 y185 w300 h50 gStartAdmin, Gestionar el cuidado colectivo

Gui, Font, s10 Normal, Segoe UI
Gui, Add, Button, x150 y255 w100 h35 gExitApp, Salir

Gui, Show, w400 h320, Val-e Launcher
return

; --- Acciones ---

StartPublic:
Run, cmd /c "python -m streamlit run app.py", , Hide
MsgBox, 64, Val-e, Accediendo al espacio colectivo...
return

StartAdmin:
Run, cmd /c "python -m streamlit run app.py -- --mode admin", , Hide
MsgBox, 48, Val-e, Iniciando gestion de cuidado colectivo (Monitor Humano).
return

ExitApp:
GuiClose:
ExitApp
