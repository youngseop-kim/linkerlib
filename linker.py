import os
import clr
from typing import Any, AnyStr, Tuple, Dict, Union, NoReturn, TypeVar

'''
WHAT IS PURPOSE OF LINKER LIBRARY ?
as i fascinated on selector system, made linker library based on uipath
this library helps python user to use powerful uipath activities on python runtime
with hope to have better develops on ui automation field,
please do not use for bypassing uipath solution license policy
KIM, YS
'''

__base_dir__ = os.path.dirname(os.path.abspath(__file__))
__dll_dir__ = os.sep.join((__base_dir__, 'dll',))
__nupkg_dir__ = os.sep.join((__base_dir__, 'nupkg',))

class AssemblyLinker(object):
    '''
    WHAT IS LINKER.ASSEMBLYLINKER ?
    assembly linker class helps you to load assemblies 
    for using uipath activities (Community Edition, Version=20.10.7585.27318),
    and it could be using without uipath installation
    thus, this class requires pythonnet library
    for loading external module on your python process
    
    # for more information about pythonnet,
    # document page - https://pypi.org/project/pythonnet/

    also, you can look around reference files with below variables
        1. __dll_dir__ : dll files stored directory variable
        2. __nupkg_dir__ : nuget packages stored directory variable
    '''
    def __init__(self, assemblies_directory:AnyStr):
        self.__assemblies_directory = assemblies_directory 
        self.__loaded_assemblies = {}

    @property
    def assemblies_directory(self) -> AnyStr:
        '''
        > return assemblies directory for uipath
        you could load assemblies with your own build
        or additional uipath nuget packages 
        by class initialize argument
        '''
        return self.__assemblies_directory

    @property
    def loaded_assemblies(self) -> Dict[AnyStr, Tuple[bool, AnyStr]]:
        '''
        > return runtime-loaded assembly list
        key is for assembly file name,
        value is for "is assembly file loaded" & "failure reason"
        '''
        return self.__loaded_assemblies

    def walk_assemblies_directory(self) -> Dict[AnyStr, Tuple]:
        '''
        > return property "loaded_assemblies"
        this method loads all assemblies that is located in assemblies directory
        and of course, it should be used first before
        using method "import_external_module(module_name)" 
        '''
        root = os.walk(self.__assemblies_directory)
        for packed in root:
            directory, _, files = packed
            main_key = os.path.basename(directory)

            for file_ in files:
                fname, fext = os.path.splitext(file_)
                assembly_directory = os.sep.join((directory, file_,))

                if fext == '.dll':
                    self.__loaded_assemblies[fname] = self.set_assembly(assembly_directory)
        
        return self.loaded_assemblies

    def set_assembly(self, assembly_directory:AnyStr) -> Tuple:
        '''
        > return "is assembly file loaded" & "failure reason"
        this method adds reference on clr module
        '''
        try:
            clr.AddReference(assembly_directory)
            return (True, 'No exception',)

        except Exception as assembly_error:
            return (False, assembly_error,)

    def import_external_module(self, module_name:AnyStr) -> bool:
        '''
        > return "is module in global scope" 
        this method imports external module on linker libraray scope,
        not on your script scope! 
        '''
        globals()[module_name] = __import__(module_name)
        return module_name in globals()

class ActivityLinker(object):
    '''
    WHAT IS LINKER.ACTIVITYLINKER ?
    before explaining activity linker class,
    the uipath developers use uipath activities by drag & drop within studio
    that are actually come from activity namespaces like "UiPath.Core.Activities.dll"
    and these are designed for microsoft's windows workflow foundation (wf)
    that means the method following wf model cannot be using by itself, 
    these should require workflow invoke method ("workflow invoker" invokes "activity instance")
    so this activity linker class helps develepers to use these methods little bit easier

    # for more information about microsoft's windows workflow foundation,
    # document page - https://docs.microsoft.com/ko-kr/dotnet/framework/windows-workflow-foundation/ 
    '''

    DIRECTION_IN = 0
    DIRECTION_OUT = 1

    def __init__(self):
        if 'System' not in globals():
            raise ModuleNotFoundError

        if 'UiPath' not in globals():
            raise ModuleNotFoundError

        self.__invoker__ = None
        self.__instance__ = None

    def _create_argument_variable(self, direction:int, value:Any)\
        -> Union[TypeVar('System.Activities.InArgument'), TypeVar('System.Activities.OutArgument')]:
        '''
        > return "InArgument" / "OutArgument" class wrapped variable
        due to pythonnet library's access way,
        you cannot pass variable that is not wrapped in 
        "InArgument" / "OutArgument" class to activity argument
        thus, this method supports creation of "InArgument" / "OutArgument" variable
        and also be-wrapped variable should be .NET object type
        '''
        if direction == self.__class__.DIRECTION_IN:
            return System.Activities.InArgument[type(value)](value)

        elif direction == self.__class__.DIRECTION_OUT:
            return System.Activities.OutArgument[type(value)](value)

    def set_invoker(self, invoker_class:Any) -> NoReturn:
        '''
        set workflow invoker instance for invoking activity instance
        '''
        self.__invoker__ = invoker_class

    def set_instance(self, activity_class:Any) -> NoReturn:
        '''
        set an activity instance that is invoked by invoker instance
        you could set arguments by just calling "__instance__" variable
        '''
        self.__instance__ = activity_class()

    def set_argument(self, attributes:Tuple[AnyStr], value:Any) -> NoReturn:
        '''
        set input direction argument for invoking activity instance
        '''
        instance_attribute = self.__instance__
        argument_variable = self._create_argument_variable(self.__class__.DIRECTION_IN, value)

        for depth, attribute in enumerate(attributes):
            if depth == len(attributes)-1:
                instance_attribute = setattr(instance_attribute, attribute, argument_variable)
            else:
                instance_attribute = getattr(instance_attribute, attribute)

    def do_instance(self) -> Union[TypeVar('System.Activities.OutArgument'),NoReturn]:
        '''
        > return "OutArgument" class wrapped variable
        when workflow invoker instance invokes activity instance,
        this invoke method returns "OutArgument" variable if activity has return variable
        '''
        out_argument = self.__invoker__.Invoke(self.__instance__)
        return out_argument