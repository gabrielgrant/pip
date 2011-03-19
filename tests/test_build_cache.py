from glob import fnmatch
import textwrap
from test_pip import reset_env, run_pip, write_file, assert_all_changes
from path import Path

def test_build_cache():
    """
    It should cache a build if requested, then install from that cache.
    """

    # Install INITools, explicitly caching the build 
    env = reset_env()
    cachedir = env.scratch_path/'build_cache'
    result = result = run_pip('install', '--build-cache', cachedir,
                     '--cache-build', 'INITools')
    assert_all_changes({}, result, [env.scratch/'build_cache',
                                    env.venv, env.scratch])

    # Monkey with the cached initools install so it's easy to verify that it
    # was used in the upcoming install.
    initools_dir = cachedir.glob("**/setup.py")[0].folder/'initools'
    assert initools_dir.exists, "couldn't find %r" %(initools_dir, )
    verification_filename = 'installed_from_cache.py'
    with open(initools_dir/verification_filename, 'w') as f:
        f.write('# from build cache')

    # Uninstall and re-install INITools
    uninstall_result = run_pip('uninstall', '-y', 'INITools')
    result = run_pip('install', '--build-cache', cachedir, 'INITools')

    # Verify that the newly installed initools was installed from the cache
    assert_all_changes(uninstall_result, result,
                       [env.venv/'initools'/verification_filename,
                        env.venv, env.scratch])
