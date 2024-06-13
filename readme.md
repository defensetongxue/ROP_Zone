# ROP Zone
[官中版](./说明.md)

This is the official repository for the ROP zone section of `ROP-Marker: an evidence-oriented AI assistant for ROP diagnosis`. This method mainly involves modeling the retina and calculating the angles between the lesion and the optic disc. Optic location and lesion segmentation are prerequisite tasks for this task. Please refer to the [optic disc location repository](https://github.com/defensetongxue/optic_disc_location) and the [ridge segmentation repository](https://github.com/defensetongxue/ridge_segmentation) respectively.

The main challenge of this method lies in the modeling process, but the code might not fully reflect this process (it directly applies the conclusions of related analyses). For the analysis process of the method, please refer to the original paper.

`estimate_angle.py` is the core part of this repository, responsible for sampling lesions and calculating angles.

`get_best_ab.py` uses exhaustive search to find the appropriate compensation angles for near and far distances, and the boundaries for zones 1, 2, and 3.

`visual.py` provides a visualization scheme, and the results can be referenced in the images from the original paper.
