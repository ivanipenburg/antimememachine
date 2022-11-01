import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import io

num_classes = 41
MODEL_PATH = 'model_weights.pt'

# Load model
model = models.resnet50(num_classes=num_classes)
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

def transform_image(image_bytes):
    transform = transforms.Compose([
                transforms.Resize((32, 32)),
                transforms.ToTensor(),
                transforms.Normalize(1.6085, 1.9212)])


    image = Image.open(io.BytesIO(image_bytes))

    return transform(image).unsqueeze(0)

def get_prediction(image_tensor):
    images = image_tensor.reshape(1, -1, 32, 32)
    outputs = model(images)
    outputs = nn.functional.softmax(outputs, dim=1)
    
    if torch.max(outputs) > 0.8:
        _, prediction = torch.max(outputs.data, 1)
        return prediction
    
    return torch.tensor([26])