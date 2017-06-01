import json, csv

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
        writer.writerow(header)
        for sub in d:
            header = []
            header.append(sub['topicDetails']['topicIds'])
            header.append(sub['topicDetails']['topicCategories'])
            header.append(sub['statistics']['commentCount'])
            header.append(sub['statistics']['viewCount'])
            header.append(sub['statistics']['videoCount'])
            header.append(sub['statistics']['subscriberCount'])
            header.append(sub['statistics']['hiddenSubscriberCount'])
            writer.writerow(header)
