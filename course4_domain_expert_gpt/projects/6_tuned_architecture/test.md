python - <<'PY'
import torch, json
ckpt = torch.load("/home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v6/best.pt", map_location="cpu")
print("ckpt keys:", list(ckpt.keys())[:10])
cfg = json.load(open("/home/pooja-saxena/PoojaVault/Professional/Workbench/Models/llm/language_models/elephantdomain_gpt/gpt-bpe-v6/model_config.json"))
print("config vocab_size:", cfg["model_config"]["vocab_size"])
PY
