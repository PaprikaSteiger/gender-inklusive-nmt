# gender-inklusive-nmt
Gender-inklusive nmt system for German and French

## Preprocessing
We adopted byte-pair encoding for tokenized data (Sennrich et al., 2016).
```
cat train.fr train_annotated.fr |subword-nmt learn-bpe -s 3000 > train_codes
for set in train validation test; do
  subword-nmt apply-bpe -c train_codes <${set}.fr >${set}.fr.bpe
  subword-nmt apply-bpe -c train_codes <${set}_annotated.fr >${set}_annotated.fr.bpe
done
```
## Training
Before training, we prepare the training data by splitting it into shards and serializing it into matrix format.
```
python -m sockeye.prepare_data \
-s train.fr.bpe -t train_annotated.fr.bpe --shared-vocab \
--word-min-count 3 --pad-vocab-to-multiple-of 8 --max-seq-len 95 \
--num-samples-per-shard 10000000 --output prepared --max-processes $(nproc)
```

We then train the model with 1 GPU.
```
python -m sockeye.train \
--prepared-data prepared \
--validation-source validation.fr.bpe \
--validation-target validation_annotated.fr.bpe \
--output model \
--num-layers 3 \
--transformer-model-size 1024 --transformer-attention-heads 16 \
--transformer-feed-forward-num-hidden 4096 --amp --batch-type max-word \
--batch-size 5000 --update-interval 80 --checkpoint-interval 500 \
--max-num-checkpoint-not-improved 10 --optimizer-betas 0.9:0.98 \
--initial-learning-rate 0.06325 \
--learning-rate-scheduler-type inv-sqrt-decay --learning-rate-warmup 4000 \
--seed 1
```
## Evaluation (on working)
After training, we rewrite the preprocessed test set.
```
python -m sockeye.translate \
--input test.fr.bpe \
--output out.bpe \
--model model \
--dtype float16 \
--beam-size 5 \
--batch-size 64
