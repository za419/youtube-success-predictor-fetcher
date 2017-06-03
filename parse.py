import json, csv
import datetime
from sets import Set

with open('output.json') as json_data:
    d = json.load(json_data, strict=False)
    with open('data.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
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
        header.append("video_tags")
        header.append("avg_comment_count")
        header.append("avg_view_count")
        header.append("avg_favorite_count")
        header.append("avg_like_count")
        header.append("avg_dislike_count")
        header.append("avg_video_duration")
        header.append("avg_title_length")
        header.append("avg_description_length")
        header.append("avg_posting_time")
        header.append("sd/hd_ratio")
        header.append("projection_ratio")
        header.append("caption_ratio")
        header.append("licensed_content_ratio")
        header.append("3d/2d_ratio")
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
            sd = 0
            hd = 0
            _360 = 0
            rectangular = 0
            caption_true = 0
            caption_false = 0
            total_duration = datetime.timedelta();
            licensed_true = 0
            licensed_false = 0
            threeD = 0
            twoD = 0
            total_title_length = 0
            total_description_length = 0
            v_tags = Set([])
            total_posting_offset = datetime.timedelta() # Posting time encoded as seconds after midnight

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
                    for l in v['snippet']['tags']:
                        v_tags.add(l)
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

                try:
                    try:
                        time=datetime.datetime.strptime(v['contentDetails']['duration'], "PT%MM%SS")
                    except ValueError:
                        try:
                            time=datetime.datetime.strptime(v['contentDetails']['duration'], "PT%HH%MM%SS")
                        except ValueError:
                            try:
                                time=datetime.datetime.strptime(v['contentDetails']['duration'], "PT%MM")
                            except ValueError:
                                try:
                                    time=datetime.datetime.strptime(v['contentDetails']['duration'], "PT%SS")
                                except ValueError:
                                    time=datetime.datetime.strptime(v['contentDetails']['duration'], "PT%HH%SS")
                    total_duration += (time-datetime.datetime(time.year, time.month, time.day))
                except KeyError:
                    continue

                try:
                    time=datetime.datetime.strptime(v['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%S.000Z")
                    total_posting_offset += (time-datetime.datetime(time.year, time.month, time.day))
                except KeyError:
                    continue

                try:
                    total_title_length += len(v['snippet']['title'])
                except KeyError:
                    continue

                try:
                    total_description_length += len(v['snippet']['description'])
                except KeyError:
                    continue

                if v['contentDetails']['definition'] == "hd":
                    hd += 1
                elif v['contentDetails']['definition'] == "sd":
                    sd += 1

                if v['contentDetails']['projection'] == 360:
                    _360 += 1
                elif v['contentDetails']['projection'] == "rectangular":
                    rectangular += 1

                if v['contentDetails']['caption'] == "true":
                    caption_true += 1
                elif v['contentDetails']['caption'] == "false":
                    caption_false += 1

                if v['contentDetails']['licensedContent'] == "true":
                    licensed_true += 1
                elif v['contentDetails']['licensedContent'] == "false":
                    licensed_true += 1

                if v['contentDetails']['licensedContent'] == "3d":
                    threeD += 1
                elif v['contentDetails']['licensedContent'] == "2d":
                    twoD += 1

            header.append("+".join(v_topicCat).encode("ascii", "backslashreplace"))
            header.append("+".join(v_rel_topicids).encode("ascii", "backslashreplace"))
            header.append("+".join(v_tags).encode("ascii", "backslashreplace"))
            header.append(float(comment_count)/len(sub['videos']))
            header.append(float(view_count) / len(sub['videos']))
            header.append(float(favorite_count) / len(sub['videos']))
            header.append(float(like_count) / len(sub['videos']))
            header.append(float(dislike_count) / len(sub['videos']))
            header.append((total_duration / len(sub['videos'])).total_seconds())
            header.append(float(total_title_length) / len(sub['videos']))
            header.append(float(total_description_length) / len(sub['videos']))
            header.append((total_posting_offset / len(sub['videos'])).total_seconds())

            try:
                defn_ratio = round(float(sd) / (hd + sd), ndigits=2)
                header.append(defn_ratio)
            except ZeroDivisionError:
                header.append(0.0)

            try:
                proj_ratio = round(float(_360) / (rectangular + _360), ndigits=2)
                header.append(proj_ratio)
            except ZeroDivisionError:
                header.append(0.0)

            try:
                caption_ratio = round(float(caption_true)/(caption_true+caption_false),ndigits=2)
                header.append(caption_ratio)
            except ZeroDivisionError:
                header.append(0.0)

            try:
                licensed_ratio = round(float(licensed_true) / (licensed_true+licensed_false), ndigits=2)
                header.append(licensed_ratio)
            except ZeroDivisionError:
                header.append(0.0)

            try:
                dimension_ratio = round(float(threeD) / (threeD+twoD), ndigits=2)
                header.append(dimension_ratio)
            except ZeroDivisionError:
                header.append(0.0)

            writer.writerow(header)



#just checks to make sure all instances have same number of attributes
with open('data.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter =',')
    for row in reader:
        print len(row)

