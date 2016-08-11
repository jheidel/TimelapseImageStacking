"""Merges a time lapse sequence into a blended sequence."""
import argparse
import numpy
import os
from PIL import Image
import sys

parser = argparse.ArgumentParser()
parser.add_argument('timelapse_dir', help='Path to directory containing timelapse images.')
parser.add_argument('output_name', help='Directory for output merged sequence. Will be created in timelapse_dir.')
parser.add_argument('--darken', action='store_true', help='Enable darken mode.')
parser.add_argument('--skip', nargs='?', const=1, type=int,
                    help='Use one out of every SKIP images.')
parser.add_argument('--window', nargs='?', const=0, type=int,
                    help='Merge the last N images. 0 to merge all.')
args = parser.parse_args()


def MergeImages(img1, img2, lighten=True):
  assert img1.size == img2.size
  a1 = numpy.asarray(img1)
  a2 = numpy.asarray(img2)
  if lighten:
    ao = numpy.maximum(a1, a2)
  else:
    ao = numpy.minimum(a1, a2)
  return Image.fromarray(ao, mode=img1.mode)


def WindowMerge(filenames):
  def gen_bundles():
    for i in range(0, len(filenames)):
      yield filenames[max(0, i-args.window):i]
  bundles = list(filter(None, gen_bundles()))

  for c, bundle in enumerate(bundles):
    print 'Processing %s (%d / %d)' % (bundle, c + 1, len(bundles))
    history_img = None
    for fname in bundle:
      fpath = os.path.join(args.timelapse_dir, fname)
      if history_img is None:
        img_out = Image.open(fpath)
      else:
        img_new = Image.open(fpath)
        img_out = MergeImages(history_img, img_new, lighten=not args.darken)
      history_img = img_out

    history_img.save(os.path.join(args.timelapse_dir, args.output_name, 'output%05d.jpg' % c),
                     'JPEG', quality=97)


def MergeAll(filenames):
  history_img = None
  for c, fname in enumerate(filenames):
    fpath = os.path.join(args.timelapse_dir, fname)
    print 'Processing %s (%d / %d)' % (fpath, c + 1, len(filenames))
    if history_img is None:
      img_out = Image.open(fpath)
    else:
      img_new = Image.open(fpath)
      img_out = MergeImages(history_img, img_new, lighten=not args.darken)
    
    img_out.save(os.path.join(args.timelapse_dir, args.output_name, 'output%05d.jpg' % c),
                 'JPEG', quality=97)
    history_img = img_out


def Main():
  print '*** Super Timelapse Merge Script ***'
  
  filenames = os.listdir(args.timelapse_dir)
  filenames = filter(lambda x: os.path.isfile(os.path.join(args.timelapse_dir, x)), filenames)
  filenames.sort()
  print 'Found %d files' % len(filenames)

  skip = args.skip or 1
  if skip != 1:
    print 'Filtering list. Using 1 out of every %d images.' % skip
    filenames[:] = filenames[::skip]

  if args.darken:
    print 'Using darken mode.'
    
  os.makedirs(os.path.join(args.timelapse_dir, args.output_name))

  if args.window > 0:
    print 'Using window merge mode.'
    WindowMerge(filenames)
  else:
    MergeAll(filenames)

  print 'DONE.'

if __name__ == '__main__':
    Main()
