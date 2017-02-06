import tensorflow as tf
import numpy

def inference(input_x, embedding_dim, lstm_hidden_dim_1, vocab_size,
    lstm_hidden_dim_2=None, dropout=None) :
    """
    Args:
        input_x: 2D tensor batch_size X time_step
        embedding_dim: embedding dimension
        lstm_hidden_dim_1: the dimension of the hidden unit of the bottom lstm 
        lstm_hidden_dim_2(optional): the dimension of the hidden unit of the top lstm
        vocab_size: vocabulary size
        dropout(optional): dropout keep probability, it should be a placeholder
    Returns:
        logits: predict result
        pretrain_list: the variable that can be pretrianed by lstm
        output_linear_list: the last output linear layer(cannot pretrained bt lstm)
    """
    pretrain_list = []
    output_linear_list = []

    #embedding layer
    with tf.name_scope('embedding'):
        init_width = 0.5 / embedding_dim
        emb = tf.Variable(
            tf.random_uniform(
            [vocab_size, embedding_dim], -init_width, init_width),
            name="emb")
        input_emb = tf.nn.embedding_lookup(emb, input_x)

    # add embedding matrix to pretrain list
    pretrain_list.append(emb)

    #lstm1 layer
    with tf.name_scope('recurrent_layer1'):
        cell = tf.nn.rnn_cell.LSTMCell(lstm_hidden_dim_1, state_is_tuple=True)
        if dropout:
            cell = tf.nn.rnn_cell.DropoutWrapper(cell, input_keep_prob=dropout, output_keep_prob=dropout)
        initial_state_vector = tf.get_variable('initial_state_vector', [1, lstm_hidden_dim_1])

        initial_state = tf.tile(initial_state_vector, [tf.shape(input_x)[0], 1])
        lstm1_outputs, final_state = tf.nn.dynamic_rnn(cell, input_emb, initial_state=initial_state)
        #lstm1_outputs: [batch_size, num_steps, state_size]

    # add LSTM variable to pretrain list
    with tf.variable_scope('recurrent_layer1') as vs:
        lstm1_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=vs.name)
        pretrain_list = pretrain_list + lstm1_variables

    #output layer which is attached after lstm1 
    with tf.name_scope('output_lstm1_linear'):
        W = tf.get_variable('W', [lstm_hidden_dim_1, vocab_size])
        b = tf.get_variable('b', [vocab_size], initializer=tf.constant_initializer(0.0))

        logits = tf.matmul(att_lstm_outputs, W) + b

    #dropout, pretrain
    #add pretrain_param, output_linear_param
    output_linear_list.append(W)
    output_linear_list.append(b)

    return logits, pretrain_list, output_linear_list

def loss(logits, labels, entropy=None, entropy_reg=0) :
    """
    args:
        logits: [batch_size, num_steps, vocab_size] dtype='float32'
        labels: [batch_size, num_steps] dtype='int'
    return :
        total_label_loss: the summation of the full tensor loss
        loss: for training
    """
    cross_entropy_result = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels, logits=logits)
    total_label_loss = tf.reduce_sum(cross_entropy_result)
    #devide vocab size
    loss = tf.reduce_mean(cross_entropy_result)
    if entropy :
        loss = loss + entropy_reg*entropy

    return total_label_loss, loss

def training(loss, learning_rate, grad_norm) :
    """
    args:
        loss
        learning_rate: it should be a placeholder
        grad_norm: max grad norm

    return :
        train_op
    """
    # Add a scalar summary for the snapshot loss.
    tf.summary.scalar('loss', loss)
    # Create the gradient descent optimizer with the given learning rate.
    optimizer = tf.train.AdamOptimizer(learning_rate)
    gvs = optimizer.compute_gradients(loss)
    capped_gvs = [(tf.clip_by_norm(grad, grad_norm), var) for grad, var in gvs]
    # Use the optimizer to apply the gradients that minimize the loss
    # (and also increment the global step counter) as a single training step.
    train_op = optimizer.apply_gradients(capped_gvs)
    return train_op





