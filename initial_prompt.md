I want to make a make an app using the library provided, fastHTML, that allows you to upscale an image.

Spec:
- Darkmode, clean, high quality asthetic
- title at the top with the text AuraSR Upscaler
- An input bar near the top where you can select an image from your computer on the left and on the right once you have selected an image there should be a submit button. The submit button should be greyed out until you have selected an image
- The image selected from your computer should appear below the input bar, with width at most half of the screen or height all the way to the bottom of the screen (but no lower, the user should not need to scroll), which ever is smaller.
- There should be a loading spinner displayed over the uploaded image while the image is being upscaled
- When the upscaled image is returned, it should be compared to the orginal image. This should be done by using img-comparison-slider javascript library. it should be done in the same spot as where the uploaded image was originally displayed, also no more than half the screen's width 
- There should be a download image button in the middle of the input bar when the upscaled image is returned 


Here is how you call the upscaler model 

from aura_sr import AuraSR 
aura_sr = AuraSR.from_pretrained("fal/AuraSR-v2") 
# image should be a PIL Image 
upscaled_image = aura_sr.upscale_4x_overlapped(image)

