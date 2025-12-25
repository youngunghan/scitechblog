import matplotlib.pyplot as plt
import matplotlib.patches as patches

def create_latex_thumbnail(output_path):
    # Setup figure
    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
    fig.patch.set_facecolor('#1e1e1e')
    ax.set_facecolor('#1e1e1e')
    
    # Remove axes
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 60)
    ax.axis('off')
    
    # Draw browser window-like container
    window = patches.FancyBboxPatch((5, 5), 90, 50,
                                   boxstyle="round,pad=0,rounding_size=1",
                                   facecolor='#252526',
                                   edgecolor='#333333',
                                   linewidth=1)
    ax.add_patch(window)
    
    # Window controls
    ax.add_patch(patches.Circle((10, 52), 0.8, color='#ff5f56'))
    ax.add_patch(patches.Circle((13, 52), 0.8, color='#ffbd2e'))
    ax.add_patch(patches.Circle((16, 52), 0.8, color='#27c93f'))
    
    # Content
    font_family = 'monospace'
    
    # Title
    ax.text(50, 45, "Math Rendering Issue", 
            color='#ffffff', fontsize=16, fontfamily=font_family, 
            ha='center', weight='bold')
            
    # "Before" section (Raw Text)
    ax.text(15, 35, "Before (Raw Text):", color='#ff5f56', fontsize=12, fontfamily=font_family)
    ax.text(20, 30, r"$O(N \log N)$", color='#cccccc', fontsize=14, fontfamily=font_family)
    ax.text(20, 25, r"$\sum_{i=1}^{n} i$", color='#cccccc', fontsize=14, fontfamily=font_family)
    
    # Arrow
    ax.arrow(50, 28, 10, 0, head_width=2, head_length=2, fc='#569cd6', ec='#569cd6')
    
    # "After" section (Rendered)
    ax.text(65, 35, "After (MathJax):", color='#4af626', fontsize=12, fontfamily=font_family)
    
    # We can't easily render real LaTeX here without external deps, 
    # so we'll simulate it with text that looks "math-like"
    ax.text(70, 30, "O(N log N)", color='#ffffff', fontsize=14, fontfamily='serif', style='italic')
    ax.text(70, 25, "∑ i", color='#ffffff', fontsize=14, fontfamily='serif')

    # Config snippet
    box = patches.Rectangle((15, 8), 70, 12, facecolor='#1e1e1e', edgecolor='#333333')
    ax.add_patch(box)
    ax.text(17, 16, "---", color='#569cd6', fontsize=10, fontfamily=font_family)
    ax.text(17, 13, "math: true", color='#4af626', fontsize=10, fontfamily=font_family, weight='bold')
    ax.text(17, 10, "---", color='#569cd6', fontsize=10, fontfamily=font_family)

    # Save
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0.1, facecolor='#1e1e1e')
    plt.close()

if __name__ == "__main__":
    import os
    os.makedirs("assets/img/posts/troubleshooting", exist_ok=True)
    create_latex_thumbnail("assets/img/posts/troubleshooting/latex_thumbnail.png")
    print("Thumbnail generated successfully.")
