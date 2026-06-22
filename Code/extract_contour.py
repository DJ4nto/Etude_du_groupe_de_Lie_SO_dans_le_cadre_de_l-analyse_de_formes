import cv2
import numpy as np
import torch


def rot2d(angle):
    c, s = torch.cos(angle), torch.sin(angle)
    return torch.tensor([[c, -s], [s, c]], dtype=torch.float32)


def extract_contour_torch(png_path, threshold=128, simplify_eps=0.5):
    img = cv2.imread(png_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Cannot load: {png_path}")

    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        raise RuntimeError("No contour found")

    contour = max(contours, key=len)
    contour = cv2.approxPolyDP(contour, epsilon=simplify_eps, closed=True)
    contour = contour.reshape(-1, 2).astype(np.float32)

    landmarks = torch.from_numpy(contour).float()

    N = landmarks.shape[0]
    edges = torch.stack([
        torch.arange(N),
        torch.roll(torch.arange(N), shifts=-1)
    ], dim=1).long()

    return landmarks, edges
