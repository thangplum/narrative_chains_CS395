import json
import chains

def parse_test_instance(story):
    """Returns TWO ParsedStory instances representing option 1 and 2"""
    # this is very compressed
    id = story.InputStoryid
    story = list(story)
    sentences = [chains.nlp(sentence) for sentence in story[2:6]]
    alternatives = [story[6], story[7]]
    return [chains.ParsedStory(id, id, chains.nlp(" ".join(story[2:6]+[a])), *(sentences+[chains.nlp(a)])) for a in alternatives]

def story_answer(story):
    """Tells you the correct answer. Return (storyid, index). 1 for the first ending, 2 for the second ending"""
    #obviously you can't use this information until you've chosen your answer!
    return story.InputStoryid, story.AnswerRightEnding

def evaluate(choice1, choice2):

    if len(choice1[0]) != len(choice2[0]):
        pass
    with open("all.json") as fp:
        table = chains.ProbabilityTable(json.load(fp))


# Load training data and build the model
# data, table = chains.process_corpus("train.csv", 100)
#print(table.pmi("move", "nsubj", "move", "nsubj"))

# load the pre-built model
# with open("all.json") as fp:
#     table = chains.ProbabilityTable(json.load(fp))


# load testing data
test = chains.load_data("val.csv")
right_answers = 0
total_answers = 0
for t in test:
    one, two = parse_test_instance(t)
    one_deps = chains.extract_dependency_pairs(one)
    two_deps = chains.extract_dependency_pairs(two)
    if len(one[-1]) != len(two[-1]):
        if len(one[-1]) > len(two[-1]):
            if t.AnswerRightEnding == 1:
                right_answers += 1
        else:
            if t.AnswerRightEnding == 2:
                right_answers += 1
    else:
        total_pmi = 0
        for (dp1, dp2) in zip(one_deps[1][0], two_deps[1][0]):
            with open("all.json") as fp:
                table = chains.ProbabilityTable(json.load(fp))
                total_pmi += table.pmi(dp1[0], dp1[1], dp2[0], dp2[1])
        if total_pmi <= 0:
            total_pmi = 1
        else:
            total_pmi = 2
        if total_pmi == t.AnswerRightEnding:
            right_answers += 1
    total_answers += 1
    print("Total right answer so far", str(right_answers))
    print("Total answer so far", str(total_answers))

percentage = right_answers / total_answers * 100
percentage += '%'
print("The correct percentage:", percentage)

