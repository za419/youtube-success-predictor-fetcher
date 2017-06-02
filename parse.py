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
        header.append("video_relevant_topic_ids")
        header.append("avg_view_count")
        header.append("avg_comment_count")
        header.append("avg_favorite_count")
        header.append("avg_dislike_count")
        header.append("avg_like_count")
        writer.writerow(header) #attribute names

        for sub in d: #iterating through channels
            header = []
            header.append(sub['topicDetails']['topicIds'])
            header.append(sub['topicDetails']['topicCategories'])
            header.append(sub['statistics']['commentCount'])
            header.append(sub['statistics']['viewCount'])
            header.append(sub['statistics']['videoCount'])
            header.append(sub['statistics']['subscriberCount'])
            header.append(sub['statistics']['hiddenSubscriberCount'])

            v_topicCat = Set([])
            v_rel_topicids = Set([])
            comment_count = 0
            view_count = 0
            favorite_count = 0
            like_count = 0
            dislike_count = 0
            for v in sub['videos']: #iterating through videos of channels, max of 25
                try:
                    for l in v['topicDetails']['topicCategories']:
                        v_topicCat.add(l)
                except KeyError:
                    continue

                try:
                    for l in v['topicDetails']['relevantTopicIds']:
                        v_rel_topicids.add(l)
                except KeyError:
                    continue

                try:
                    comment_count += int(v['statistics']['commentCount'])
                except KeyError:
                    continue

                try:
                    view_count += int(v['statistics']['viewCount'])
                except KeyError:
                    continue

                try:
                    favorite_count += int(v['statistics']['favoriteCount'])
                except KeyError:
                    continue

                try:
                    like_count += int(v['statistics']['likeCount'])
                except KeyError:
                    continue

                try:
                    dislike_count += int(v['statistics']['dislikeCount'])
                except KeyError:
                    continue


            header.append(list(v_topicCat))
            header.append(list(v_rel_topicids))
            header.append(float(comment_count)/len(sub['videos']))
            header.append(float(view_count) / len(sub['videos']))
            header.append(float(favorite_count) / len(sub['videos']))
            header.append(float(like_count) / len(sub['videos']))
            header.append(float(dislike_count) / len(sub['videos']))

            writer.writerow(header)



#just checks to make sure all instances have same number of attributes
with open('data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter =',')
    for row in reader:
        print len(row)

