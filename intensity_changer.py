import numpy as np
from PIL import Image

def get_nearest(sample, targetNum):
    diff = 2 ** 32 - 1  # Very big number.
    currentKey = None
    for i in sample.keys():
        newDiff = abs(int(i) - targetNum)
        if newDiff < diff:
            currentKey = i
            diff = newDiff
    return sample[currentKey]


def read_itf(itf_path):
    itf = Image.open(itf_path).convert("L")
    return itf




def scale(X, x_min=0, x_max=1):
    # nom = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
    nom = (X - x_min) / (X.max() - x_min)
    # nom = (1 - nom)
    # print('normalised =', nom[:])
    return np.multiply(nom, 255)


def calc_itf(itf):
    itf_array = np.where(np.array(itf) == 255, 0, 1)
    itemindex = np.sort(np.where(itf_array == 1))
    data = {}
    # normalise = scale(itemindex[0])

    for i in range(len(itemindex[0])):
        # data[itemindex[1][i]] = normalise[i]
        data[itemindex[1][i]] = float(itemindex[0][i])
        # print(itemindex[1][i], itemindex[0][i])

    return data


def intensity_transformation(image_path, itf_path):
    image = Image.open(image_path)
    base = [image.convert('L')]
    new_base = []
    itf = read_itf(itf_path).convert('L')
    data = calc_itf(itf)
    for color in base:
        color = np.array(color)
        new_color = []
        for col in range(len(color)):
            new_r = []
            for row in range(len(color[0])):
                try:
                    new_r.append(data[color[col][row]])

                except:
                    new_r.append(get_nearest(data, color[col][row]))

                # print(len(color[col]))
            new_color.append(new_r)
        new_base.append(new_color)
    new_base = np.array(new_base)
    # print(rgb)
    print(type(new_base[0]))

    new_image = Image.merge('RGB',
                            (Image.fromarray(new_base[0]).convert('L'), Image.fromarray(new_base[0]).convert('L'),
                             Image.fromarray(new_base[0]).convert('L')))
    new_image.save('output/{}'.format('modifyed_'+itf_path.split('/')[-1].split('.')[0]+'_'+image_path.split('/')[-1]))
    new_image.show()




if __name__ == '__main__':
    intensity_transformation('img/car.png', 'itf/itf2.png')
    intensity_transformation('img/xray.jpg', 'itf/itf3.png')
    intensity_transformation('img/xray.jpg', 'itf/itf4.png')
