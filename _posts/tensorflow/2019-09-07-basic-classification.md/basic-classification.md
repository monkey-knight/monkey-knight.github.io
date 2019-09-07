
此实验用于训练了一个神经网络模型，来对服装图像进行分类。


```python
import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt
```


```python
print('tensorflow 版本：', tf.__version__)
```

    tensorflow 版本： 1.14.0


## 导入 `Fashion MNIST` 数据集

此实验使用 [Fashion MNIST](https://github.com/zalandoresearch/fashion-mnist) 数据集，其中包含了 `10` 个类别的 `70000` 张灰度图像，每张图像的分辨率为 $28 \times 28$ 像素。

我们将使用 `60000` 张图像来训练网络和 `10000` 张图像来评估网络模型。下面直接使用 `tensorflow.keras` 来加载 `Fashion MNIST` 数据集：


```python
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

print('训练集的数量：', len(train_images))
print('测试集的数量：', len(test_images))
```

    训练集的数量： 60000
    测试集的数量： 10000


## 分析数据集


```python
print('train_images 数据类型：', type(train_images))
print('train_labels 数据类型：', type(train_labels))
print('test_images 数据类型：', type(test_images))
print('test_labels 数据类型：', type(test_labels))
```

    train_images 数据类型： <class 'numpy.ndarray'>
    train_labels 数据类型： <class 'numpy.ndarray'>
    test_images 数据类型： <class 'numpy.ndarray'>
    test_labels 数据类型： <class 'numpy.ndarray'>


`load_data()` 函数会返回四个 `numpy` 数组：
- `train_images` 和 `train_labels` 数组是训练集。
- `test_images` 和 `test_labels` 是测试集。


```python
print('train_images 形状：', train_images[0].shape)
print('test_images 形状：', test_images[0].shape)
print('train_labels[0]：', train_labels[0])
print('test_labels[0]：', test_labels[0])
```

    train_images 形状： (28, 28)
    test_images 形状： (28, 28)
    train_labels[0]： 9
    test_labels[0]： 9


`train_images` 和 `test_images` 的每一个元素都是 $28 \times 28$ 的 `numpy` 数组，对应一张图像，像素值的取值范围为 $[0, 255]$。`train_labels` 和 `test_labels` 的每一个元素都是一个整数，其取值范围为 $[0, 9]$，对应图像的类别。

|标签	|类别|
| --- | --- |
|0	|T-shirt/top|
|1	|Trouser|
|2	|Pullover|
|3	|Dress|
|4	|Coat|
|5	|Sandal|
|6	|Shirt|
|7	|Sneaker|
|8	|Bag|
|9	|Ankle boot|

每个图像都映射到一个标签。由于类别名称不包含在数据集中,因此把他们存储在这里以便在绘制图像时使用:


```python
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
```

## 数据集预处理


```python
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()
```


![output_14_0](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/tensorflow/assets/output_14_0.png)


如上图，如果将训练集的第一张图显示出来，我们可以看到其像素值的取值范围为 $[0, 255]$。


```python
train_images = train_images / 255
test_images = test_images / 255
```

将数据集送往神经网络之前，我们将数据集进行归一化处理，也就是将像素值压缩到 $0$ 和 $1$ 之间。

显示训练集中的前25个图像，并在每个图像下方显示类名，以验证数据格式是否正确。


```python
plt.figure(figsize=(15, 15))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()
```


![output_19_0](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/tensorflow/assets/output_19_0.png)


## 构建模型

### 设置网络层


```python
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax),
])
```

    WARNING: Logging before flag parsing goes to stderr.
    W0907 14:33:55.680732 11912 deprecation.py:506] From C:\Users\monkeyknight\Anaconda3\envs\tensorflow-learning\lib\site-packages\tensorflow\python\ops\init_ops.py:1251: calling VarianceScaling.__init__ (from tensorflow.python.ops.init_ops) with dtype is deprecated and will be removed in a future version.
    Instructions for updating:
    Call initializer instance with the dtype argument instead of passing it to the constructor


网络中的第一层，`keras.layers.Flatten`，将 $28 \times 28$ 的二维数组转换成一维数组。

在像素被展平之后，网络由一个包含有两个 `tf.keras.layers.Dense` 网络层组成。他们是全连接层。 第一个全连接层包含有 $128$ 个节点(或被称为神经元)。第二个(也是最后一个)全连接层是一个包含 $10$ 个节点的 `softmax` 层——它将返回包含 $10$ 个概率分数的数组，总和为1。每个节点包含一个分数，表示当前图像隶属于某一个类别的概率。

### 编译模型

模型编译需要设置的参数包括：
- 损失函数：可以衡量模型在训练过程中的准确度。
- 优化器：模型根据它看到的数据及其损失函数进行更新的方式。
- 度量方式：用于监控训练和测试的每一步。以下示例使用准确率(accuracy)，即正确分类的图像的百分比。


```python
model.compile(loss='sparse_categorical_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])
```

## 训练模型

训练神经网络的步骤如下：
- 提供训练数据集。
- 提供训练标签。


```python
model.fit(train_images, train_labels, epochs=20)
```

    Epoch 1/20
    60000/60000 [==============================] - 5s 82us/sample - loss: 0.4917 - acc: 0.8263
    Epoch 2/20
    60000/60000 [==============================] - 4s 63us/sample - loss: 0.3733 - acc: 0.8656
    Epoch 3/20
    60000/60000 [==============================] - 4s 65us/sample - loss: 0.3353 - acc: 0.8786
    Epoch 4/20
    60000/60000 [==============================] - 4s 72us/sample - loss: 0.3099 - acc: 0.8858
    Epoch 5/20
    60000/60000 [==============================] - 4s 66us/sample - loss: 0.2930 - acc: 0.8923
    Epoch 6/20
    60000/60000 [==============================] - 4s 67us/sample - loss: 0.2787 - acc: 0.8969
    Epoch 7/20
    60000/60000 [==============================] - 4s 68us/sample - loss: 0.2665 - acc: 0.9002
    Epoch 8/20
    60000/60000 [==============================] - 4s 73us/sample - loss: 0.2570 - acc: 0.9049
    Epoch 9/20
    60000/60000 [==============================] - 4s 68us/sample - loss: 0.2450 - acc: 0.9080
    Epoch 10/20
    60000/60000 [==============================] - 4s 69us/sample - loss: 0.2406 - acc: 0.9100
    Epoch 11/20
    60000/60000 [==============================] - 4s 72us/sample - loss: 0.2321 - acc: 0.9140
    Epoch 12/20
    60000/60000 [==============================] - 5s 87us/sample - loss: 0.2254 - acc: 0.9161
    Epoch 13/20
    60000/60000 [==============================] - 5s 77us/sample - loss: 0.2158 - acc: 0.9198
    Epoch 14/20
    60000/60000 [==============================] - 5s 78us/sample - loss: 0.2107 - acc: 0.9199
    Epoch 15/20
    60000/60000 [==============================] - 5s 86us/sample - loss: 0.2060 - acc: 0.9230
    Epoch 16/20
    60000/60000 [==============================] - 5s 81us/sample - loss: 0.2001 - acc: 0.9251
    Epoch 17/20
    60000/60000 [==============================] - 5s 85us/sample - loss: 0.1961 - acc: 0.9260
    Epoch 18/20
    60000/60000 [==============================] - 5s 88us/sample - loss: 0.1896 - acc: 0.9292
    Epoch 19/20
    60000/60000 [==============================] - 5s 79us/sample - loss: 0.1838 - acc: 0.9307
    Epoch 20/20
    60000/60000 [==============================] - 5s 84us/sample - loss: 0.1807 - acc: 0.9322





    <tensorflow.python.keras.callbacks.History at 0x2ac47c36448>



## 评估准确率

接下来比较模型在测试数据集上的执行情况：


```python
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('测试准确率：', test_acc)
```

    10000/10000 [==============================] - 0s 39us/sample - loss: 0.3500 - acc: 0.8912
    测试准确率： 0.8912


## 进行预测

模型训练好之后，就可以用来预测图像了。


```python
predictions = model.predict(test_images)
```

此处，模型已经预测了测试集中每个图像的标签。我们来看看第一个预测:


```python
print(predictions[0])
```

    [1.6380170e-08 6.3935100e-16 1.1461103e-11 2.4103100e-11 3.4604535e-12
     1.8873816e-05 8.1581044e-09 3.3188709e-03 3.9819021e-08 9.9666226e-01]


预测结果是包含了 $10$ 个概率一维数组，分别对应图像属于某一个类别的可能性。一般，我们会选择概率值最大的类别：


```python
print(np.argmax(predictions[0]))
print('类别: ', class_names[np.argmax(predictions[0])])
```

    9
    类别:  Ankle boot


我们可以用图表来查看前 $15$ 个图像的预测结果：


```python
def plot_image(i, predictions_array, true_label, img):
  predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  
  plt.imshow(img, cmap=plt.cm.binary)
  
  predicted_label = np.argmax(predictions_array)
  if predicted_label == true_label:
    color = 'blue'
  else:
    color = 'red'
  
  plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions_array),
                                class_names[true_label]),
                                color=color)

def plot_value_array(i, predictions_array, true_label):
  predictions_array, true_label = predictions_array[i], true_label[i]
  plt.grid(False)
  plt.xticks([])
  plt.yticks([])
  thisplot = plt.bar(range(10), predictions_array, color="#777777")
  plt.ylim([0, 1])
  predicted_label = np.argmax(predictions_array)
  
  thisplot[predicted_label].set_color('red')
  thisplot[true_label].set_color('blue')
    
num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, test_labels, test_images)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, test_labels)
plt.show()
```


![output_41_0](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/tensorflow/assets/output_41_0.png)


最后，我们使用训练的模型对单个图像进行预测。在对单个图像数据进行处理以前，我们需要将单个图像数据加入到一个列表中，这是因为 `tensorflow.keras` 处理的是批量数据。


```python
print(test_images[0].shape)

img = np.expand_dims(test_images[0], axis=0)

print(img.shape)
```

    (28, 28)
    (1, 28, 28)



```python
prediction = model.predict(img)

print(prediction)
```

    [[1.6380170e-08 6.3934613e-16 1.1461125e-11 2.4103053e-11 3.4604470e-12
      1.8873816e-05 8.1581195e-09 3.3188709e-03 3.9819096e-08 9.9666226e-01]]



```python
plot_value_array(0, prediction, test_labels)
plt.xticks(range(10), class_names, rotation=45)
plt.show()
```


![output_45_0](https://raw.githubusercontent.com/monkey-knight/monkey-knight.github.io/master/_posts/tensorflow/assets/output_45_0.png)


`model.predict` 返回一个包含列表的列表，每个图像对应一个列表的数据。获取批次中我们(仅有的)图像的预测:


```python
print(class_names[np.argmax(prediction[0])])
```

    Ankle boot

