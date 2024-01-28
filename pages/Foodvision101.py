# create a streamlit app.py
# Imports
import os
import torch
import torchvision
from torch import nn
import streamlit as st
from timeit import default_timer as timer
from typing import Tuple, Dict
from PIL import Image


def create_effnetb2_model(num_classes: int = 3,
                          seed: int = 42):
    """Creates an EfficientNetB2 feature extractor model and transforms.

    Args:
        num_classes (int, optional): number of classes in the classifier head. 
            Defaults to 3.
        seed (int, optional): random seed value. Defaults to 42.

    Returns:
        model (torch.nn.Module): EffNetB2 feature extractor model. 
        transforms (torchvision.transforms): EffNetB2 image transforms.
    """
    # Create EffNetB2 pretrained weights, transforms and model
    weights = torchvision.models.EfficientNet_B2_Weights.DEFAULT
    transforms = weights.transforms()
    model = torchvision.models.efficientnet_b2(weights=weights)

    # Freeze all layers in base model
    for param in model.parameters():
        param.requires_grad = False

    # Change classifier head with random seed for reproducibility
    torch.manual_seed(seed)
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features=1408, out_features=num_classes),
    )

    return model, transforms


# Setup class names
with open("class_names.txt", "r") as f:
    class_names = [food_name.strip() for food_name in f.readlines()]

# Create model
effnetb2, effnetb2_transforms = create_effnetb2_model(
    num_classes=101,  # could also use len(class_names)
)

# Load saved weights
effnetb2.load_state_dict(
    torch.load(
        f="09_pretrained_effnetb2_feature_extractor_food101_20_percent.pth",
        map_location=torch.device("cpu"),  # load to CPU
    )
)

# Predict function


def predict(img) -> Tuple[Dict, float]:
    start_time = timer()

    # Transform the target image and add a batch dimension
    img = effnetb2_transforms(img).unsqueeze(0)

    # Put model into evaluation mode and turn on inference mode
    effnetb2.eval()
    with torch.inference_mode():
        pred_probs = torch.softmax(effnetb2(img), dim=1)

    # Create a prediction label and prediction probability dictionary for each prediction class
    pred_labels_and_probs = {class_names[i]: float(
        pred_probs[0][i]) for i in range(len(class_names))}

    # Calculate the prediction time
    pred_time = round(timer() - start_time, 5)

    return pred_labels_and_probs, pred_time

# Streamlit app


def main():
    st.title("FoodVision Big 🍔👁")
    st.write(
        "An EfficientNetB2 feature extractor computer vision model to classify images of food into [101 different classes](https://github.com/mrdbourke/pytorch-deep-learning/blob/main/extras/food101_class_names.txt).")
    st.markdown(
        "Created at when learn [PyTorch Model Deployment](https://www.learnpytorch.io/09_pytorch_model_deployment/).")

    # Upload image through Streamlit
    uploaded_image = st.file_uploader(
        "Choose an image...", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        # Display the image
        st.image(uploaded_image, caption="Uploaded Image.",
                 use_column_width=True)
        st.write("")
        st.write("Classifying...")

        # Convert to PIL Image
        pil_image = Image.open(uploaded_image)

        # Call the prediction function
        predictions, prediction_time = predict(pil_image)

        # Display predictions and prediction time
        st.subheader("Predictions:")
        st.json(predictions)
        st.subheader("Prediction time (s):")
        st.write(prediction_time)
