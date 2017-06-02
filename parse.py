import json, csv
from sets import Set

with open('output.json') as json_data:
    d = json.load(json_data, strict=False)
    with open('data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        header = []
        header.append("topicIds")
        header.append("topicCategories")
        header.append("commentCount")
        header.append("viewCount")
        header.append("videoCount")
        header.append("subscriberCount")
        header.append("hiddenSubscriberCount")
        header.append("video_topic_cats")
        writer.writerow(header)
        count = 0
        for sub in d:
            count = 0
            header = []
            header.append(sub['topicDetails']['topicIds'])
            header.append(sub['topicDetails']['topicCategories'])
            header.append(sub['statistics']['commentCount'])
            header.append(sub['statistics']['viewCount'])
            header.append(sub['statistics']['videoCount'])
            header.append(sub['statistics']['subscriberCount'])
            header.append(sub['statistics']['hiddenSubscriberCount'])


            v_topicCat = Set([])
            for v in sub['videos']:
                try:
                    for l in v['topicDetails']['topicCategories']:
                        v_topicCat.add(l)
                except KeyError:
                    continue
            header.append(list(v_topicCat))
            writer.writerow(header)

with open('data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter =',')
    for row in reader:
        print len(row)

