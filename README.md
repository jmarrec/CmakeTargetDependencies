# CmakeTargetDependencies

Test bed for add_custom_command / add_custom_target dependency chain.

I don't understand why you need both a file-level dependency and a target-level dependency when you use add_custom_command and add_custom_target here: https://github.com/jmarrec/CmakeTargetDependencies/blob/206e425fc3566765c97fcc0aec391710d4dafce9/src/EnergyPlus/CMakeLists.txt#L26-L27

