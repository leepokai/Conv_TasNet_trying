# source https://github.com/kaituoxu/Conv-TasNet
# output_directory

which contain the mix audio and the separate audio 
and use pretrained model final.pth.tar to separate the mix audio

# Changes on code
# Changes in EvalDataset Class
**File**: src/data.py

### Before:
```python
class EvalDataset(data.Dataset):
    def __init__(self, mix_dir, mix_json, batch_size, sample_rate=8000):
        ...
```

### After:
```python
class EvalDataset(data.Dataset):
    def __init__(self, mix_dir, mix_json, batch_size, sample_rate=8000):
        ...
        with open(mix_json, 'r') as f:
            mix_infos = json.load(f)['mix']
        ...
```

# Changes in load_mixtures_and_sources Function
**File**: src/data.py

### Before:
```python
def load_mixtures_and_sources(batch):
    ...
    for mix_info, s1_info, s2_info in zip(mix_infos, s1_infos, s2_infos):
        mix_path = mix_info[0]
        s1_path = s1_info[0]
        s2_path = s2_info[0]
        ...
```

### After:
```python
def load_mixtures_and_sources(batch):
    ...
    for mix_info, s1_info, s2_info in zip(mix_infos, s1_infos, s2_infos):
        mix_path = mix_info['mix_path']
        s1_path = s1_info['mix_path']
        s2_path = s2_info['mix_path']
        ...
```

# Changes in load_mixtures Function
**File**: src/data.py

### Before:
```python
def load_mixtures(batch):
    ...
    for mix_info in mix_infos:
        mix_path = mix_info[0]
        ...
```

### After:
```python
def load_mixtures(batch):
    ...
    for mix_info in mix_infos:
        mix_path = mix_info['mix_path']
        ...
```

# Adding and Modifying write Function
**File**: src/separate.py

### Before:
```python
def write(inputs, filename, sr):
    librosa.output.write_wav(filename, inputs, sr)
```

### After:
```python
import soundfile as sf

def write(inputs, filename, sr):
    sf.write(filename, inputs, sr)
```

# Changes in separate Function
**File**: src/separate.py

### Before:
```python
def separate(args):
    ...
    eval_loader = EvalDataLoader(eval_dataset, batch_size=1)
    ...
    def write(inputs, filename, sr):
        librosa.output.write_wav(filename, inputs, sr)
    ...
            write(mixture[i], filename + '.wav')
            for c in range(C):
                write(flat_estimate[i][c], filename + '_s{}.wav'.format(c+1))
```

### After:
```python
def separate(args):
    ...
    eval_loader = DataLoader(eval_dataset, batch_size=1, shuffle=False, collate_fn=_collate_fn_eval)
    ...
    def write(inputs, filename, sr):
        sf.write(filename, inputs, sr)
    ...
            write(mixture[i].cpu().numpy(), filename + '.wav', args.sample_rate)
            for c in range(C):
                write(flat_estimate[i][c].cpu().numpy(), filename + '_s{}.wav'.format(c+1), args.sample_rate)
```

# Adding remove_pad Function Definition
**File**: src/utils.py (Assumed)

### New:
```python
def remove_pad(inputs, input_lengths):
    """
    Remove padding from inputs.
    Args:
        inputs (torch.Tensor): inputs with padding, size [B, C, T]
        input_lengths (torch.Tensor): lengths of each input, size [B]
    Returns:
        list: A list of length B, each item is a torch.Tensor of size [C, T_i]
    """
    results = []
    for i in range(inputs.size(0)):
        results.append(inputs[i, :, :input_lengths[i]].squeeze(0))
    return results
```
