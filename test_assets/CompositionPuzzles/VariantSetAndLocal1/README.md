# VariantSet with Local opinion

![problem](images/Slide56.PNG)

Here, an Onmiverse user has authored a layer with a direct opinion and a VariantSet on the same prim. He is confused about why the opinion from the VariantSet was not showing up in Create, even though he verified that the "small" variant was selected. Can you spot what's going wrong? Let's evaluate LIVRPS to find out!

![livrps step 1](images/Slide57.PNG)

There is only a single layer in this LayerStack. So we start by checking for any Local opinions.

![livrps step 2](images/Slide58.PNG)

There is a Local opinion, so it is added as the strongest opinion in the prim spec and property spec stacks.

![livrps step 2](images/Slide59.PNG)

Are there any opinions from Inherits? No.

![livrps step 3](images/Slide60.PNG)

Are there any opinions form VariantSets?

![livrps step 4](images/Slide61.PNG)

Yes! A VariantSet is contributing an opinion. So that is added
to the prim spec and property spec stacks.

![livrps step 5](images/Slide62.PNG)

Are there any opinions from References, Payloads, or Specializes?
No, no, and no.

![livrps step 6](images/Slide63.PNG)

Our stage is composed! Even though this is a layer stack of a single layer, LIVRPS still applies. The fact that the VariantSet data is arranged before the direct opinion on the Sphere prim in the text of the `puzzle_1.usda` file is irrelevant - the only thing that matters is the composition strategy, and within a layer stack, Local opinions are always stronger than opinions authored through a VariantSet.
