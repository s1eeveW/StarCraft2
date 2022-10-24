import numpy as np
import os
import glob
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from PIL import Image

from scipy.stats import ttest_ind

# ..........torch imports............
import torch
import torchvision


from torch.utils.data import IterableDataset, DataLoader
from torchvision import transforms

#.... Captum imports..................
from captum.attr import LayerGradientXActivation, LayerIntegratedGradients

from captum.concept import TCAV
from captum.concept import Concept

from captum.concept._utils.data_iterator import dataset_to_dataloader, CustomIterableDataset
from captum.concept._utils.common import concepts_to_str

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"

def transform(img):
    return transforms.Compose(
        [
            # transforms.Resize(256),
            # transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
            ),
        ]
    )(img)


def get_tensor_from_filename(filename):
    img = Image.open(filename).convert("RGB")
    return transform(img)


def load_image_tensors(class_name, root_path='images', transform=True):
    path = os.path.join(root_path, class_name)
    filenames = glob.glob(path + '/*.png')

    tensors = []
    for filename in filenames:
        img = Image.open(filename).convert('RGB')
        tensors.append(transform(img) if transform else img)

    return tensors

def assemble_concept(name, id, concepts_path="images/Single/incept_concept/"):
    concept_path = os.path.join(concepts_path, name) + "/"
    dataset = CustomIterableDataset(get_tensor_from_filename, concept_path)
    concept_iter = dataset_to_dataloader(dataset)

    return Concept(id=id, name=name, data_iter=concept_iter)

concepts_path = "images/Single/incept_concept/"

Player1_concept = assemble_concept("Banshee", 0, concepts_path=concepts_path)
Player2_concept = assemble_concept("111", 1, concepts_path=concepts_path)
# Player3_concept = assemble_concept("Serral", 2, concepts_path=concepts_path)

random_0_concept = assemble_concept("random_0", 2, concepts_path=concepts_path)
random_1_concept = assemble_concept("random_1", 3, concepts_path=concepts_path)

# n_figs = 4
# n_concepts = 4
#
# fig, axs = plt.subplots(n_concepts, n_figs + 1, figsize=(16, 4 * n_concepts))
#
# for c, Banshee in enumerate([Player1_concept, Player2_concept, random_0_concept, random_1_concept]):
#     concept_path = os.path.join(concepts_path, Banshee.name) + "/"
#     img_files = glob.glob(concept_path + '*')
#     for i, img_file in enumerate(img_files[:n_figs + 1]):
#         if os.path.isfile(img_file):
#             if i == 0:
#                 axs[c, i].text(1.0, 0.5, str(Banshee.name), ha='right', va='center', family='sans-serif', size=24)
#
#                 img = plt.imread(img_file)
#                 plt.imshow(img)
#                 # pylab.show()
#             else:
#                 img = plt.imread(img_file)
#                 axs[c, i].imshow(img)
#
#             axs[c, i].axis('off')

# Pre-trained 'GoogleNet' model
# model = torchvision.models.googlenet(weights='GoogLeNet_Weights.DEFAULT')

# Trained binary classifier of 'MobileNet'
loaded_dict = torch.load('inception1.pt')
# model = torchvision.models.mobilenet_v2()   #注意这里需要对模型结构有定义
model = torchvision.models.inception_v3()
model.state_dict = loaded_dict
model = model.eval()
print(model)

# Inception layers
# layers = ['Mixed_5b', 'Mixed_5c', 'Mixed_5d', 'Mixed_6a', 'Mixed_6b', 'Mixed_6c', 'Mixed_6d', 'Mixed_6e', 'Mixed_7a', 'Mixed_7b', 'Mixed_7c', 'fc']
# layers = ['Mixed_5b', 'Mixed_5c', 'Mixed_5d', 'Mixed_6a', 'Mixed_6b', 'Mixed_6c', 'Mixed_6d', 'Mixed_6e', 'Mixed_7a', 'Mixed_7b', 'Mixed_7c']
layers = ['Mixed_6c', 'Mixed_6d', 'Mixed_6e']

# MobileNet layers
# layers = ['features', 'classifier']


mytcav = TCAV(model=model,
              layers=layers,
              layer_attr_method=LayerIntegratedGradients(
                model, None, multiply_by_inputs=False))

experimental_set_rand = [[Player1_concept, random_0_concept], [Player1_concept, random_1_concept]]

# Load sample images from folder
zebra_imgs = load_image_tensors('Single/incept_target', transform=False)

# Show some samples of images
# print(zebra_imgs)
# fig, axs = plt.subplots(1, 5, figsize=(25, 5))
# axs[0].imshow(zebra_imgs[0])
# axs[1].imshow(zebra_imgs[41])
# axs[2].imshow(zebra_imgs[34])
# axs[3].imshow(zebra_imgs[31])
# axs[4].imshow(zebra_imgs[30])
#
# axs[0].axis('off')
# axs[1].axis('off')
# axs[2].axis('off')
# axs[3].axis('off')
# axs[4].axis('off')
#
# plt.show()

# Load sample images from folder
zebra_tensors = torch.stack([transform(img) for img in zebra_imgs])
# print(experimental_set_rand)

# zebra class index
zebra_ind = 2

# improve player Banshee(you te dian)
# rush (other) mobile_concepts

tcav_scores_w_random = mytcav.interpret(inputs=zebra_tensors,
                                        experimental_sets=experimental_set_rand,
                                        target=zebra_ind,
                                        n_steps=5,
                                       )


def format_float(f):
    return float('{:.3f}'.format(f) if abs(f) >= 0.0005 else '{:.3e}'.format(f))

def plot_tcav_scores(experimental_sets, tcav_scores):
    fig, ax = plt.subplots(1, len(experimental_sets), figsize=(25, 7))

    barWidth = 1 / (len(experimental_sets[0]) + 1)
    for idx_es, concepts in enumerate(experimental_sets):

        concepts = experimental_sets[idx_es]
        concepts_key = concepts_to_str(concepts)
        print(concepts)
        print(concepts_key)
        pos = [np.arange(len(layers))]
        for i in range(1, len(concepts)):
            pos.append([(x + barWidth) for x in pos[i-1]])
            print(pos)
        _ax = (ax[idx_es] if len(experimental_sets) > 1 else ax)

        for i in range(len(concepts)):
            val = [format_float(scores['sign_count'][i]) for layer, scores in tcav_scores[concepts_key].items()]
            _ax.bar(pos[i], val, width=barWidth, edgecolor='white', label=concepts[i].name)

        _ax.set_xlabel('Set {}'.format(str(idx_es)), fontweight='bold', fontsize=16)
        _ax.set_xticks([r + 0.3 * barWidth for r in range(len(layers))])
        _ax.set_xticklabels(layers, fontsize=12)

        # Create legend & Show graphic
        _ax.legend(fontsize=12)
    plt.show()

plot_tcav_scores(experimental_set_rand, tcav_scores_w_random)
# experimental_set_zig_dot = [[Player1_concept, Player2_concept, random_0_concept, random_1_concept]]
experimental_set_zig_dot = [[Player1_concept, Player2_concept]]

tcav_scores_w_zig_dot = mytcav.interpret(inputs=zebra_tensors,
                                         experimental_sets=experimental_set_zig_dot,
                                         target=zebra_ind,
                                         n_steps=5)

plot_tcav_scores(experimental_set_zig_dot, tcav_scores_w_zig_dot)

#
# def final_scores(experimental_sets, tcav_scores):
#     concept_list = {}
#     name_list = []
#     for idx_es, concepts in enumerate(experimental_sets):
#         print(dir(concepts[0]))
#         concepts = experimental_sets[idx_es]
#         concepts_key = concepts_to_str(concepts)
#         pos = [np.arange(len(layers))]
#         print(pos)
#         print(type(pos))
#
#         for i in range(0, len(concepts)):
#             concept_list[str(concepts[i].name)] = 0
#             name_list.append(str(concepts[i].name))
#
#         for i in range(len(concepts)):
#             val = [format_float(scores['sign_count'][i]) for layer, scores in tcav_scores[concepts_key].items()]
#             for j in range(0, len(val)):
#                 if val[j] > 0:
#                     concept_list[name_list[0]] += 1
#
#             print(concept_list)
#             concept_list[name_list[0]] /= (len(pos) - 1)
#             del(name_list[0])
#     #
#     # x = []
#     # y = []
#     #
#     # for i in range(0, len(concept_list)):
#     #     x =
#     #     y =
#     #     matplotlib.bar(x[i], y[i])
#     #
#
#     print(concept_list)
#     plt.show()
#
# final_scores(experimental_set_zig_dot, tcav_scores_w_zig_dot)