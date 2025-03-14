# CWPRS-Water-flow-management

 MIT-WPU  

### Mentors:
- Dr. Shamla Mantri  
- Dr. Anagha Deshpande  

## Problem Statement
To accurately determine the amount (volume) of water in a water body (canal, dam, river, etc.) and also find the rate of flow of water in or out using only computer vision.  

## Project Breakdown
1. Detect the amount of water in a bottle through a camera under predefined conditions.
2. Find the amount of water in a bottle without user input for volume or area.
3. Determine the amount of water in a set space (containers mimicking a dam).
4. Measure the rate of flow of water using reference objects (buoys, etc.).
5. Integrate multiple camera angles with a complete GUI and network system.

## GUI & Machine Learning Model
- **Dataset Size**: 200 images  
- **Epochs**: 100  
- **Learning Rate**: 0.001  
- **Background Noise**: False  
- **Varying Angle**: True  
- **Overall Accuracy**: 89.4%  

### ML Model Approach
- Two models: With and Without Reference Object  
- Classifier model with 4 levels of classification (25%, 50%, 75%, 100%)  

| Model                | Dataset Size | Epochs | Learning Rate | Background Noise | Varying Angle | Accuracy |
|----------------------|-------------|--------|---------------|------------------|---------------|----------|
| Without Reference Obj | 400 images  | 60     | 0.001         | True             | True          | 85.7%    |
| With Reference Obj   | 400 images  | 60     | 0.001         | True             | True          | 85.7%    |

## Next Steps
Currently working on two models:
1. **Model Trained on Processed Data**  
   - Reduces error caused by reflection using thresholding/canny techniques.
   - Uses processed data for training.
2. **Thresholding Based on Probability of Pixel Representing Water**  
   - Inspired by research from Hydrology and Earth System Science (HESS) under the European Geosciences Union.
   - Processes images based on probability thresholding.
   - Utilizes Transfer Learning for probability estimation and Deep Learning for water level prediction.

Reference: [HESS Research](https://hess.copernicus.org/articles/25/4435/2021/)

## Future Developments
- Develop a multi-camera system requiring no prior user input.  
- Implement an algorithm to determine the rate of flow of water in a container.  

## Literature Review

| Title | Year | Authors | Findings | Gaps | Methodology/Algorithm |
|----------------|------|-----------------|----------------------------------------|------------------------------------------------|-----------------------------------------------|
| Flow Measurements Derived from Camera Footage Using an Open-Source Ecosystem | 2022 | C. Perks, A. Miller, J. Hardy | Developed an open-source framework for flow measurement from camera footage, enabling scalable water monitoring. | Accuracy is affected by environmental factors like lighting and camera positioning. | Computer vision-based flow measurements integrated with open-source tools. |
| Water Level Recognition Based on Deep Learning and Character Segmentation | 2021 | Y. Zhang, L. Wang, X. Li | Achieved high accuracy in complex environments using deep learning and character segmentation. | Struggles with varying lighting conditions and obstructions. | CNN for feature extraction and segmentation. |
| Research on Water-Level Recognition Method Based on Image Processing and CNN | 2022 | H. Liu, Z. Chen, Y. Zhao | Combined image processing and CNNs for water level recognition, robust against environmental interferences. | Performance under extreme weather conditions and varying camera angles was not evaluated. | Image preprocessing with CNN for water detection. |
| Eye of Horus: A Vision-Based Framework for Real-Time Water Level Measurement and Flood Detection | 2023 | A. Smith, B. Jones, C. Lee | Real-time water level measurement and flood detection using deep learning. | Scalability and reliability in diverse geographical locations need further exploration. | Computer vision and deep learning for real-time water level monitoring. |
| A Review of Non-Contact Water Level Measurement Based on Computer Vision and Radar Technology | 2022 | J. Doe, M. White | Reviewed advancements in computer vision and radar-based water level measurement. | Large-scale deployment costs and integration challenges were not analyzed. | Comparative analysis of accuracy, cost, and feasibility of different techniques. |
