# Unencapsulated Relationship Tests

These tests focus on demonstrating valid and invalid uses of unencapsulated relationship targets. A relationship target is unencapsulated when the target prim path is outside of the scope of a reference target prim and its descendants. When these sorts of relationships are referenced, the composition engine is unable to resolve and update the prim path of the relationship target because the target no longer exists in the new context. This can happen due to:
1. Bad asset structure with relationships target prims outside of the default prim.
2. Misuse of a reference by targeting a prim that wasn't designed or intended to be a reference target.

When you add a reference with an unencapsulated relationship, you will see an error like this in the console:
```
Warning: in _ReportErrors at line 3157 of W:\257786efc4f464db\USD\pxr\usd\usd\stage.cpp -- In </World/washer.material:binding>: The relationship target </World/Looks/metal> from </World/Geometry/washer.material:binding> in layer @c:/Assets/InternalReferencesTest/washer.usda@ refers to a path outside the scope of the reference from </World/washer>.  Ignoring. (getting targets for relationship </World/washer.material:binding> on stage @c:/Assets/InternalReferencesTest/ExternalReferenceBadTarget.usda@ <000002315659E8F0>)
```
These tests all use the `material:binding` relationship for demonstration since it is a very common property in OpenUSD and often where the illustrated issues will be found, but this applies to all relationships. An added benefit of using material bindings for these tests is that we can visually validate the issue because any unencapsulated binding targets will be discarded and the renderer will show the mesh with no material.

## External reference with a bad target prim (ExternalReferenceBadTargetTest)
The `ExternalReferenceBadTargetTest.usda` stage references a `washer.usda` component asset with a valid asset structure. It defines a default prim, `World`, so that when this layer is referenced using the default prim, it properly brings along its geometry and materials. This test illustrates an issue where an end-user of the asset decided to only reference a specific mesh from the asset and broken the relationship for the bound material on the mesh since the material is not referenced.

## Internal reference with unencapsulated material binding (InternalReferenceTest)
The `InternalReferenceTest.usda` stage is an assembly asset with some prototype component assets defined inline. These prototype assets are then used as internal references and potentially natively instanced as a workflow and performance optimization. This is a useful technique for DCCs that may want to export an assembly asset as a single layer, but still identify component assets within the assembly say a car from a CAD application with fully modeled hardware that is repeated many times with the car asset.

This can get tricky when a developer wants to share one material across multiple component assets (e.g. a copper metal material shared between bolts and washers). One valid, but tedious approach is to bind the shared material after the prototypes have been referenced within the assembly. Another approach would be to create an unencapsulated relationship for the material bindings where the component assets are defined. This is bad, right? Well, as of [USD 23.05 unencapsulated relationships are allowed for internal references](https://github.com/PixarAnimationStudios/OpenUSD/commit/13fa79d1a6dde7c3eaa88378ec7233870c080b34). In this test, we will show the expected results for USD version before pre-23.05 and 23.05+.

### Result: pre-23.05


### Result: 23.05+

## Internal reference with unencapsulated material bindings across sublayers (SublayeredInternalReferenceTest)

### Result: pre-23.05


### Result: 23.05+
## Referenced assemblies with unencapsulated internal references (ReferencedAssembliesWithInternalReferencesTest)

### Result: pre-23.05


### Result: 23.05+