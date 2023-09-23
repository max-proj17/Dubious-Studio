import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='Dubious Studio', width=800, height=800)

with dpg.window(label="Example Window"):
    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
    
    # Create a drawing canvas
    with dpg.drawlist(width=500, height=500) as drawlist:
        # Example: Draw a red line on the canvas
        dpg.draw_rectangle((0, 0), (500, 500), color=(255, 255, 255, 255), fill=(255, 255, 255, 255))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
