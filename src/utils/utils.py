

def generate_colors(num_colors):
    # Define a list of color codes (you can customize this list)
    color_list = ['#F7941D', '#426386', '#FACA6E', '#ff5733', '#995577', '#2299aa', '#ffcc22', '#1199dd']
    
    # Repeat the color list to cover all bars
    colors = [color_list[i % len(color_list)] for i in range(num_colors)]
    
    return colors