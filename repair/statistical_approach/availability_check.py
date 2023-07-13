
import jpype
import os
def java_version():
    """
    Get the version of the Java Virtual Machine.

    Returns
    -------
    str
        The version of the JVM.
    """
    return jpype.JVM_VERSION