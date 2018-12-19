import os, math, numpy as np, cv2
from pylut import LUT as lut


def generate_texture():
	# generate colors from (0,0,0) to (255,255,255), step 4
    step = 4
    gradients = int(256 / step) + 1
    lattice = []
    for b in range(0, gradients):
        for g in range(0, gradients):
            for r in range(0, gradients):
                blue = b * step if b < 64 else 255
                green = g * step if g < 64 else 255
                red = r * step if r < 64 else 255
                lattice.append((blue, green, red))  # channel order is BGR

    # because of possible jpeg compression, multiple blocks with gradation has to be made
    # furthurmore, each block will need to have a margin around
    # to avoid color corruption between abrupt color changes
    margin = 10
    blocksize = 65 + 2 * margin
    height = blocksize * 5
    width = blocksize * 13
    img = np.zeros((height, width, 3), np.int16)
    for y in range(0, img.shape[0]):
        for x in range(0, img.shape[1]):
            # make grids of r by g
            blockx = math.floor(x / blocksize)  # 13 blocks in a row
            blocky = math.floor(y / blocksize)  # 5 blocks in a column
            residual_x = x % blocksize - margin
            if residual_x < 0:
                residual_x = 0
            elif residual_x > 64:
                residual_x = 64
            residual_y = y % blocksize - margin
            if residual_y < 0:
                residual_y = 0
            elif residual_y > 64:
                residual_y = 64
            count = blockx * 4225 + blocky * 4225 * 13 + residual_y * 65 + residual_x
            color = lattice[count]
            for z in range(0, 3):
                img[y, x, z] = color[z]  # channel order is BGR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    cv2.imwrite('texture.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 100])


def process_color(color):
    new = [1, 1, 1]
    new[0] = "{:.6f}".format(color[2] / 255)
    new[1] = "{:.6f}".format(color[1] / 255)
    new[2] = "{:.6f}".format(color[0] / 255)
    return new


def lut_from_texture(file):
    filename = os.path.basename(file)
    lutstring = list()
    img = cv2.imread(file, 1)  # channel order is BGR
    img = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
    if np.array(img).shape != (425, 1105, 3):
        print('Invalid texture image: ' + filename + " , process skipped.")
        return
    for i in range(0, 65):  # for each of 65 blocks
        posx = i % 13
        posy = math.floor(i / 13)
        startx = posx * 85
        starty = posy * 85
        block = img[starty:(starty + 84), startx:(startx + 84), :]
        core = block[10:75, 10:75, :]

        # read core area
        for y in range(0, 65):
            for x in range(0, 65):
                lutstring.append(process_color(core[y, x, :]))

    file = file[:-4]
    with open(file + '.cube', 'w') as outfile:
        outfile.write('TITLE "' + file + '"\n\n')
        outfile.write('LUT_3D_SIZE 65\n\n')
        for l in lutstring:
            for e in l:
                outfile.write(str(e) + ' ')
            outfile.write('\n')

    # resize to 32 cubesize and smooth, using modul pylut
    resize = lut.FromCubeFile(file + '.cube')
    resized = lut.Resize(resize, 32)
    resized.ToCubeFile(file + '.cube')
    print(filename, 'processed.')


# batch process
def batch_img2lut(targetdir):
    files = os.listdir(targetdir)
    for f in files:
        if os.path.splitext(f)[1].lower() == '.jpg':
            abspath = os.path.join(targetdir, f)
            lut_from_texture(abspath)