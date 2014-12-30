
import sys
import os
import numpy
from PIL import Image


def MergeImages(img1, img2, min=True):
  assert img1.size == img2.size
  a1 = numpy.asarray(img1)
  a2 = numpy.asarray(img2)
  if min:
    ao = numpy.minimum(a1, a2)
  else:
    ao = numpy.maximum(a1, a2)
  return Image.fromarray(a0, mode=img1.mode)


def Main():
  print '*** Super Timelapse Merge Script ***'
  
  dir_path = sys.argv[1]
  filenames = os.listdir(dir_path)
  filenames.sort()
  
  out_dir = sys.argv[2]
  os.makedirs(out_dir)
  
  history_img = None
  c = 0
  
  for fname in filenames:
    fpath = os.path.join(dir_path, fname)
    print 'Processing %s (%d / %d)' % (fpath, c + 1, len(filenames))
    if history_img is None:
      img_out = Image.open(fpath)
    else:
      img_new = Image.open(fpath)
      img_out = MergeImages(history_img, img_new)
    
    img_out.save(os.path.join(out_dir, 'output%05d.jpg' % c),
                 'JPEG', quality=97)
    history_img = img_out
    c += 1

  print 'DONE.'

if __name__ == '__main__':
    Main()
