import torch
import torch.nn as nn
from transformers import AutoModel

class IndoBERT_BiLSTM(nn.Module):
    def __init__(self, hidden_dim=256, output_dim=3):
        super().__init__()

        self.bert = AutoModel.from_pretrained("indobenchmark/indobert-base-p1")

        self.bilstm = nn.LSTM(
            input_size=768,
            hidden_size=hidden_dim,
            batch_first=True,
            bidirectional=True
        )

        self.attention = nn.Linear(hidden_dim * 2, 1)

        self.classifier = nn.Linear(hidden_dim * 2, output_dim)

    def forward(self, input_ids, attention_mask):
        bert_output = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        sequence_output = bert_output.last_hidden_state

        lstm_out, _ = self.bilstm(sequence_output)

        attn_weights = torch.softmax(self.attention(lstm_out), dim=1)
        context = torch.sum(attn_weights * lstm_out, dim=1)

        output = self.classifier(context)

        return output