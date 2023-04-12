offset_val=1570
start="image"
end=".png"
for file in *.png; do
  ignoreimage=${file:5}
  #echo $ignoreimage
  number=${ignoreimage%.*}
  #echo $number
  #echo $end
  #echo "$start$(($number+$offset_val))$end"
  mv "$file" "$start$(($number+$offset_val))$therest"
done
