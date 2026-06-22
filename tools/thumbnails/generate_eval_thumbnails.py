"""Light box-diagram cover thumbnails for the evaluation-rigor posts
(FID reproducibility checklist + the cross-project 'numbers eat pipelines' capstone).

License-clean: pure schematics, no dataset-derived images.
Run from the repo root: python tools/thumbnails/generate_eval_thumbnails.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# pastel palette (matches the architecture diagram aesthetic)
Y = ("#fdf2c0", "#cdb24a"); B = ("#d6e8fb", "#5a9bd4"); G = ("#d7f0d7", "#5aa85a")
O = ("#fde0c8", "#e0913a"); R = ("#fbd6d6", "#d45a5a"); P = ("#e8d6fb", "#9b5ad4"); GR = ("#ececec", "#999999")


def box(ax, x, y, w, h, text, color, fs=11, weight="bold"):
    fc, ec = color
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=1.6",
                                facecolor=fc, edgecolor=ec, linewidth=1.6))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight, color="#222")


def arrow(ax, x1, y1, x2, y2, style="->"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color="#555", lw=1.8))


def _canvas():
    fig, ax = plt.subplots(figsize=(10.5, 5.6), dpi=100)
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    ax.set_xlim(0, 100); ax.set_ylim(0, 56); ax.axis("off")
    return fig, ax


def fid_checklist(path):
    fig, ax = _canvas()
    ax.text(50, 52, "How to Actually Report FID", ha="center", fontsize=20, weight="bold", color="#1a1a1a")
    ax.text(50, 47, "the number only means something if every box is pinned",
            ha="center", fontsize=12, color="#666")
    # pipeline row
    box(ax, 4, 30, 18, 9, "images\n(real + fake)", B, fs=11)
    box(ax, 28, 30, 20, 9, "InceptionV3\n2048-d pool3", G, fs=11)
    box(ax, 54, 30, 18, 9, "Fréchet\ndistance", Y, fs=11)
    box(ax, 80, 30, 16, 9, "FID", O, fs=14)
    for x in (22, 48, 72):
        arrow(ax, x, 34.5, x + 6, 34.5)
    # four knobs
    knobs = [("✓ extractor", G, 6), ("✓ input pipeline", B, 30), ("✓ sampling", Y, 54), ("✓ controls", P, 78)]
    for label, color, x in knobs:
        box(ax, x, 12, 18, 7, label, color, fs=10.5)
    ax.text(50, 5, "miss one box and the number is not comparable to anything",
            ha="center", fontsize=11, style="italic", color="#444")
    plt.savefig(path, bbox_inches="tight", pad_inches=0.15, facecolor="white"); plt.close()
    print("saved", path)


def numbers_eat_pipelines(path):
    fig, ax = _canvas()
    ax.text(50, 52, "Numbers Eat Pipelines", ha="center", fontsize=22, weight="bold", color="#1a1a1a")
    ax.text(50, 47, "the same mistake in two domains", ha="center", fontsize=12, color="#666")
    # left: generative / FID
    box(ax, 8, 33, 36, 8, "text-to-image GAN", P, fs=12)
    box(ax, 8, 22, 36, 8, "FID 0.24  →  really ~165", R, fs=12)
    arrow(ax, 26, 33, 26, 30)
    # right: detection / mAP
    box(ax, 56, 33, 36, 8, "object detector", B, fs=12)
    box(ax, 56, 22, 36, 8, "0.91 mAP  →  leaked split", R, fs=12)
    arrow(ax, 74, 33, 74, 30)
    # converge to bottom lesson
    arrow(ax, 26, 22, 44, 13); arrow(ax, 74, 22, 56, 13)
    box(ax, 18, 4, 64, 8, "trust a metric only after you understand its pipeline", G, fs=12.5)
    plt.savefig(path, bbox_inches="tight", pad_inches=0.15, facecolor="white"); plt.close()
    print("saved", path)


if __name__ == "__main__":
    os.makedirs("assets/img/posts/fid-checklist", exist_ok=True)
    os.makedirs("assets/img/posts/numbers-eat-pipelines", exist_ok=True)
    fid_checklist("assets/img/posts/fid-checklist/cover.png")
    numbers_eat_pipelines("assets/img/posts/numbers-eat-pipelines/cover.png")
