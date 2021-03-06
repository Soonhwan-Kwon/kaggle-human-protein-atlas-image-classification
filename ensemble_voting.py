import math

import pandas as pd
from theconf import Config as C

from common import name_label_dict, save_pred
from data import get_dataset

if __name__ == '__main__':
    ensemble_181226 = [
        'resnet34_d0.2_lr0.0001_v2',                    # 0.4649
        'resnet50_d0.2_lr0.0001_v2',                    # 0.4608
        'densenet121_cutout140',                        # 0.4276
        'densenet169_v2_lr0.0001_d0.2',                 # 0.4336
        # 'inception_lr0.0001_v2_reg0.00001_cutout35'   # 0.4794
    ]
    ensemble_181227 = [
        'densenet121_hpa',  # loss=0.4368 f1(0.629@0.01 0.662@0.01 0.680@0.02 0.709@0.05 0.723@0.10 0.739@0.20 0.742@0.30 0.752@0.50 0.754@0.60 0.753@0.70 "0.757"@0.80 0.754@0.90)
        'densenet169_hpa',  # loss=0.4327 f1(0.620@0.01 0.650@0.01 0.677@0.02 0.693@0.05 0.701@0.10 0.716@0.20 0.718@0.30 "0.728"@0.50 0.727@0.60 0.727@0.70 0.722@0.80 0.719@0.90)
        'inception_hpa',    # loss=0.4528 f1(0.655@0.01 0.669@0.01 0.687@0.02 0.716@0.05 0.721@0.10 0.726@0.20 "0.729"@0.30 0.712@0.50 0.709@0.60 0.707@0.70 0.708@0.80 0.705@0.90)
        'resnet34_hpa',     # loss=0.4590 f1(0.639@0.01 0.658@0.01 0.682@0.02 0.689@0.05 0.694@0.10 0.702@0.20 0.707@0.30 0.708@0.50 0.709@0.60 0.710@0.70 "0.711"@0.80 0.700@0.90)
        # 'resnet50_hpa',     # loss=0.4666 f1(0.589@0.01 0.606@0.01 0.619@0.02 0.635@0.05 0.646@0.10 0.656@0.20 0.663@0.30 0.663@0.50 0.664@0.60 "0.664"@0.70 0.663@0.80 0.659@0.90)
        # 'vgg16_hpa_try2',   # loss=0.4659 f1(0.602@0.01 0.612@0.01 0.620@0.02 0.629@0.05 0.645@0.10 0.652@0.20 0.653@0.30 0.659@0.50 0.664@0.60 0.669@0.70 0.669@0.80 "0.675"@0.90)
    ]
    ensemble_181227_2 = ensemble_181227[:-1]

    # ensemble 181228 : +inceptionv4_lr0.0001
    ensemble_181228 = [
        # 0.48144908558097205 0.8693285873717421 [0.7286644501471183, 0.7571138480433932, 0.7803764344801262, 0.8065658440003218, 0.8211493778037718, 0.8347763316033342, 0.8421543584765375, 0.8528350850291943, 0.8566394950483225, 0.8606958186892885, 0.8634412951050635, 0.8693285873717421]
        # 0.4257088624514066 0.7563931221722974 [0.6687331824029713, 0.7000887087117694, 0.7170249675371145, 0.7342908849016757, 0.7431131472895022, 0.7508583166793433, 0.7563931221722974, 0.7556821513449838, 0.7561008349637734, 0.7533586237448494, 0.751350478494259, 0.7476325023446959]
        # f1_best = 0.7788019150173727
        # 0.7695442477076717
        'densenet121_hpa',
        # 0.47052022654314024 0.883564831147545 [0.7627464694600287, 0.7893119927469171, 0.8105534536018242, 0.8319489495243756, 0.8443073609025877, 0.857207575279235, 0.863863215496233, 0.8717448652464224, 0.8743542189729707, 0.8768512090804925, 0.8800744059161048, 0.883564831147545]
        # 0.41962752586755997 0.7673593753940517 [0.6759358828856666, 0.694891578913996, 0.7109333987492683, 0.7248506420001423, 0.7280066341840679, 0.7421194584128399, 0.7516022545403335, 0.7624105124637249, 0.7645276686621482, 0.7671003821123755, 0.7673593753940517, 0.7617924179582866]
        # f1_best= 0.7761037564777157
        # 0.7668825055343866
        'densenet169_hpa',
        # 0.4727695916838591 0.8795792656788672 [0.7628248353272801, 0.786798789733215, 0.8064970335084095, 0.8278627256426968, 0.8400277443695218, 0.8511478997519669, 0.8574925875948934, 0.8673485884712768, 0.8703730845952214, 0.8726489282817946, 0.8761520388901199, 0.8795792656788672]
        # 0.4479030920909001 0.722188447195193 [0.6603354689500212, 0.6781756706240787, 0.6970617977257934, 0.7068099320896729, 0.7137396918565154, 0.716672371152485, 0.7205550817391908, 0.722188447195193, 0.7196673390101791, 0.7183425801814213, 0.7123691008665016, 0.707516674267073]
        # 0.7213300030996928
        'inception_hpa',
        # 0.4999040642336959 0.8371811554080003 [0.6863789867160089, 0.7176828859495333, 0.743081428211204, 0.7704841630165901, 0.7868865529203365, 0.8012075006477748, 0.80951227631265, 0.8194290765127887, 0.8235081724145665, 0.8273043246831974, 0.8320513377767054, 0.8371811554080003]
        # 0.43655064167120516 0.7397710878144628 [0.618103573413701, 0.6420990833405801, 0.6638790573943991, 0.6905911940007078, 0.7082335215352913, 0.7201180500501377, 0.7359422515289147, 0.737509295045373, 0.73677779625502, 0.7397710878144628, 0.738189435110362, 0.7354039329642069]
        # 0.7534582471306929
        # 0.7428748322318268
        'inceptionv4_lr0.0001',
        # 0.4989233031552923 0.8358830729429877 [0.755467158002834, 0.77130183673666, 0.7845672517273364, 0.8000958367796535, 0.8078515126903854, 0.8160262953289789, 0.8197899249768058, 0.8256650971462641, 0.8274022060603471, 0.8295134057482816, 0.8332039001194055, 0.8358830729429877]
        # 0.4504535901240813 0.7234162014384161 [0.6765092487054609, 0.6892159293921468, 0.6956717597608402, 0.7015828117794182, 0.7126844364732333, 0.7166789034589038, 0.7234162014384161, 0.7226045136088662, 0.7217221409012344, 0.7207246760208065, 0.721255303145193, 0.7124682752311414]
        # f1_best= 0.7152717393254319
        # 0.7116274910401094
        'resnet50_hpa',
        # 0.4504535901240813 0.7234162014384161 [0.6765092487054609, 0.6892159293921468, 0.6956717597608402, 0.7015828117794182, 0.7126844364732333, 0.7166789034589038, 0.7234162014384161, 0.7226045136088662, 0.7217221409012344, 0.7207246760208065, 0.721255303145193, 0.7124682752311414]
        # f1_best = 0.7323759248075878
        # 0.7241969229628581
        'resnet34_hpa'
    ]

    ensemble_181229 = [
        'inception_fold0',
        'inception_fold1',
        'inception_fold2',
        'inception_fold3',
        'inception_fold4',
        'inceptionv4_fold0',
        'inceptionv4_fold1',
        'inceptionv4_fold2',
        'inceptionv4_fold3',
        'inceptionv4_fold4',
        'densenet121_fold0',
        'densenet121_fold1',
        'densenet121_fold2',
        'densenet121_fold3',
        'densenet121_fold4',
        'densenet169_fold0',
        'densenet169_fold1',
        'densenet169_fold2',
        'densenet169_fold3',
        'densenet169_fold4'
    ]

    ensemble_190104 = [
        'ensemble_nn3_lr001_try1.csv',
        'ensemble_nn3_lr001_try2.csv',
        'ensemble_nn3_lr001_try3.csv',
        'ensemble_nn3_lr005_try1.csv',
        'ensemble_nn3_lr005_try2.csv',
        'ensemble_nn3_lr005_try3.csv',
    ]

    # ensemble_list = ensemble_181226
    # ensemble_th = 3
    # ensemble_list = ensemble_181227
    # ensemble_th = 2
    # ensemble_list = ensemble_181227_2     # 0.553
    # ensemble_th = 1
    # ensemble_list = ensemble_181228         # 0.598
    # ensemble_th = 2
    # ensemble_list = ensemble_181229[-10:]
    # ensemble_th = 2

    # ensemble_181231 = [           # 0.579
    #     'inceptionv4_fold1',
    #     'inceptionv4_fold3',
    #     'densenet121_fold4',
    #     'densenet169_fold0',
    #     'densenet169_fold2',
    # ]
    # ensemble_list = ensemble_181231
    # ensemble_th = 2
    ensemble_list = ensemble_190104
    ensemble_th = 4

    model_selection = [
        'densenet121_fold0',
        'densenet121_fold3',
        'densenet121_fold4',
        'densenet121_fold2_lr0.0001_bce',

        'densenet169_fold0',
        'densenet169_fold3',
        'densenet169_fold4',
        'densenet169_fold2_lr0.0001_bce',  # <--- best one

        'inceptionv4_fold0',
        'inceptionv4_fold1',
        'inceptionv4_fold3',

        'pnasnet_fold2_lr0.00005',
        'senet_fold0_lr0.00005',

        'nasnet_fold0_lr0.0001_relu_bce',
        'nasnet_fold2_lr0.0001_relu_bce',
    ]
    ensemble_list = model_selection
    ensemble_th = 3

    C.get()['cv_fold'] = 0
    _, _, _, ids_test = get_dataset()

    votes = []
    for _ in range(len(ids_test)):
        vote = [0] * len(name_label_dict)
        votes.append(vote)

    for model_name in ensemble_list:
        if '.csv' in model_name:
            path = 'asset_v3/%s' % model_name
        else:
            path = 'asset_v3/%s.aug.csv' % model_name
        print('load... %s' % path)
        labels = pd.read_csv(path).set_index('Id')
        for idx, s in enumerate(labels['Predicted']):
            if not isinstance(s, str) and math.isnan(s):
                continue
            for pred_idx in [int(i) for i in str(s).split()]:
                votes[idx][pred_idx] += 1

    output = 'asset/ensemble_vote_th%d.csv' % (ensemble_th)
    save_pred(ids_test, votes, th=ensemble_th, fname=output)
    print('done. %s' % output)
