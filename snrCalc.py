import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load grayscale image
image = cv2.imread('your_image.jpg', cv2.IMREAD_GRAYSCALE)

# Normalize image
norm_img = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)

# Threshold to find bright objects
_, thresh = cv2.threshold(norm_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find contours (objects)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assume the largest bright region is the object
contours = sorted(contours, key=cv2.contourArea, reverse=True)
object_mask = np.zeros_like(norm_img)
cv2.drawContours(object_mask, [contours[0]], -1, 255, -1)

# Extract object region
object_pixels = norm_img[object_mask == 255]
signal_mean = np.mean(object_pixels)

# Background mask = invert of object mask
background_mask = cv2.bitwise_not(object_mask)

# Use KMeans to isolate darker areas in background for better noise estimate
bg_pixels = norm_img[background_mask == 255].reshape(-1, 1)
kmeans = KMeans(n_clusters=2, random_state=0).fit(bg_pixels)
dark_cluster = np.argmin(kmeans.cluster_centers_)
dark_pixels = bg_pixels[kmeans.labels_ == dark_cluster]
noise_std = np.std(dark_pixels)

# Compute SNR
snr = (signal_mean - np.mean(dark_pixels)) / noise_std
print(f"Estimated SNR: {snr:.2f}")

# Optional: Show object and background masks
plt.subplot(1, 3, 1)
plt.title('Original')
plt.imshow(norm_img, cmap='gray')

plt.subplot(1, 3, 2)
plt.title('Object Mask')
plt.imshow(object_mask, cmap='gray')

plt.subplot(1, 3, 3)
plt.title('Background Mask')
plt.imshow(background_mask, cmap='gray')
plt.tight_layout()
plt.show()
