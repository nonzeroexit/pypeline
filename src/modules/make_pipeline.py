def main(pipeline_file_path):
    lines = []
    print('Making new pipeline.\nUse % before a param so it can be changed when running the pipeline.')
    add_new_step = True
    while add_new_step:
        step_name = input('Step name: ')
        step_command = input('Command: ')
        lines.append(f'{step_name},{step_command}')
        add_new_step = input('Add new step?[y]: ') != 'n'
    with open(pipeline_file_path, 'w', encoding='utf-8') as fhandle:
        fhandle.write(('\n').join(lines))
