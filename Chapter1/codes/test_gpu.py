import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"cuda available: {torch.cuda.is_available()}")
print(f"cuda info: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'}")