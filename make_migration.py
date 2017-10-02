"""
Command line script that compares the schema of the database to the current schema of the source code
This script assumes that the database is at least at version 1
"""

import subprocess
import sys
import os
import re

# Variables which hold values of arguments
message = None
repo_dir = 'migrate_repo'
schema_file = 'src/models.py'
model_name = schema_file.replace('.py', '').replace('/', '.').replace('\\', '.') + '.metadata'
to_stdout = False
dry = False

models_dir = '{0}/versions/models'.format(repo_dir)
models_dir_modified = False
# Loop that grabs command line arguments
i = 1
while i < len(sys.argv):
    if sys.argv[i] == '-h' or sys.argv[i] =='--help' or sys.argv[i] == 'help':
        print('Author: Sam Xifaras', 
              '',
              'Usage: python make_upgrade.py [options] MESSAGE',
              'Description: Compares the current database schema to that in the source code', 
              'Note: All paths given as arguments to the command must be relative paths.',
              '',
              'Options:',
              '  -h, --help : Shows this message',
              '  --repo-dir REPO_DIR : Sets the repository to REPO_DIR',
              '  --schema-file SCHEMA_FILE : Changes the schema file to SCHEMA_FILE',
              '  --to-stdout : Prints the update script that is generated to standard output',
              '  --dry : Runs the script and prints normal output but does not modify the filesystem or the database',
              '          This is useful for debugging or making sure the script looks correct (in combinations with --to-stdout)',
              '  --models-dir MODELS_DIR : Specifies the directory where the schemas of previous versions will be saved.',
              '          The script needs to save previous schemas so it can generate migrations that work properly.'
              '',
              'Positional arguments:',
              '  MESSAGE : The short title/description of the upgrade',
              sep='\n')
        exit()
    elif sys.argv[i] == '--repo-dir':
        repo_dir = sys.argv[i + 1]
        if not models_dir_modified:
            models_dir = '{0}/versions/models'.format(repo_dir)
        i += 1
    elif sys.argv[i] == '--schema-file':
        schema_file = sys.argv[i + 1]
        # Update model_name too
        model_name = schema_file.replace('.py', '').replace('/', '.').replace('\\', '.') + '.metadata'
        i += 1
    elif sys.argv[i] == '--to-stdout': # prints the script that is generated to stdout
        to_stdout = True
    elif sys.argv[i] == '--dry': # Shows all normal output but does not actually create an upgrade script
        dry = True
    elif sys.argv[i] =='--models-dir':
        models_dir = sys.argv[i + 1]
        models_dir_modified = True
        i += 1
    elif sys.argv[i].startswith('-'):
        print('ERROR: Unknown option {0}'.format(sys.argv[i].strip('-')))
        exit()
    elif message is None:
        message = sys.argv[i]
    else:
        print('ERROR: Too many arguments')
        exit()

    i += 1

# Throw error if positional arguments are missing
if message is None:
    print('ERROR: Missing positional argument: MESSAGE')
    exit()



# Function which loops through versions directory, getting migration script with highest version number, which represents the current schema of the database
def get_most_recent_script():
    files = os.listdir('{0}/versions'.format(repo_dir))
    upgrade_scripts = {}
    for file in files:
        match = re.match(r'([0-9]+)(.*)\.py', file)
        if match is not None:
            upgrade_scripts[int(match.group(1))] = ''.join(match.group(1, 2))

    selected_file = upgrade_scripts[max(upgrade_scripts.keys())]
    return selected_file

previous_script = get_most_recent_script()
previous_version_num = re.match(r'([0-9]+).*', previous_script).group(1)

# Create the script using manage.py
script_process = subprocess.run(['python', 'manage.py', 'make_update_script_for_model', 
                                 '--oldmodel={0}.model{1}.metadata'.format(models_dir.replace('/', '.').replace('\\', '.'), previous_version_num), 
                                 '--model={0}'.format(model_name)], stdout=subprocess.PIPE)
script = script_process.stdout

# Print script to standard output
if to_stdout:
    print(script.decode('utf-8'))

if not dry:
    subprocess.run(['python', 'manage.py', 'script', '"{0}"'.format(message)])
    new_script = get_most_recent_script()

    upgrade_script_path = '{0}/versions/{1}.py'.format(repo_dir, new_script)

    print('Writing upgrade script > {0}'.format(upgrade_script_path))
    with open(upgrade_script_path, 'wb') as file:
        file.write(script)

    new_version_num = re.match(r'([0-9]+).*', new_script).group(1)
    with open(schema_file, 'r') as file:
        models_text = file.read()
    
    model_path = '{0}/model{1}.py'.format(models_dir, new_version_num)
    print('Copying current {0} > {1}'.format(schema_file, model_path))
    
    with open(model_path, 'w+') as file:
        file.write(models_text)

    print('\nUpgrade script has been created. Run `python manage.py upgrade` to perform the upgrade.')
    print('To downgrade to a previous version, run `python manage.py downgrade <version>`, then delete the upgrade script that was created in the {0}/versions directory'.format(repo_dir))
else:
    upgrade_script_path = '{0}/versions/{1:03d}{2}.py'.format(repo_dir, int(previous_version_num)+1, '_' + message.replace(' ', '_'))
    print('Writing upgrade script > {0}'.format(upgrade_script_path))
    model_path = '{0}/model{1:03d}.py'.format(models_dir, int(previous_version_num)+1)
    print('Copying current {0} > {1}'.format(schema_file, model_path))

    print('\nUpgrade script has been created. Run `python manage.py upgrade` to perform the upgrade.')
    print('To downgrade to a previous version, run `python manage.py downgrade <version>`, then delete the upgrade script that was created in the {0}/versions directory'.format(repo_dir))
    print('\nDry run complete. No files were modified.')