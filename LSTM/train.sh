#! /bin/bash
mode='train'
#init_from
#init_method
word_vector_path='../data/word2vec/GoogleNews-vectors-negative300.bin'

data_dir='../data/PTB_data'
save='./model'
#att_file

rnn_size=300
emb_size=300
num_layers=1

batch_size=20
max_seq_length=60
min_seq_length=3

max_epochs=1000
dropout=0.7
max_grad_norm=5
#entropy_reg

learning_rate=0.01
decay_rate=1
learning_rate_decay_after=1000

#gpu_id
#print_every

python ./run.py --mode $mode --word_vector_path $word_vector_path --data_dir $data_dir --save $save --rnn_size $rnn_size --emb_size $emb_size --num_layers $num_layers --batch_size $batch_size --max_seq_length $max_seq_length --min_seq_length $min_seq_length --max_epochs $max_epochs --dropout $dropout --max_grad_norm $max_grad_norm --learning_rate $learning_rate --decay_rate $decay_rate --learning_rate_decay_after $learning_rate_decay_after
