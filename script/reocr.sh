#!/bin/bash

path="/Users/DXY/Documents/Project/image/*"
files=$(ls $path)
model_name="/Users/DXY/Documents/Project/Kraken.mlmodel"
for image_name in $files
do
   text_name=${image_name/image/text}
   text_name=${text_name%.jpg}.txt
   kraken -i $image_name $text_name binarize segment ocr -m $model_name
done
