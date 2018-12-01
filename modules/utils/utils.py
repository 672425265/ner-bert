

def bert_labels2tokens(dl, labels):
    res_tokens = []
    res_labels = []
    for f, l in zip(dl.dataset, labels):
        label = []
        prev_idx = 0
        for origin_idx in f.tok_map:
            label.append(l[prev_idx])
            prev_idx = origin_idx
            if origin_idx < 0:
                break
        res_tokens.append(f.tokens[1:-1])
        res_labels.append(label[1:])
    return res_tokens, res_labels


def tokens2spans_(tokens_, labels_):
    res = []
    idx_ = 0
    while idx_ < len(tokens_):
        label = labels_[idx_]
        if label in ["I_O", "B_O"]:
            res.append((tokens_[idx_], "O"))
            idx_ += 1
        else:
            span = [tokens_[idx_]]
            span_label = labels_[idx_].split("_")[1]
            idx_ += 1
            while idx_ < len(tokens_) and labels_[idx_] not in ["I_O", "B_O"] and labels_[idx_].split("_")[0]=="I":
                if span_label == labels_[idx_].split("_")[1]:
                    span.append(tokens_[idx_])
                    idx_ += 1
                else:
                    break
            res.append((" ".join(span), span_label))
    return res

def tokens2spans(tokens, labels):
    assert len(tokens) == len(labels)

    return list(map(lambda x: tokens2spans_(*x), zip(tokens, labels)))
