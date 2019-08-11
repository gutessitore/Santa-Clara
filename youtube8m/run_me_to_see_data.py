import tensorflow as tf


string = 'DS_video_train'


for example in tf.python_io.tf_record_iterator("{0}/train0111.tfrecord".format(string)):
    print(tf.train.Example.FromString(example))

input('Press "enter" when done')