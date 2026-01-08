from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "stanford-crfm/BioMedLM"

AutoTokenizer.from_pretrained(model_id)      # downloads tokenizer
AutoModelForCausalLM.from_pretrained(model_id)  # downloads model weights
