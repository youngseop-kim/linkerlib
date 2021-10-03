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