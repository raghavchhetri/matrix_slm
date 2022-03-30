print(f'Invoking __init__.py for {__name__}')

from .target_pattern import target_pattern
from .generate_mask import generate_mask


#Note: Much of the Python documentation states that an __init__.py file must be present in the package directory when creating a package. This was once true. It used to be that the very presence of __init__.py signified to Python that a package was being defined. The file could contain initialization code or even be empty, but it had to be present.

#Starting with Python 3.3, Implicit Namespace Packages were introduced. These allow for the creation of a package without any __init__.py file. Of course, it can still be present if package initialization is needed. But it is no longer required.