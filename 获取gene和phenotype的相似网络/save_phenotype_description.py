import json
import os

def merge_json_folder(folder_path, output_file):
    json_files = [f for f in os.listdir(folder_path) if f.endswith('.json')]

    merge_data = []

    for file in json_files:
        file_path = os.path.join(folder_path,file)
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            merge_data.extend(data)


    print(len(merge_data))
    # 写入文件
    with open(output_file, 'w') as output:
        json.dump(merge_data,output)

    print('json文件合并完成！')



# folder_path = 'phenotype_des'
# output_file = 'merged_des.json'
folder_path = 'phenotype_synon'
output_file = 'merged_syn.json'
# merge_json_folder(folder_path,output_file)


#
