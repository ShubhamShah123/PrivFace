import streamlit as st
from PIL import Image
import image_effects as ie
import numpy as np
from datetime import datetime
import os

AFTER_FOLDER = './afterFolder/'

def getFileName():
	current_datetime = datetime.now()
	current_datetime = datetime.now()

	# Format without leading zeros for the month and hour manually
	formatted_date = f"{current_datetime.day}-{current_datetime.month}-{current_datetime.year}-{current_datetime.strftime('%I')}-{current_datetime.strftime('%M')}"

	# Add AM/PM flag
	am_pm_flag = '1' if current_datetime.strftime('%p') == 'AM' else '0'

	# Combine the formatted date and flag
	formatted_datetime = f"{formatted_date}-{am_pm_flag}"

	return formatted_datetime

def apply_effects(image, method_name: str, args: dict) -> np.ndarray:
	if method_name == 'DP Snow':
		return ie.dp_snow(image, args['delta'])
	elif method_name == 'DP Pix':
		return ie.dp_pix(image, args['delta'], args['b'], args['m'])
	elif method_name == 'DP Samp':
		return ie.dp_samp(image, args['delta'], args['k'], args['m'])

def main():
	
	st.set_page_config(
        page_title="PrivFace",
	)
	st.title("Photo Upload and Display App")
	# Allow the user to upload a photo
	uploaded_file = st.file_uploader("Upload a photo:", type=["jpg", "jpeg", "png"])

	if uploaded_file:
		
		# Display the same photo twice side by side in a smaller size
		col1, col2 = st.columns(2)

		with col1:
			st.write("Original Photo")
			image = Image.open(uploaded_file)
			
			st.image(image, caption="Original Photo")

		# Dropdown menu below the first photo
		option_1 = st.selectbox("Choose an option for Photo 1:", ("Select the method.", "DP Snow", "DP Pix", "DP Samp"))
		st.write(f"You selected: {option_1}")
		file_name = uploaded_file.name
		file_extension = file_name.split('.')[-1]
		option = option_1.replace(' ', '-').lower()
		name = getFileName()
		afterFileName = f"{name}-after-{option}.{file_extension}"
		flag = 0
		slider_values = {}

		if option_1 == "DP Snow":
			flag = 1
			delta = st.slider("Privacy Budget (\u03B4):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
			slider_values = {
				'delta': delta
			}

		elif option_1 == "DP Pix":
			flag = 2
			delta = st.slider("Privacy Budget (\u03B4):", min_value=1, max_value=50, value=5, step=1)
			b = st.slider("Block Size (b):", min_value=1, max_value=25, value=12, step=1)
			m = st.slider("Number of Pixels (m):", min_value=1, max_value=25, value=16, step=1)
			slider_values = {
				'delta': delta,
				'b': b,
				'm': m
			}

		elif option_1 == "DP Samp":
			flag = 3
			delta = st.slider("Privacy Budget (\u03B4):", min_value=1, max_value=50, value=25, step=1)
			k = st.slider("Number of clusters (k):", min_value=1, max_value=50, value=24, step=1)
			m = st.slider("Number of Pixels (m):", min_value=1, max_value=25, value=12, step=1)
			slider_values = {
				'delta': delta,
				'k': k,
				'm': m
			}

		if st.button('Apply'):
			# Apply effects and get the processed image
			after_image = apply_effects(image, option_1, slider_values)
			output_img = Image.fromarray(after_image.astype(np.uint8))
			# Convert the processed image back to PIL format for Streamlit
			# after_image_pil = Image.fromarray(after_image.astype('uint8'))
			output_file_path = os.path.join(AFTER_FOLDER, afterFileName)
			output_img.save(output_file_path)
			# Display the processed image in col2
			with col2:
				st.write("Photo after obfuscation")
				st.image(output_img, caption="Photo after Obfuscation")

if __name__ == "__main__":
	main()
