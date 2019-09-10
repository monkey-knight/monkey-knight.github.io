---
layout: article
title: text classification
permalink: /_posts/python/tensorflow/2019-09-10-text-classification
tags: Tensorflow
aside:
  toc: true
sidebar:
  nav: Tensorflow
---

<!--more-->

此实验将文本形式的影评分为“正面”或“负面”影评。


```python
import tensorflow as tf
from tensorflow import keras

import numpy as np

print(tf.__version__)
```

    1.14.0


## 准备数据集

我们将使用 `IMDB` 数据集，其中包括 $5000$ 条影评文本。`Tensorflow` 中包含了 `IMDB` 数据集。


```python
imdb = keras.datasets.imdb

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
```

`num_words=10000` 参数会保留数据集中出现频次前 $10000$ 的字词。为确保数据规模处于可管理的水平，罕见字词将被舍弃。

## 分析数据集

`Tensorflow` 已经对该数据集进行了处理，其将影评（字词序列）转换为整数序列，其中每个整数表示字典中的一个特定字词。


```python
print(train_data[0])
```

    [1, 14, 22, 16, 43, 530, 973, 1622, 1385, 65, 458, 4468, 66, 3941, 4, 173, 36, 256, 5, 25, 100, 43, 838, 112, 50, 670, 2, 9, 35, 480, 284, 5, 150, 4, 172, 112, 167, 2, 336, 385, 39, 4, 172, 4536, 1111, 17, 546, 38, 13, 447, 4, 192, 50, 16, 6, 147, 2025, 19, 14, 22, 4, 1920, 4613, 469, 4, 22, 71, 87, 12, 16, 43, 530, 38, 76, 15, 13, 1247, 4, 22, 17, 515, 17, 12, 16, 626, 18, 2, 5, 62, 386, 12, 8, 316, 8, 106, 5, 4, 2223, 5244, 16, 480, 66, 3785, 33, 4, 130, 12, 16, 38, 619, 5, 25, 124, 51, 36, 135, 48, 25, 1415, 33, 6, 22, 12, 215, 28, 77, 52, 5, 14, 407, 16, 82, 2, 8, 4, 107, 117, 5952, 15, 256, 4, 2, 7, 3766, 5, 723, 36, 71, 43, 530, 476, 26, 400, 317, 46, 7, 4, 2, 1029, 13, 104, 88, 4, 381, 15, 297, 98, 32, 2071, 56, 26, 141, 6, 194, 7486, 18, 4, 226, 22, 21, 134, 476, 26, 480, 5, 144, 30, 5535, 18, 51, 36, 28, 224, 92, 25, 104, 4, 226, 65, 16, 38, 1334, 88, 12, 16, 283, 5, 16, 4472, 113, 103, 32, 15, 16, 5345, 19, 178, 32]


训练数据集和测试数据集的数量均为 $25000$ 条影评文本。


```python
print('Training entries: {}, labels: {}'.format(len(train_data), len(train_labels)))
print('Testing entries: {}, labels: {}'.format(len(test_data), len(test_labels)))
```

    Training entries: 25000, labels: 25000
    Testing entries: 25000, labels: 25000


如下面代码所示，影评的长度会有所不同。但是神经网络的输入格式是固定的，所以这个问题需要我们稍后解决。


```python
print('第一条影评的长度：', len(train_data[0]))
print('第二条影评的长度：', len(train_data[1]))
```

    第一条影评的长度： 218
    第二条影评的长度： 189


### 将整数转换回文本

将整数转换回文本在之后会很有作用。接下来的代码帮助我们做到这件事。


```python
# a dictionary mapping words to integer index
word_index = imdb.get_word_index()
print(list(word_index.items())[:5])

# The first indices are reserved
word_index = {k:(v+3) for k,v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

# a dictionary mapping integer index to words
reversed_word_index = dict([(v, k) for (k, v) in word_index.items()])
print(list(reversed_word_index.items())[:5])

def decode_review(text):
    return ' '.join([reversed_word_index.get(i) for i in text])

print(decode_review(train_data[0]))
```

    [('fawn', 34701), ('tsukino', 52006), ('nunnery', 52007), ('sonja', 16816), ('vani', 63951)]
    [(34704, 'fawn'), (52009, 'tsukino'), (52010, 'nunnery'), (16819, 'sonja'), (63954, 'vani')]
    <START> this film was just brilliant casting location scenery story direction everyone's really suited the part they played and you could just imagine being there robert <UNK> is an amazing actor and now the same being director <UNK> father came from the same scottish island as myself so i loved the fact there was a real connection with this film the witty remarks throughout the film were great it was just brilliant so much that i bought the film as soon as it was released for <UNK> and would recommend it to everyone to watch and the fly fishing was amazing really cried at the end it was so sad and you know what they say if you cry at a film it must have been good and this definitely was also <UNK> to the two little boy's that played the <UNK> of norman and paul they were just brilliant children are often left out of the <UNK> list i think because the stars that play them all grown up are such a big profile for the whole film but these children are amazing and should be praised for what they have done don't you think the whole story was so lovely because it was true and was someone's life after all that was shared with us all


## 数据集的预处理

影评（整数数组）必须转换为 `tensor`，然后才能传递到神经网络中。我们可以通过以下两种方法实现这种转换：
- 对数组进行 `one_hot` 编码，即将数组转换成只有 $0$ 和 $1$ 的向量。例如，序列 $[3, 5]$ 将变成一个 $10000$ 维的向量，除索引 $3$ 和 $5$ 转换为 $1$ 之外，其余全转换为 $0$。不过，这种方法会占用大量的内存。存储这个数据集需要 `num_words * num_reviews` 维的矩阵。
- 填充数组，使得这些数组具有相同的长度，然后创建一个形状为 `max_length * num_reviews` 的 `tensor`。我们可以使用一个能够处理这种形状的 `Embedding` 层作为网络的第一层。

在本实验中，我们使用第二种方法。

我们可以使用 `pad_sequences` 函数将长度标准化。


```python
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)

test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                       value=word_index["<PAD>"],
                                                       padding='post',
                                                       maxlen=256)
```

现在来看看样本的长度：


```python
print(len(train_data[0]), len(test_data[0]))
```

    256 256


查看第一条影评：


```python
print(train_data[0])
```

    [   1   14   22   16   43  530  973 1622 1385   65  458 4468   66 3941
        4  173   36  256    5   25  100   43  838  112   50  670    2    9
       35  480  284    5  150    4  172  112  167    2  336  385   39    4
      172 4536 1111   17  546   38   13  447    4  192   50   16    6  147
     2025   19   14   22    4 1920 4613  469    4   22   71   87   12   16
       43  530   38   76   15   13 1247    4   22   17  515   17   12   16
      626   18    2    5   62  386   12    8  316    8  106    5    4 2223
     5244   16  480   66 3785   33    4  130   12   16   38  619    5   25
      124   51   36  135   48   25 1415   33    6   22   12  215   28   77
       52    5   14  407   16   82    2    8    4  107  117 5952   15  256
        4    2    7 3766    5  723   36   71   43  530  476   26  400  317
       46    7    4    2 1029   13  104   88    4  381   15  297   98   32
     2071   56   26  141    6  194 7486   18    4  226   22   21  134  476
       26  480    5  144   30 5535   18   51   36   28  224   92   25  104
        4  226   65   16   38 1334   88   12   16  283    5   16 4472  113
      103   32   15   16 5345   19  178   32    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0    0    0    0    0    0    0    0    0    0    0
        0    0    0    0]


## 构建验证集

在训练时，我们需要检查模型处理从未见过的数据的准确率。我们从原始训练数据中分离出 $10000$ 个样本，创建一个验证集。


```python
validation_data = train_data[:10000]
partial_train_data = train_data[10000:]

validation_labels = train_labels[:10000]
partial_train_labels = train_labels[10000:]

print(len(validation_data), len(validation_labels))
```

    10000 10000


## 构建模型

### 创建神经网络

在构建模型时，我们需要考虑两个方面的问题：
- 模型的神经网络由多少层构成。
- 每一层需要多少个神经元。


```python
vocabulary_size = 10000

model = keras.Sequential()
model.add(keras.layers.Embedding(vocabulary_size, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

model.summary()
```

    Model: "sequential_1"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    embedding_1 (Embedding)      (None, None, 16)          160000    
    _________________________________________________________________
    global_average_pooling1d_1 ( (None, 16)                0         
    _________________________________________________________________
    dense_2 (Dense)              (None, 16)                272       
    _________________________________________________________________
    dense_3 (Dense)              (None, 1)                 17        
    =================================================================
    Total params: 160,289
    Trainable params: 160,289
    Non-trainable params: 0
    _________________________________________________________________


- 第一层是 `Embedding` 层。`Embedding` 层的具体描述见 [YJango的Word Embedding--介绍](https://zhuanlan.zhihu.com/p/27830489) 和 [keras Embedding层详解](https://blog.csdn.net/jiangpeng59/article/details/77533309)。
- 第二层是 `GlobalAveragePooling1D` 层。
- 第三层是包含了 $16$ 个神经元的全连接层。
- 第四层是只有 $1$ 个神经元的全连接层。

### 编译模型

在编译模型时需要设定一个损失函数和一个优化器。由于本实验是一个文本二分类问题，所以我们使用 `binary_crossentropy` 损失函数。

该函数并不是唯一的损失函数，例如，您可以选择 mean_squared_error。但一般来说，binary_crossentropy 更适合处理概率问题。


```python
model.compile(optimizer=tf.train.AdamOptimizer(),
             loss='binary_crossentropy',
             metrics=['accuracy'])
```

## 训练模型

以 $512$ 个样本作为一个 `batch` 训练模型 $40$ 个 `epochs`。


```python
history = model.fit(partial_train_data,
                    partial_train_labels,
                    epochs=40,
                    batch_size=512,
                    validation_data=(validation_data, validation_labels))
```

    Train on 15000 samples, validate on 10000 samples
    Epoch 1/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0960 - acc: 0.9743 - val_loss: 0.3081 - val_acc: 0.8833
    Epoch 2/40
    15000/15000 [==============================] - 1s 40us/sample - loss: 0.0922 - acc: 0.9761 - val_loss: 0.3112 - val_acc: 0.8827
    Epoch 3/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0891 - acc: 0.9769 - val_loss: 0.3142 - val_acc: 0.8832
    Epoch 4/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0859 - acc: 0.9789 - val_loss: 0.3176 - val_acc: 0.8816
    Epoch 5/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0832 - acc: 0.9797 - val_loss: 0.3214 - val_acc: 0.8816
    Epoch 6/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0799 - acc: 0.9807 - val_loss: 0.3268 - val_acc: 0.8798
    Epoch 7/40
    15000/15000 [==============================] - 1s 40us/sample - loss: 0.0773 - acc: 0.9817 - val_loss: 0.3286 - val_acc: 0.8806
    Epoch 8/40
    15000/15000 [==============================] - 1s 40us/sample - loss: 0.0744 - acc: 0.9831 - val_loss: 0.3316 - val_acc: 0.8810
    Epoch 9/40
    15000/15000 [==============================] - 1s 40us/sample - loss: 0.0719 - acc: 0.9840 - val_loss: 0.3358 - val_acc: 0.8796
    Epoch 10/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0692 - acc: 0.9850 - val_loss: 0.3396 - val_acc: 0.8800
    Epoch 11/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0669 - acc: 0.9854 - val_loss: 0.3437 - val_acc: 0.8797
    Epoch 12/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0648 - acc: 0.9861 - val_loss: 0.3521 - val_acc: 0.8753
    Epoch 13/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0628 - acc: 0.9869 - val_loss: 0.3524 - val_acc: 0.8780
    Epoch 14/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0600 - acc: 0.9877 - val_loss: 0.3561 - val_acc: 0.8779
    Epoch 15/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0580 - acc: 0.9887 - val_loss: 0.3608 - val_acc: 0.8768
    Epoch 16/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0559 - acc: 0.9895 - val_loss: 0.3673 - val_acc: 0.8754
    Epoch 17/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0539 - acc: 0.9898 - val_loss: 0.3693 - val_acc: 0.8768
    Epoch 18/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0525 - acc: 0.9909 - val_loss: 0.3777 - val_acc: 0.8739
    Epoch 19/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0503 - acc: 0.9915 - val_loss: 0.3779 - val_acc: 0.8766
    Epoch 20/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0485 - acc: 0.9918 - val_loss: 0.3837 - val_acc: 0.8753
    Epoch 21/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0468 - acc: 0.9923 - val_loss: 0.3877 - val_acc: 0.8769
    Epoch 22/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0451 - acc: 0.9927 - val_loss: 0.3919 - val_acc: 0.8758
    Epoch 23/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0435 - acc: 0.9931 - val_loss: 0.3981 - val_acc: 0.8758
    Epoch 24/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0419 - acc: 0.9934 - val_loss: 0.4021 - val_acc: 0.8753
    Epoch 25/40
    15000/15000 [==============================] - 1s 42us/sample - loss: 0.0406 - acc: 0.9935 - val_loss: 0.4064 - val_acc: 0.8749
    Epoch 26/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0393 - acc: 0.9937 - val_loss: 0.4114 - val_acc: 0.8746
    Epoch 27/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0374 - acc: 0.9945 - val_loss: 0.4163 - val_acc: 0.8739
    Epoch 28/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0360 - acc: 0.9948 - val_loss: 0.4218 - val_acc: 0.8728
    Epoch 29/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0350 - acc: 0.9951 - val_loss: 0.4258 - val_acc: 0.8741
    Epoch 30/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0339 - acc: 0.9953 - val_loss: 0.4311 - val_acc: 0.8732
    Epoch 31/40
    15000/15000 [==============================] - 1s 40us/sample - loss: 0.0322 - acc: 0.9956 - val_loss: 0.4394 - val_acc: 0.8707
    Epoch 32/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0311 - acc: 0.9955 - val_loss: 0.4420 - val_acc: 0.8715
    Epoch 33/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0299 - acc: 0.9961 - val_loss: 0.4463 - val_acc: 0.8718
    Epoch 34/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0286 - acc: 0.9963 - val_loss: 0.4521 - val_acc: 0.8701
    Epoch 35/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0275 - acc: 0.9967 - val_loss: 0.4574 - val_acc: 0.8706
    Epoch 36/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0265 - acc: 0.9969 - val_loss: 0.4620 - val_acc: 0.8698
    Epoch 37/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0254 - acc: 0.9969 - val_loss: 0.4700 - val_acc: 0.8689
    Epoch 38/40
    15000/15000 [==============================] - 1s 39us/sample - loss: 0.0246 - acc: 0.9972 - val_loss: 0.4718 - val_acc: 0.8687
    Epoch 39/40
    15000/15000 [==============================] - 1s 38us/sample - loss: 0.0237 - acc: 0.9975 - val_loss: 0.4774 - val_acc: 0.8686
    Epoch 40/40
    15000/15000 [==============================] - 1s 41us/sample - loss: 0.0227 - acc: 0.9979 - val_loss: 0.4843 - val_acc: 0.8679


## 评估模型


```python
evaluation = model.evaluate(test_data, test_labels)
print(evaluation)
```

    25000/25000 [==============================] - 1s 42us/sample - loss: 0.5147 - acc: 0.8568
    [0.5146519127082825, 0.8568]


## 创建准确率和损失随时间变化的图

`model.fit()` 返回一个 `History` 对象，该对象包含一个字典，其中包括训练期间发生的所有情况：


```python
%matplotlib inline

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)

# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
```


![png](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/tensorflow/assets/output_39_0.png)


```python
plt.clf()   # clear figure

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.show()
```

![png](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/tensorflow/assets/output_40_0.png)

