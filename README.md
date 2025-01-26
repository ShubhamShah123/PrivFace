# PrivFace

### Overview
<div style="text-align: justify">
PrivFace is an interactive Streamlit-based application that allows users to upload images, apply privacy-preserving obfuscation methods to the images, and visualize the results. The app provides three different obfuscation techniques <i>("DP Snow", "DP Pix", and "DP Samp")</i> that use differential privacy to modify the uploaded images while maintaining privacy.
</div<

### Features
1.  <strong>Upload Images:</strong> Users can upload photos in JPG, JPEG, or PNG formats.
2.  <strong>Multiple Obfuscation Methods:</strong> Users can choose from three obfuscation methods:

    * DP Snow: Adds noise to the image to obscure details.
    * DP Pix: Applies pixel-based transformations with adjustable block sizes and pixel counts.
    * DP Samp: Uses clustering and sampling techniques to alter the image.
    
3. <strong>Customizable Parameters:</strong> Each method has adjustable sliders for parameters like privacy budget (<i>&#948;</i>) , block size (<i>b</i>), number of pixels(<i>m</i>) and number of clusters(<i>k</i>).

4. <strong>Streamlined Interface:</strong> A clean and interactive interface makes it easy to experiment with different settings.
---
### Installation and Setup
#### Prerequisites
Ensure that you have this installed
* python 3.8+
* pip

#### Installation Steps
1. <strong>Clone the repo: </strong>
 ```bash
    git clone <repository-url>
    cd <repository-folder>
```
2. <strong>Install the dependencies</strong>
```bash
    pip install -r requirements.txt
```
3. <strong>Run the app</strong>
```bash
    streamlit run app.py
```
4. <strong>Access the app: </strong>Open the browser and navigate [`http://localhost:8501`](#localhost)
---
### Usage Guide
1. Launch the app by running streamlit run app.py.
2. Upload an image using the "Upload a photo" button.
3. View the original image in the left column (Photo 1).
4. Use the dropdown menu to select an obfuscation method:
    - "DP Snow"
    - "DP Pix"
    - "DP Samp"
5. Adjust the sliders to configure the parameters for the selected method:
    - DP Snow: Adjust privacy budget (δ).
    - DP Pix: Adjust privacy budget (δ), block size, and the number of pixels.
    - DP Samp: Adjust privacy budget (δ), the number of clusters, and the number of pixels.
6. Click the "Apply" button to generate the obfuscated image.
7. View the obfuscated image in the right column (Photo 2).
---
### File Structure
```bash
project-folder/
├── afterFolder/           # Stores the obfuscated images    
├── main.py                # Main application file
├── image_effects.py       # Module for implementing obfuscation methods
├── requirements.txt       # Python dependencies
├── README.md              # Documentation
```
---
### Technical Details
#### Obfuscation Methods

1. DP Snow:<div style="text-align: justify">
    - DP-SNOW is a de-identification method that combines differential privacy with the concept of k-anonymity. The algorithm groups similar faces together and then applies a noiseadding mechanism to ensure privacy. 
    - By maintaining the overall structure of the face while adding noise, DP-SNOW
produces de-identified faces that are visually similar to the
original images, while still protecting individual privacy.

2. DP Pix:
    - Pixel-based de-identification technique that applies differential privacy by perturbing individual pixel values in the image.
    - The method adds carefully calibrated noise to the pixels, ensuring that the output image is both private and visually similar to the original image.
This allows for privacy preservation while maintaining the
overall structure and appearance of the face.

3. DP Samp:
    - The <i>DP-SAMP</i> method is a sampling-based approach that
leverages differential privacy. It involves randomly selecting
a subset of facial features from the original image and replacing them with corresponding features from other images in
the dataset. 
    - This process ensures that the de-identified face
is a composite of multiple individuals, making it difficult to
link the output image to any specific person.</div>


#### Core Functionality

The ``` apply-effects ``` function maps the user provided methods and parameters of the respective obfuscation methods in the ```image-effects``` module.


#### Libraries Used
* Streamlit - For creating the interactive web interface.
* Pillow - For image processing.
* NumPy - For numerical processing.
* Scikit Learn - For clustering the pixels using KMeans clustering.
* Scipy - For statiscal calulcations.

#### Future Enhancements

1. Add support for more image formats (e.g., BMP, TIFF).
2. Include additional obfuscation methods.
3. Allow users to download the obfuscated images.
4. Implement batch processing for multiple images.
5. Integrate a preview of parameter effects before applying them.

---
### References

1. Cynthia Dwork and Aaron Roth. 2014. *The Algorithmic Foundations of Differential Privacy.* Found. Trends Theor. Comput. Sci. 9, 3–4 (Aug 2014), 211–407. [https://doi.org/10.1561/0400000042](https://doi.org/10.1561/0400000042)

2. Liyue Fan. 2018. *Image Pixelization with Differential Privacy.* In *Database Security.*

3. Liyue Fan. 2019. *Differential Privacy for Image Publication.*

4. Oran Gafni, Lior Wolf, and Yaniv Taigman. 2019. *Live Face De-Identification in Video.* arXiv:1911.08348 [cs.LG].

5. Isabelle Hupont Torres and Carles Fernández. 2019. *DemogPairs: Quantifying the Impact of Demographic Imbalance in Deep Face Recognition.* 1–7. [https://doi.org/10.1109/FG.2019.8756625](https://doi.org/10.1109/FG.2019.8756625)

6. Brendan John, Ao Liu, Lirong Xia, Sanjeev Koppal, and Eakta Jain. 2020. *Let It Snow: Adding Pixel Noise to Protect the User’s Identity.* In *ACM Symposium on Eye Tracking Research and Applications* (Stuttgart, Germany) (ETRA ’20 Adjunct). Association for Computing Machinery, New York, NY, USA, Article 43, 3 pages. [https://doi.org/10.1145/3379157.3390512](https://doi.org/10.1145/3379157.3390512)

7. Megvii. [n.d.]. *Face++.* [https://www.faceplusplus.com/](https://www.faceplusplus.com/)

8. Dominick Reilly and Liyue Fan. [n.d.]. *A Comparative Evaluation of Differentially Private Image Obfuscation.* *2021 Third IEEE International Conference on Trust, Privacy and Security in Intelligent Systems and Applications (TPS-ISA)* ([n.d.]). [https://doi.org/10.1109/TPSISA52974.2021.00009](https://doi.org/10.1109/TPSISA52974.2021.00009)

9. Joseph Robinson. 2022. *Balanced Faces in the Wild.* [https://doi.org/10.21227/nmsj-df12](https://doi.org/10.21227/nmsj-df12)

10. Han Wang, Shangyu Xie, and Yuan Hong. 2020. *VideoDP: A Flexible Platform for Video Analytics with Differential Privacy.* *Proceedings on Privacy Enhancing Technologies 2020* (Oct 2020), 277–296. [https://doi.org/10.2478/popets-2020-0073](https://doi.org/10.2478/popets-2020-0073)

11. Mei Wang, Weihong Deng, Jiani Hu, Xunqiang Tao, and Yaohai Huang. 2019. *Racial Faces in-the-Wild: Reducing Racial Bias by Information Maximization Adaptation Network.* arXiv:1812.00194 [cs.CV].

---
### Acknowledgments
<div style="text-align: justify">
Firstly, I would like to thank Dr. Shirin Nilizadeh, my
professor in this course who gave me the oppurtunity to
work on this project and also we would like to express our
gratitude to, Mr. Sadegh Moosavi, who guided us throughout
this project.
</div>
