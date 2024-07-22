import torch

def is_pytorch_model(file_path):
    try:
        # Attempt to load the file as a PyTorch model checkpoint
        torch.load(file_path)
        return True
    except Exception as e:
        return False

file_path = 'final.pth.tar'
if is_pytorch_model(file_path):
    print("yes")
else:
    print("no")
