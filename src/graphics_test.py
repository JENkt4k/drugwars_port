from ti_draw import *

W, H = get_screen_dim()

clear()

set_color(0, 0, 0)
draw_text(10, 15, "TI-Nspire Graphics Test")

set_color(0, 100, 255)
fill_rect(20, 40, 100, 50)

set_color(255, 0, 0)
fill_circle(200, 100, 30)

set_color(0, 0, 0)
draw_text(20, 160, str(W) + " x " + str(H))

paint_buffer()
