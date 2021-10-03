# linkerlib

> uipath uiautomation activities sdk link library



## environment

python : 3.6.12

pythonnet : 2.3.0

uipath : community edition, 20.10.7585.27318



## what is purpose ?

as i fascinated on selector system, made linker library based on uipath. this library helps python user to use powerful uipath activities on python runtime. with hope to have better develops on ui automation field, please do not use for bypassing uipath solution license policy



## how to use ?

##### Assembly Linker

​	assembly linker class helps you to load assemblies for using uipath activities (Community Edition, Version=20.10.7585.27318), and it could be using without uipath installation. thus, this class requires pythonnet library for loading external module on your python process. also, you can look around reference files with below variables

​	- \_\_dll_dir\_\_ : dll files stored directory variable

​	- \_\_nupkg_dir\_\_ : nuget packages stored directory variable

for more information about pythonnet, document page - https://pypi.org/project/pythonnet/



##### Activity Linker

​	before explaining activity linker class, the uipath developers use uipath activities by drag & drop within studio that are actually come from activity namespaces like "UiPath.Core.Activities.dll" and these are designed for microsoft's windows workflow foundation (wf) that means the method following wf model cannot be using by itself, these should require workflow invoke method ("workflow invoker" invokes "activity instance"). so this activity linker class helps develepers to use these methods little bit easier

for more information about microsoft's windows workflow foundation, document page - https://docs.microsoft.com/ko-kr/dotnet/framework/windows-workflow-foundation/



## example code

```python
import linker

if __name__ == '__main__':
    # load assemblies on runtime
    assembly_linker = linker.AssemblyLinker(linker.__dll_dir__)
    assembly_linker.walk_assemblies_directory()

    # import external module on linker scope
    assembly_linker.import_external_module('System')
    assembly_linker.import_external_module('UiPath')

    # initalize activity linker & set default workflow invoker
    activity_linker = linker.ActivityLinker()
    activity_linker.set_invoker(linker.System.Activities.WorkflowInvoker)

    # set explore selector
    selector = '''
    <wnd app='explorer.exe' cls='CabinetWClass' title='*' />  
    <wnd cls='ToolbarWindow32' title='주소: *' />
    '''

    # uipath acitivity settings (Click)
    activity_linker.set_instance(linker.UiPath.Core.Activities.Click)

    activity_linker.set_argument(('Target','Selector',), linker.System.String(selector))
    activity_linker.set_argument(('ContinueOnError',), linker.System.Boolean(True))

    # do uipath activity
    activity_linker.do_instance()

    # uipath acitivity settings (GetAttribute)
    activity_linker.set_instance(linker.UiPath.Core.Activities.GetAttribute)

    activity_linker.set_argument(('Target','Selector',), linker.System.String(selector))
    activity_linker.set_argument(('Attribute',), linker.System.String('AppPath'))
    activity_linker.set_argument(('ContinueOnError',), linker.System.Boolean(True))

    # do uipath activity
    out_argument = activity_linker.do_instance()
    print(out_argument['Result'])
```

