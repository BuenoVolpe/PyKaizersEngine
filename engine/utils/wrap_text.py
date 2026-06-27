def wrap_text(text, font, max_width):
    #--------------------------------#
    words = text.split(" ")
    lines = []
    current = ""
    #--------------------------------#
    for word in words:
        #--------------------------------#
        test_line = current + (" " if current else "") + word
        width = font.render(test_line, False, (0,0,0)).get_width()
        #--------------------------------#
        if width <= max_width:
            current = test_line
        #--------------------------------#
        else:
            #--------------------------------#
            if current:
                lines.append(current)
            #--------------------------------#
            current = word
    #--------------------------------#
    if current:
        lines.append(current)
    #--------------------------------#
    return lines
