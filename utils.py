def print_with_color(message, color):
    def get_color_code(color):
        colors = {
            'green':'\033[92m',
            'yellow':'\033[93m',
            'red':'\033[91m'
        }

        if color in colors:
            return colors[color]
        
        return ''

    print get_color_code(color) + message + '\033[0m'
