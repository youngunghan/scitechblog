import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.font_manager import FontProperties

def create_terminal_thumbnail(output_path):
    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    
    # Remove axes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')
    
    # Draw terminal window
    window = patches.FancyBboxPatch((5, 5), 90, 50,
                                   boxstyle="round,pad=0,rounding_size=1",
                                   facecolor='#000000',
                                   edgecolor='#333333',
                                   linewidth=1)
    ax.add_patch(window)
    
    # Window controls (Mac style)
    ax.add_patch(patches.Circle((10, 52), 0.8, color='#ff5f56')) # Red
    ax.add_patch(patches.Circle((13, 52), 0.8, color='#ffbd2e')) # Yellow
    ax.add_patch(patches.Circle((16, 52), 0.8, color='#27c93f')) # Green
    
    # Terminal Text
    font_size = 10
    line_height = 3
    start_y = 45
    x_margin = 8
    
    text_content = [
        (r"root@scitechblog:~$ bundle exec htmlproofer _site", '#4af626'),
        (r"Running 3 checks (Images, Links, Scripts) in ['_site']...", '#d4d4d4'),
        (r"Checking 323 internal links", '#d4d4d4'),
        (r"Ran on 141 files!", '#d4d4d4'),
        (r"", '#d4d4d4'),
        (r"For the Images check, the following failures were found:", '#ff5f56'),
        (r"* At _site/scitechblog/index.html:1053:", '#d4d4d4'),
        (r"  internal image /scitechblog/scitechblog/assets/img/...", '#ff5f56'),
        (r"  does not exist", '#ff5f56'),
        (r"", '#d4d4d4'),
        (r"HTML-Proofer found 1 failure!", '#ff5f56'),
        (r"root@scitechblog:~$ _", '#4af626'),
    ]
    
    for i, (text, color) in enumerate(text_content):
        ax.text(x_margin, start_y - (i * line_height), text,
                color=color, fontsize=font_size, fontfamily='monospace',
                ha='left', va='top')

    # Save
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, facecolor='#1e1e1e')
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("assets/img/posts/troubleshooting", exist_ok=True)
    create_terminal_thumbnail("assets/img/posts/troubleshooting/thumbnail.png")
    print("Thumbnail generated successfully.")
