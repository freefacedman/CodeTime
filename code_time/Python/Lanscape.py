"""
Enhanced Visual-Only Python Landscape Generator

This script generates an interactive and animated landscape using Matplotlib and NumPy.
It includes dynamic seasons, time-of-day transitions, weather variations, animated elements,
and interactive GUI controls—all created entirely with geometric shapes in code.
No external audio or image files are required, and images are not saved as PNGs.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Polygon
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Button, RadioButtons
from matplotlib.animation import FuncAnimation

# Configuration dictionary for easy customization
config = {
    "canvas_size": (-200, 200, -100, 100),
    "element_counts": {
        "trees": 15,
        "flowers": 20,
        "clouds": 5,
        "bushes": 10,
        "rocks": 5,
        "stars": 50,
        "raindrops": 100,
        "snowflakes": 100
    },
    "colors": {
        "ground": "#8B5A2B",
        "trunk": "#4E2F0B",
        "leaves": "#228B22",
        "flower1": "#FF69B4",
        "flower2": "#FFD700",
        "cloud": "#FFFFFF",
        "river": "#ADD8E6",
        "mountain": "#808080",
        "grass": "#32CD32",
        "bush": "#006400",
        "rock": "#A9A9A9",
        "star": "#FFFFE0",
        "raindrop": "blue",
        "snowflake": "#FFFFFF",
        "sun": "#FFD700",
        "moon": "#F0E68C"
    },
    "season": "spring",           # Options: spring, summer, autumn, winter
    "time_of_day": "day",         # Options: day, sunset, night
    "weather": "clear",           # Options: clear, rainy, snowy
}

def adjust_colors_for_season(config):
    """Adjust color scheme based on the selected season."""
    season = config["season"]
    if season == "spring":
        config["colors"]["leaves"] = "#32CD32"
        config["colors"]["flower1"] = "#FF69B4"
        config["colors"]["flower2"] = "#FFB6C1"
    elif season == "summer":
        config["colors"]["leaves"] = "#228B22"
        config["colors"]["flower1"] = "#FFA500"
        config["colors"]["flower2"] = "#FFD700"
    elif season == "autumn":
        config["colors"]["leaves"] = "#FF8C00"
        config["colors"]["flower1"] = "#FF4500"
        config["colors"]["flower2"] = "#DAA520"
    elif season == "winter":
        config["colors"]["ground"] = "#F0F8FF"
        config["colors"]["leaves"] = "#D3D3D3"
        config["colors"]["flower1"] = "#FFFFFF"
        config["colors"]["flower2"] = "#F5F5F5"
        config["colors"]["river"] = "#B0E0E6"

def is_overlap(existing_positions, x, y, threshold=30):
    """Check if a new element overlaps with existing ones."""
    for ex, ey in existing_positions:
        distance = np.sqrt((ex - x) ** 2 + (ey - y) ** 2)
        if distance < threshold:
            return True
    return False

def draw_tree(ax, x, y, config):
    """Draw a tree at the specified position."""
    trunk_color = config["colors"]["trunk"]
    leaves_color = config["colors"]["leaves"]
    trunk = Rectangle((x - 5, y), 10, 40, color=trunk_color, zorder=5)
    leaf = Ellipse((x, y + 40), 30, 30, color=leaves_color, zorder=6)
    ax.add_patch(trunk)
    ax.add_patch(leaf)

def draw_cloud(ax, x, y, size, config):
    """Draw a cloud at the specified position."""
    cloud_color = config["colors"]["cloud"]
    alpha = 0.8
    cloud = Ellipse((x, y), size, size / 2, color=cloud_color, alpha=alpha, zorder=7)
    cloud2 = Ellipse((x + size * 0.3, y + size * 0.1), size * 0.6, size / 3, color=cloud_color, alpha=alpha, zorder=7)
    cloud3 = Ellipse((x - size * 0.3, y + size * 0.1), size * 0.6, size / 3, color=cloud_color, alpha=alpha, zorder=7)
    ax.add_patch(cloud)
    ax.add_patch(cloud2)
    ax.add_patch(cloud3)

def draw_flower(ax, x, y, config, size=8):
    """Draw a flower at the specified position."""
    flower_colors = [config["colors"]["flower1"], config["colors"]["flower2"]]
    stem = Rectangle((x - 1, y), 2, 20, color="green", zorder=4)
    petals = Ellipse((x, y + 20), size, size / 2, color=random.choice(flower_colors), zorder=5)
    ax.add_patch(stem)
    ax.add_patch(petals)

def draw_star(ax, x, y, config, size=2):
    """Draw a star at the specified position."""
    star_color = config["colors"]["star"]
    star = Ellipse((x, y), size, size, color=star_color, alpha=0.8, zorder=10)
    ax.add_patch(star)

def draw_sun_or_moon(ax, config):
    """Draw the sun or moon based on the time of day."""
    if config["time_of_day"] == "day":
        sun = Ellipse((150, 80), 20, 20, color=config["colors"]["sun"], alpha=0.9, zorder=8)
        ax.add_patch(sun)
    elif config["time_of_day"] == "night":
        moon = Ellipse((150, 80), 15, 15, color=config["colors"]["moon"], alpha=0.8, zorder=8)
        ax.add_patch(moon)

def add_gradient_background(ax, config):
    """Add a gradient background based on the time of day."""
    time = config["time_of_day"]
    if time == "day":
        top_color = "#87CEEB"
        bottom_color = config["colors"]["ground"]
    elif time == "sunset":
        top_color = "#FF7E67"
        bottom_color = "#FFDAB9"
    elif time == "night":
        top_color = "#191970"
        bottom_color = "#2F4F4F"
    else:
        top_color = "#87CEEB"
        bottom_color = config["colors"]["ground"]
    gradient = np.linspace(0, 1, 256).reshape(1, -1)
    gradient = np.vstack((gradient, gradient))
    cmap = LinearSegmentedColormap.from_list("gradient", [top_color, bottom_color])
    ax.imshow(gradient, aspect='auto', cmap=cmap, interpolation='bicubic', extent=config["canvas_size"], zorder=0)

def generate_mountain_shape(start_x, start_y, width, height, config):
    """Generate a random mountain shape."""
    points = []
    num_points = 100
    for i in range(num_points + 1):
        x = start_x + (width / num_points) * i
        y_variation = random.uniform(-height, height)
        y = start_y + y_variation
        points.append((x, y))
    points.append((start_x + width, start_y))
    points.append((start_x, start_y))
    return points

def draw_mountains(ax, config):
    """Draw mountains in the background."""
    mountain1 = Polygon(generate_mountain_shape(-200, -100, 100, 50, config),
                       color=config["colors"]["mountain"], alpha=0.7, zorder=3)
    ax.add_patch(mountain1)
    mountain2 = Polygon(generate_mountain_shape(100, -100, 100, 50, config),
                       color=config["colors"]["mountain"], alpha=0.7, zorder=3)
    ax.add_patch(mountain2)

def draw_river(ax, config):
    """Draw a river flowing through the landscape."""
    river = Polygon([(-200, -100), (-150, -90), (-100, -100), (100, -100), (150, -90), (200, -100)],
                    color=config["colors"]["river"], alpha=0.6, zorder=2)
    ax.add_patch(river)

def draw_bush(ax, x, y, config, size=20):
    """Draw a bush at the specified position."""
    bush_color = config["colors"]["bush"]
    bush = Ellipse((x, y), size, size / 2, color=bush_color, alpha=0.7, zorder=4)
    ax.add_patch(bush)

def draw_rock(ax, x, y, config, size=10):
    """Draw a rock at the specified position."""
    rock_color = config["colors"]["rock"]
    rock = Ellipse((x, y), size, size / 2, color=rock_color, alpha=0.9, zorder=5)
    ax.add_patch(rock)

def draw_snowflake(ax, x, y, config, size=2):
    """Draw a snowflake at the specified position."""
    snow_color = config["colors"]["snowflake"]
    snowflake = Ellipse((x, y), size, size, color=snow_color, alpha=0.8, zorder=9)
    ax.add_patch(snowflake)

def add_legend(ax, config):
    """Add a legend to the plot."""
    legend_elements = [
        Rectangle((0,0),1,1, color=config["colors"]["ground"], label="Ground"),
        Rectangle((0,0),1,1, color=config["colors"]["trunk"], label="Tree Trunk"),
        Ellipse((0,0),1,1, color=config["colors"]["leaves"], label="Leaves"),
        Ellipse((0,0),1,1, color=config["colors"]["cloud"], label="Clouds"),
        Ellipse((0,0),1,1, color=config["colors"]["river"], label="River"),
        Polygon([[0,0]], color=config["colors"]["mountain"], label="Mountain"),
        Ellipse((0,0),1,1, color=config["colors"]["bush"], label="Bushes"),
        Ellipse((0,0),1,1, color=config["colors"]["rock"], label="Rocks"),
        Ellipse((0,0),1,1, color=config["colors"]["flower1"], label="Flowers"),
        Ellipse((0,0),1,1, color=config["colors"]["star"], label="Stars"),
        Rectangle((0,0),1,1, color=config["colors"]["raindrop"], label="Raindrops"),
        Ellipse((0,0),1,1, color=config["colors"]["snowflake"], label="Snowflakes"),
        Ellipse((0,0),1,1, color=config["colors"]["sun"], label="Sun"),
        Ellipse((0,0),1,1, color=config["colors"]["moon"], label="Moon"),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize='small')

def describe_scene(config):
    """Print a description of the current scene."""
    season = config["season"].capitalize()
    time = config["time_of_day"].capitalize()
    weather = config["weather"].capitalize()
    description = f"A {season} landscape during {time.lower()} with {weather.lower()} conditions. "
    description += f"The ground is {config['colors']['ground']}, adorned with vibrant flowers and lush trees. "
    description += f"Majestic mountains rise in the background, while clouds drift across the sky. "
    if config["weather"] == "rainy":
        description += "A serene river flows gracefully through the scene, complemented by scattered bushes and rocks, with raindrops falling steadily."
    elif config["weather"] == "snowy":
        description += "A serene river flows gracefully through the scene, complemented by scattered bushes and rocks, with snowflakes gently falling."
    else:
        description += "A serene river flows gracefully through the scene, complemented by scattered bushes and rocks."
    print(description)

def animate_clouds(frame, clouds, config):
    """Animate clouds moving horizontally."""
    for cloud in clouds:
        new_x = cloud.center[0] + 0.5
        if new_x > config["canvas_size"][1] + 50:
            new_x = config["canvas_size"][0] - 50
        cloud.center = (new_x, cloud.center[1])
    return clouds

def animate_raindrops(frame, raindrops, config):
    """Animate raindrops falling vertically."""
    for drop in raindrops:
        new_y = drop.get_y() - 5
        if new_y < config["canvas_size"][2]:
            new_y = config["canvas_size"][3]
        drop.set_y(new_y)
    return raindrops

def animate_snowflakes(frame, snowflakes, config):
    """Animate snowflakes falling vertically."""
    for snow in snowflakes:
        new_y = snow.get_y() - 2
        if new_y < config["canvas_size"][2]:
            new_y = config["canvas_size"][3]
        snow.set_y(new_y)
    return snowflakes

# Store animation objects to prevent garbage collection
animations = []

def create_landscape(event=None):
    """Main function to create and display the landscape."""
    plt.close('all')  # Close previous plots
    adjust_colors_for_season(config)  # Adjust colors based on season
    fig, ax = plt.subplots(figsize=(10, 6))
    add_gradient_background(ax, config)  # Add gradient sky

    # Draw sun or moon
    draw_sun_or_moon(ax, config)

    # Draw mountains and river
    draw_mountains(ax, config)
    draw_river(ax, config)

    # Add static elements
    element_positions = []
    for _ in range(config["element_counts"]["trees"]):
        x, y = random.randint(-200, 200), random.randint(-100, 0)
        if not is_overlap(element_positions, x, y):
            draw_tree(ax, x, y, config)
            element_positions.append((x, y))
    for _ in range(config["element_counts"]["bushes"]):
        x, y = random.randint(-200, 200), random.randint(-100, -50)
        if not is_overlap(element_positions, x, y):
            draw_bush(ax, x, y, config, size=random.randint(15, 25))
            element_positions.append((x, y))
    for _ in range(config["element_counts"]["rocks"]):
        x, y = random.randint(-200, 200), random.randint(-100, -50)
        if not is_overlap(element_positions, x, y):
            draw_rock(ax, x, y, config, size=random.randint(8, 15))
            element_positions.append((x, y))
    for _ in range(config["element_counts"]["flowers"]):
        x, y = random.randint(-200, 200), random.randint(-100, 0)
        if not is_overlap(element_positions, x, y):
            draw_flower(ax, x, y, config, size=random.randint(6, 10))
            element_positions.append((x, y))

    # Add animated clouds
    clouds = []
    for _ in range(config["element_counts"]["clouds"]):
        x, y = random.randint(-200, 200), random.randint(50, 100)
        size = random.randint(30, 50)
        if not is_overlap([(c.center[0], c.center[1]) for c in clouds], x, y, threshold=60):
            cloud = Ellipse((x, y), size, size / 2, color=config["colors"]["cloud"], alpha=0.8, zorder=7)
            ax.add_patch(cloud)
            clouds.append(cloud)

    # Add animated raindrops or snowflakes based on weather
    raindrops = []
    snowflakes = []
    if config["weather"] == "rainy":
        for _ in range(config["element_counts"]["raindrops"]):
            drop_x = random.randint(config["canvas_size"][0], config["canvas_size"][1])
            drop_y = random.randint(config["canvas_size"][2], config["canvas_size"][3])
            drop = Rectangle((drop_x, drop_y), 1, 5, color=config["colors"]["raindrop"], zorder=9)
            ax.add_patch(drop)
            raindrops.append(drop)
    elif config["weather"] == "snowy":
        for _ in range(config["element_counts"]["snowflakes"]):
            snow_x = random.randint(config["canvas_size"][0], config["canvas_size"][1])
            snow_y = random.randint(config["canvas_size"][2], config["canvas_size"][3])
            snow = Ellipse((snow_x, snow_y), 2, 2, color=config["colors"]["snowflake"], alpha=0.8, zorder=9)
            ax.add_patch(snow)
            snowflakes.append(snow)

    # Add stars if it's night
    if config["time_of_day"] == "night":
        for _ in range(config["element_counts"]["stars"]):
            star_x = random.randint(config["canvas_size"][0], config["canvas_size"][1])
            star_y = random.randint(0, config["canvas_size"][3])
            star_size = random.uniform(0.5, 2)
            draw_star(ax, star_x, star_y, config, size=star_size)

    # Set plot limits and remove axes
    ax.set_xlim(config["canvas_size"][0], config["canvas_size"][1])
    ax.set_ylim(config["canvas_size"][2], config["canvas_size"][3])
    ax.set_xticks([])
    ax.set_yticks([])

    # Add legend
    add_legend(ax, config)

    # Display scene description
    describe_scene(config)

    # Animate clouds
    anim_clouds = FuncAnimation(fig, animate_clouds, fargs=(clouds, config), frames=200, interval=50, blit=False)
    animations.append(anim_clouds)  # Keep reference

    # Animate raindrops or snowflakes based on weather
    if config["weather"] == "rainy":
        anim_raindrops = FuncAnimation(fig, animate_raindrops, fargs=(raindrops, config), frames=200, interval=50, blit=False)
        animations.append(anim_raindrops)  # Keep reference
    elif config["weather"] == "snowy":
        anim_snowflakes = FuncAnimation(fig, animate_snowflakes, fargs=(snowflakes, config), frames=200, interval=50, blit=False)
        animations.append(anim_snowflakes)  # Keep reference

    # Add interactive button to regenerate the landscape
    ax_button = plt.axes([0.81, 0.01, 0.1, 0.05])
    btn = Button(ax_button, 'Regenerate')
    btn.on_clicked(create_landscape)

    # Add interactive radio buttons for season, time of day, and weather
    add_interactive_controls(fig, ax)

    plt.show()

def add_interactive_controls(fig, ax_main):
    """Add radio buttons for interactive configuration."""
    # Define axes for radio buttons
    ax_season = plt.axes([0.02, 0.8, 0.15, 0.15], facecolor='lightgoldenrodyellow')
    ax_time = plt.axes([0.02, 0.6, 0.15, 0.15], facecolor='lightgoldenrodyellow')
    ax_weather = plt.axes([0.02, 0.4, 0.15, 0.15], facecolor='lightgoldenrodyellow')

    # Create radio buttons for season
    seasons = ('spring', 'summer', 'autumn', 'winter')
    rbtn_season = RadioButtons(ax_season, seasons, active=seasons.index(config["season"]))
    for label in rbtn_season.labels:
        label.set_fontsize(8)
    ax_season.set_title('Season', fontsize=10)

    # Create radio buttons for time of day
    times = ('day', 'sunset', 'night')
    rbtn_time = RadioButtons(ax_time, times, active=times.index(config["time_of_day"]))
    for label in rbtn_time.labels:
        label.set_fontsize(8)
    ax_time.set_title('Time of Day', fontsize=10)

    # Create radio buttons for weather
    weathers = ('clear', 'rainy', 'snowy')
    rbtn_weather = RadioButtons(ax_weather, weathers, active=weathers.index(config["weather"]))
    for label in rbtn_weather.labels:
        label.set_fontsize(8)
    ax_weather.set_title('Weather', fontsize=10)

    # Define callback functions to update config and regenerate landscape
    def update_season(label):
        config["season"] = label
        create_landscape()

    def update_time(label):
        config["time_of_day"] = label
        create_landscape()

    def update_weather(label):
        config["weather"] = label
        create_landscape()

    # Connect callbacks to radio buttons
    rbtn_season.on_clicked(update_season)
    rbtn_time.on_clicked(update_time)
    rbtn_weather.on_clicked(update_weather)

def main():
    """Entry point of the script."""
    create_landscape()

if __name__ == "__main__":
    main()
