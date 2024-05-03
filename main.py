'''Parse file data and return a list of dictionaries.
First row contains a number of columns, and the rest of the rows contain data:
- L or P in the first column indicates landscape or portrait orientation
- The second column contains a number of tags
- The rest of the columns contain the tags

@param file: path to the file
@return: a tuple containing the number of columns and a list of dictionaries'''
def parse_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    n = int(lines[0])
    data = []
    i = 0
    for line in lines[1:]:
        line = line.strip().split()
        orientation = line[0]
        tags = set(line[2:])
        data.append({'orientation': orientation, 'tags': tags, 'index': i})
        i += 1
    return n, data


def pick_dataset(data_dir='data'):
    import argparse
    import os
    parser = argparse.ArgumentParser(description="Pick a dataset")
    parser.add_argument("file", type=str, help="The name of the file")
    parser.add_argument("--data_dir", type=str, default=data_dir, help="The path to the data directory")
    args = parser.parse_args()
    return args.file, os.path.join(args.data_dir, args.file)


# hash for set
def hash_set(s):
    return hash(frozenset(s))


# LRS function
#lrs_memorized = dict()
def lrs(frame_1, frame_2):
    #if lrs_memorized.get((hash_set(frame_1['tags']), hash_set(frame_2['tags']))):
    #    return lrs_memorized[(hash_set(frame_1['tags']), hash_set(frame_2['tags']))]
    min_num = min(frame_1['tags_len'], frame_2['tags_len'])
    common_tags = frame_1['tags'] & frame_2['tags']
    common_tags_len = len(common_tags)
    # memoization
    #lrs_memorized[(hash_set(frame_1['tags']), hash_set(frame_2['tags']))] = result
    return min(common_tags_len, min_num - common_tags_len)


if __name__ == '__main__':
    file, path = pick_dataset()
    n, data = parse_file(path)
    #print(f'number of columns: {n}')
    #print(f'data: {data[:3]}')
    
    for i in range(len(data)):
        data[i]['tags'] = frozenset([hash(tag) for tag in data[i]['tags']])

    # get only portrait orientation
    portraits = [d for d in data if d['orientation'] == 'P']

    # get only landscape orientation
    landscapes = [d for d in data if d['orientation'] == 'L']

    # sort by number of tags
    portraits.sort(key=lambda x: len(x['tags']), reverse=True)
    #print(f'portrait: {portraits[:3]}')


    # make frameglasses for portrait paintings pairs
    # try to pair paintings to maximize the number of tags in the frame
    import progressbar
    pbar = progressbar.ProgressBar(maxval=len(portraits) + 1).start()
    portrait_pairs = []
    while len(portraits) > 1:
        pair = (portraits.pop(0), )
        p2_index = 0
        tags_inter_num = len(pair[0]['tags'] & portraits[p2_index]['tags'])
        for i, p in enumerate(portraits):
            # if len(p.get('tags')) < tags_num * 2:
            #     break
            if len(pair[0]['tags'] & p['tags']) < tags_inter_num:
                #p2 = p
                p2_index = i
                #pair = (pair[0], p2)
                tags_inter_num = len(pair[0]['tags'] & portraits[p2_index]['tags'])
                if tags_inter_num == 0:
                    break
        pair = (pair[0], portraits.pop(p2_index))
        portrait_pairs.append(pair)
        pbar.update(len(portrait_pairs))
    if portraits:
        p1 = portraits.pop()
        p2 = {'index': -1, 'orientation': 'P', 'tags': set()}
        portrait_pairs.append((p1, p2))
    pbar.finish()
        
    #print(f'portrait pairs: {portrait_pairs[:3]}')


    # make frameglasses for portrait paintings pairs
    portrait_frames = [{'index': (pair[0]['index'], pair[1]['index']), 'orientation': 'P', 'tags': pair[0]['tags'].union(pair[1]['tags'])} for pair in portrait_pairs]

    # assemble the final list of frames
    frames = list()
    frames.extend(portrait_frames)
    frames.extend(landscapes)

    # sort by number of tags
    frames.sort(key=lambda x: len(x['tags']), reverse=True)
    #print(f'frames: {frames[:3]}')


    # make all sets of tags as numpy unique arrays
    for frame in frames:
        frame['tags'] = frozenset([tag for tag in frame['tags']])
        frame['tags_len'] = len(frame['tags'])
        # n = 4
        # chuncks = [frozenset(list(frame['tags'])[i:i+n]) for i in range(0, len(frame['tags']), n)]
        # frame['tag_chuncks'] = chuncks

    #print(f'frames: {frames[:3]}')


    #from multiprocessing import Pool
    #from itertools import repeat
    import progressbar
    # order the frames to maximize LRS while traversing the list
    frames_ordered = list()
    pbar = progressbar.ProgressBar(maxval=len(frames)).start()
    frames_ordered.append(frames.pop(0))
    while frames:
        frame_index = 0
        max_lrs = lrs(frames_ordered[-1], frames[frame_index])
        frames_batch_last_index = next((i for i, f in enumerate(frames) if f['tags_len'] <= max_lrs * 2), len(frames) - 1) - 1
        #print(f'frames batch: {frames_batch_last_index}', end='\r')
        #print(f'frames batch: {len(frames_batch)}', end='\r')
        #lrs_list = list(map(lambda f: lrs(frames_ordered[-1], f), frames_batch))
        # with Pool() as p:
        #     chunk_size = 10000
        #     lrs_list = p.starmap(lrs, zip(repeat(frames_ordered[-1]), frames_batch), chunksize=chunk_size)
        i = 0
        while i < frames_batch_last_index:
            lrs_val = lrs(frames_ordered[-1], frames[i])
            if lrs_val > max_lrs:
                max_lrs = lrs_val
                frame_index = i
                frames_batch_last_index = next((j for j, f in enumerate(frames[i:]) if f['tags_len'] <= max_lrs * 2), frames_batch_last_index) - 1
                if max_lrs == frames_ordered[-1]['tags_len'] // 2:
                    break
            else:
                i += 1
        #frame_index = lrs_list.index(max(lrs_list))
        frames_ordered.append(frames.pop(frame_index))
        #print(f'index: {frame_index}', end='\r')
        #print(f'frames ordered: {len(frames_ordered)}', end='\r')
        pbar.update(len(frames_ordered))
    pbar.finish()

    #print(f'frames ordered: {frames_ordered[:3]}')


    # calculate the sum of LRS
    sum_lrs = 0
    for i in range(len(frames_ordered) - 1):
        sum_lrs += lrs(frames_ordered[i], frames_ordered[i + 1])
    #print(f'sum of LRS: {sum_lrs}')


    from time import time

    # write the result to a file
    with open(f'data/output/{file}', 'w') as f:
        f.write(f'{len(frames_ordered)}\n')
        for frame in frames_ordered:
            if frame['orientation'] == 'L':
                f.write(f'{frame["index"]}\n')
            else:
                i1 = frame['index'][0]
                i2 = frame['index'][1]
                if i2 == -1:
                    f.write(f'{i1}\n')
                elif i1 == -1:
                    f.write(f'{i2}\n')
                else:
                    i1, i2 = sorted([i1, i2])
                    f.write(f'{i1} {i2}\n')
    #print('done')

