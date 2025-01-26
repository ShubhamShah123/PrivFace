from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import laplace
from scipy.interpolate import griddata
from sklearn.cluster import KMeans
import math

def dp_pix(input_data, epsilon, block_size, num_pixels):
	print("---- DP PIX ----")
	print(epsilon, block_size, num_pixels)
	# Initialize variables
	image = input_data.convert('RGB')
	image = np.asarray(image)
	height, width, channels = image.shape
	num_blocks = (height//block_size) * (width//block_size)
	m = num_pixels // block_size**2
	
	# Round the dimensions of the image to the nearest multiple of the block size
	height = height - height % block_size
	width = width - width % block_size
	
	# Convert the image to an array
	image = np.asarray(image)[:height, :width]
	
	# Pixelize the image
	pixelized_image = np.zeros((height//block_size, width//block_size, channels))
	for c in range(channels):
		for i in range(height//block_size):
			for j in range(width//block_size):
				pixelized_image[i,j,c] = np.mean(image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size, c])
	
	# Add Laplacian noise to the pixelized image
	noise_scale = 255 * m / (block_size**2 * epsilon)
	laplace_noise = laplace.rvs(scale=noise_scale, size=num_blocks*channels)
	laplace_noise = laplace_noise.reshape((num_blocks, channels))
	pixelized_image += laplace_noise.reshape((height//block_size, width//block_size, channels))
	
	# Map the pixelized image back to the original image size
	dp_image = np.zeros((height, width, channels))
	for c in range(channels):
		for i in range(height//block_size):
			for j in range(width//block_size):
				dp_image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size, c] = pixelized_image[i,j,c]
	
	# Resize the output image to 224x224
	dp_image = Image.fromarray(dp_image.astype(np.uint8)).resize((height, width))
	
	return np.asarray(dp_image)

def dp_snow(image, delta):
	print("--- DP SNOW ---")
	image2 = image.resize((224, 224))
	np_image = np.array(image2)
	final_image = np.zeros_like(np_image)   
	width, height = image2.size
	p = delta

	# Calculate the size of the subset S
	size_S = int(p * width * height)

	# Get the indices of the pixels in the image
	indices = np.arange(width * height)

	# Randomly select indices for the subset S
	# replace needs to False as to not select the same pixel again.
	indices_S = np.random.choice(indices, size=size_S, replace=False)
	
	
	# Len > 2 implies that image has more than 2 channels. Meaning image is RGB and adding snow in each channel separately.
	if len(np_image.shape) > 2:
		green = np_image.copy()
		red = np_image.copy()
		blue = np_image.copy()
		'''
		0 - red
		1 - green
		2 - blue
		'''
		green[:,:,0] = 0
		green[:,:,2] = 0

		red[:,:,1] = 0
		red[:,:,2] = 0

		blue[:,:,1] = 0
		blue[:,:,0] = 0

		for index in indices_S:
			x = index % width
			y = index // width
			red[x][y][0] = 127
			green[x][y][1] = 127
			blue[x][y][2] = 127
		
		red = red / 255
		blue = blue / 255
		green = green / 255

		third_array = (red + green + blue) / 3
		final_image_IMG = Image.fromarray((third_array * 255).astype(np.uint8))
		return np.asarray(final_image_IMG)

def dp_samp(im, privacy_budget, num_clusters, num_pixels, max_iterations=1000):
	print(f"DP SAMP\nDelta, k, m: {privacy_budget ,num_clusters ,num_pixels}")
	im = im.resize((224, 224))

	# Convert to grayscale for clustering
	gray_im = np.array(im.convert('L'))
	# print("image converted to grayscale")

	# 1. Pixel Clustering
	img_pixels = gray_im.reshape(-1, 1)
	kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(img_pixels)
	cluster_centers = kmeans.cluster_centers_
	cluster_labels = kmeans.labels_
	# print("image clustered")

	# 2. Budget Allocation   
	epsilon_per_cluster = np.zeros(num_clusters)
	for i in range(num_clusters):
		freq_i = np.sum(cluster_labels == i)
		epsilon_per_cluster[i] = (privacy_budget * freq_i) / len(cluster_labels)
	# print("budget allocated")

	# 3. Pixel Sampling
	sampled_pixels = []
	for i, center in enumerate(cluster_centers):
		epsilon_i = epsilon_per_cluster[i]
		count_i = np.sum(cluster_labels == i)

		x_i = num_pixels
		iteration = 0  # Add an iteration counter
		while True:
			if count_i - num_pixels > 0:
				ratio = math.comb(count_i, x_i) / (math.comb(count_i - num_pixels, x_i) + 1e-9)
			else:
				ratio = float('inf')

			prob = np.exp(epsilon_i * x_i)
			if ratio <= prob or iteration >= max_iterations:  # Break the loop if the maximum number of iterations is reached
				break
			x_i -= 1
			iteration += 1
		#set x_i to 0 if it is negative
		if x_i < 0:
			x_i = 0

		indices = np.where(cluster_labels == i)[0]
		sampled_indices = np.random.choice(indices, size=x_i, replace=False)
		sampled_pixels.extend(zip(*np.unravel_index(sampled_indices, gray_im.shape)))


	# 4. Interpolation
	im = np.array(im)  # Convert the original image to an array
	obfuscated_image = im.copy()
	for channel in range(3):
		X, Y = np.meshgrid(np.arange(0, im.shape[1], 1), np.arange(0, im.shape[0], 1))
		sampled_values = im[np.array(sampled_pixels)[:, 0], np.array(sampled_pixels)[:, 1], channel]
		interpolated_channel = griddata(np.array(sampled_pixels), sampled_values, (Y, X), method='linear', fill_value=np.nan)
		mask = np.isnan(interpolated_channel)
		obfuscated_image[:, :, channel] = np.where(mask, obfuscated_image[:, :, channel], interpolated_channel)


	return np.asarray(obfuscated_image)