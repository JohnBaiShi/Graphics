from ...shared.constants import TEST_PROJECTS_DIR, PATH_UNITY_REVISION, PATH_TEST_RESULTS, PATH_PLAYERS, UTR_INSTALL_URL, UNITY_DOWNLOADER_CLI_URL, get_unity_downloader_cli_cmd, get_timeout
from ruamel.yaml.scalarstring import PreservedScalarString as pss
from ...shared.utr_utils import utr_editmode_flags, utr_playmode_flags, utr_standalone_split_flags,utr_standalone_not_split_flags, utr_standalone_build_flags


def _cmd_base(project_folder, components):
    return [    ]


def cmd_editmode(project_folder, platform, api, test_platform, editor, scripting_backend, color_space):    
    utr_args = utr_editmode_flags( testproject=f'{TEST_PROJECTS_DIR}\{project_folder}',editor_location='WindowsEditor', scripting_backend=f'{scripting_backend}', color_space=f'{color_space}')
    utr_args.extend(test_platform["extra_utr_flags"])
    utr_args.extend(platform["extra_utr_flags"])
    if test_platform["name"].lower()=='playmode_perf_build':
        utr_args.append('--platform=Android')

    base = [ 
        f'curl -s {UTR_INSTALL_URL}.bat --output utr.bat',
        f'pip install unity-downloader-cli --index-url {UNITY_DOWNLOADER_CLI_URL} --upgrade',
        f'unity-downloader-cli { get_unity_downloader_cli_cmd(editor, platform["os"]) } -p WindowsEditor {"".join([f"-c {c} " for c in platform["components"]])} --wait --published-only',
        f'%ANDROID_SDK_ROOT%\platform-tools\\adb.exe connect %BOKKEN_DEVICE_IP%',
        f'powershell %ANDROID_SDK_ROOT%\platform-tools\\adb.exe devices',
        f'NetSh Advfirewall set allprofiles state off',
        pss(f'''
        set ANDROID_DEVICE_CONNECTION=%BOKKEN_DEVICE_IP%
        utr {" ".join(utr_args)}'''),
        f'start %ANDROID_SDK_ROOT%\platform-tools\\adb.exe kill-server'
        ]
    
    extra_cmds = extra_perf_cmd(project_folder)
    unity_config = install_unity_config(project_folder)
    extra_cmds = extra_cmds + unity_config
    if project_folder.lower() == "BoatAttack".lower():
        x=0
        for y in extra_cmds:
            base.insert(x, y)
            x += 1
    return base


def cmd_playmode(project_folder, platform, api, test_platform, editor, scripting_backend, color_space):
    utr_args = utr_playmode_flags(testproject=f'{TEST_PROJECTS_DIR}\{project_folder}',editor_location='WindowsEditor', scripting_backend=f'{scripting_backend}', color_space=f'{color_space}')
    utr_args.extend(test_platform["extra_utr_flags"])
    utr_args.extend(platform["extra_utr_flags"])
    if test_platform["name"].lower()=='playmode_perf_build':
        utr_args.append('--platform=Android')

    base = [ 
        f'curl -s {UTR_INSTALL_URL}.bat --output utr.bat',
        f'pip install unity-downloader-cli --index-url {UNITY_DOWNLOADER_CLI_URL} --upgrade',
        f'unity-downloader-cli { get_unity_downloader_cli_cmd(editor, platform["os"]) } -p WindowsEditor {"".join([f"-c {c} " for c in platform["components"]])} --wait --published-only',
        f'%ANDROID_SDK_ROOT%\platform-tools\\adb.exe connect %BOKKEN_DEVICE_IP%',
        f'powershell %ANDROID_SDK_ROOT%\platform-tools\\adb.exe devices',
        f'NetSh Advfirewall set allprofiles state off',
        pss(f'''
        set ANDROID_DEVICE_CONNECTION=%BOKKEN_DEVICE_IP%
        utr {" ".join(utr_args)}'''),
        f'start %ANDROID_SDK_ROOT%\platform-tools\\adb.exe kill-server'
        ]
    
    extra_cmds = extra_perf_cmd(project_folder)
    unity_config = install_unity_config(project_folder)
    extra_cmds = extra_cmds + unity_config
    if project_folder.lower() == "BoatAttack".lower():
        x=0
        for y in extra_cmds:
            base.insert(x, y)
            x += 1
    return base

def cmd_standalone(project_folder, platform, api, test_platform, editor, scripting_backend, color_space):   
    utr_args = utr_standalone_split_flags(platform_spec='', platform='Android', testproject=f'{TEST_PROJECTS_DIR}\{project_folder}', player_load_path=PATH_PLAYERS, player_conn_ip=None, scripting_backend=f'{scripting_backend}', color_space=f'{color_space}')
    utr_args.extend(test_platform["extra_utr_flags"])
    utr_args.extend(platform["extra_utr_flags"])
    utr_args.extend(['--scripting-backend=il2cpp', f'--editor-location=WindowsEditor'])
    utr_args.append(f'--timeout={get_timeout(test_platform, "Android")}')


    return [ 
        f'curl -s {UTR_INSTALL_URL}.bat --output utr.bat',
        f'%ANDROID_SDK_ROOT%\platform-tools\\adb.exe connect %BOKKEN_DEVICE_IP%',
        f'powershell %ANDROID_SDK_ROOT%\platform-tools\\adb.exe devices',
        f'NetSh Advfirewall set allprofiles state off',
        pss(f'''
        set ANDROID_DEVICE_CONNECTION=%BOKKEN_DEVICE_IP%
        utr {" ".join(utr_args)}'''),
        f'start %ANDROID_SDK_ROOT%\platform-tools\\adb.exe kill-server'
        ]

        
def cmd_standalone_build(project_folder, platform, api, test_platform, editor, scripting_backend, color_space):

    utr_args = utr_standalone_build_flags(platform_spec='', platform='Android', testproject=f'{TEST_PROJECTS_DIR}\\{project_folder}', player_save_path=PATH_PLAYERS, editor_location='WindowsEditor', scripting_backend=f'{scripting_backend}', color_space=f'{color_space}')
    utr_args.extend(test_platform["extra_utr_flags_build"])
    utr_args.extend(platform["extra_utr_flags_build"])
    utr_args.extend(['--scripting-backend=il2cpp'])
    utr_args.append(f'--timeout={get_timeout(test_platform, "Android", build=True)}')


    if api["name"].lower() =='vulkan':
        utr_args.extend(['--extra-editor-arg="-executemethod"', f'--extra-editor-arg="SetupProject.ApplySettings"','--extra-editor-arg="vulkan"'])

    return [  
        f'curl -s {UTR_INSTALL_URL}.bat --output utr.bat',
        f'pip install unity-downloader-cli --index-url {UNITY_DOWNLOADER_CLI_URL} --upgrade',
        f'unity-downloader-cli { get_unity_downloader_cli_cmd(editor, platform["os"]) } -p WindowsEditor {"".join([f"-c {c} " for c in platform["components"]])} --wait --published-only',
        f'mklink /d WindowsEditor\Data\PlaybackEngines\AndroidPlayer\OpenJDK %JAVA_HOME% || exit 0',
        f'mklink /d WindowsEditor\Data\PlaybackEngines\AndroidPlayer\SDK %ANDROID_SDK_ROOT% || exit 0',
        f'mklink /d WindowsEditor\Data\PlaybackEngines\AndroidPlayer\\NDK %ANDROID_NDK_ROOT% || exit 0',
        f'utr {" ".join(utr_args)}'
        ]

def extra_perf_cmd(project_folder):   
    perf_list = [
        f'git clone https://github.com/Unity-Technologies/BoatAttack.git -b feature/benchmark TestProjects/{project_folder}',
        f'Xcopy /E /I \"com.unity.render-pipelines.core\" \"{TEST_PROJECTS_DIR}/{project_folder}/Packages/com.unity.render-pipelines.core\" /Y',
        f'Xcopy /E /I \"com.unity.render-pipelines.universal\" \"{TEST_PROJECTS_DIR}/{project_folder}/Packages/com.unity.render-pipelines.universal\" /Y',
        f'Xcopy /E /I \"com.unity.shadergraph\" \"{TEST_PROJECTS_DIR}/{project_folder}/Packages/com.unity.shadergraph\" /Y'
        ]
    return perf_list

def install_unity_config(project_folder):
    cmds = [
        f'choco source add -n Unity -s https://artifactory.prd.it.unity3d.com/artifactory/api/nuget/unity-choco-local',
        f'choco install unity-config',
		#f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project remove dependency com.unity.render-pipelines.universal',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.addressables@1.15.2-preview.200901 --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.test-framework.performance@2.3.1-preview --project-path .',
		f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.test-framework.utp-reporter@1.0.2-preview --project-path .',
		f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.test-framework.build@0.0.1-preview.12 --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.test.performance.runtimesettings@0.2.0-preview --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.test.metadata-manager@0.1.1-preview --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.cli-project-setup@0.3.2-preview --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency \"com.unity.testing.graphics-performance@ssh://git@github.cds.internal.unity3d.com/unity/com.unity.testing.graphics-performance.git\"  --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.shaderanalysis@0.1.0-preview --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency \"unity.graphictests.performance.universal@ssh://git@github.cds.internal.unity3d.com/unity/unity.graphictests.performance.universal.git\" --project-path .',
		f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add dependency com.unity.test-framework@1.2.1-preview.1 --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add testable com.unity.testing.graphics-performance --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add testable com.unity.cli-project-setup  --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add testable com.unity.test.performance.runtimesettings  --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add testable test.metadata-manager  --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project add testable unity.graphictests.performance.universal  --project-path .',
        f'cd {TEST_PROJECTS_DIR}/{project_folder} && unity-config project set enable-lock-file true --project-path .'
    ]
    return cmds