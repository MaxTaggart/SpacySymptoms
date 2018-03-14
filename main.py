import pysolr
import spacy

VALIDATED_NOTE_IDS = ["N1581068671", "N1783357151", "N1334801006", "N2007934904", "N1816923311", "N248635744", "N1046395067", "N362491886", "N1782145982", "N340459839", "N1777861561", "N155059731", "N1582524513", "N1988163110", "N1354593088", "N327447579", "N1251729047", "N322921405", "N1306961167", "N1794201407", "N2005601767", "N87692227", "N1947478184", "N1857936100", "N1921623964", "N451876465", "N1979345823", "N1390090281", "N1990370857", "N324522942", "N373662661", "N65871556", "N1947992068", "N1486106366", "N362142103", "N1568191431", "N1907911237", "N1515460358", "N1581068671", "N1783357151", "N1334801006", "N2007934904", "N1816923311", "N248635744", "N1046395067", "N362491886", "N1782145982", "N340459839", "N1777861561", "N155059731", "N1582524513", "N1988163110", "N1354593088", "N327447579", "N1251729047", "N322921405", "N1306961167", "N1794201407", "N2005601767", "N87692227", "N1947478184", "N1857936100", "N1921623964", "N451876465", "N1979345823", "N1390090281", "N1990370857", "N324522942", "N373662661", "N65871556", "N1947992068", "N1486106366", "N362142103", "N1568191431", "N1907911237", "N1515460358", "N1581068671", "N1783357151", "N1334801006", "N2007934904", "N1816923311", "N248635744", "N1046395067", "N362491886", "N1782145982", "N340459839", "N1777861561", "N155059731", "N1582524513", "N1988163110", "N1354593088", "N327447579", "N1251729047", "N322921405", "N1306961167", "N1794201407", "N2005601767", "N87692227", "N1947478184", "N1857936100", "N1921623964", "N451876465", "N1979345823", "N1390090281", "N1990370857", "N324522942", "N373662661", "N65871556", "N1947992068", "N1486106366", "N362142103", "N1568191431", "N1907911237", "N1515460358", "N1581068671", "N1783357151", "N1334801006", "N2007934904", "N1816923311", "N248635744", "N1046395067", "N362491886", "N1782145982", "N340459839", "N1777861561", "N155059731", "N1582524513", "N1988163110", "N1354593088", "N327447579", "N1251729047", "N322921405", "N1306961167", "N1794201407", "N2005601767", "N87692227", "N1947478184", "N1857936100", "N1921623964", "N451876465", "N1979345823", "N1390090281", "N1990370857", "N324522942", "N373662661", "N65871556", "N1947992068", "N1486106366", "N362142103", "N1568191431", "N1907911237", "N1515460358"]
validated_note_query_string = "(" + " ".join(VALIDATED_NOTE_IDS) + ")"

nlp = spacy.load('en')

solr = pysolr.Solr('https://solr.ahmn.healthcatalyst.net/solr/report_core/', timeout=10, verify=False)

impressionNotes = solr.search('presents presented presenting', **{'rows' : 1000000, 'group': 'true', 'group.field' : 'subject_id', 'fq' : 'report_id:{}'.format(validated_note_query_string)})


def processPatientNotes(result_group):
    patient_id = result_group['groupValue']
    symptoms = []
    for result in result_group['doclist']['docs']:
        noteText = result['report_text'][0]
        doc = nlp(noteText)
        for sent in doc.sents:
            for token in sent:
                if token.lemma_ == 'present':
                    for token_inner in sent:
                        if token_inner.text == 'with' and token_inner.head.lemma_ == 'present':
                            phrase_left = token_inner.left_edge.i
                            phrase_right = token_inner.right_edge.i
                            edge_phrase = doc[phrase_left + 1 : phrase_right + 1]
                            symptoms.append(edge_phrase)
                            # symptom_phrase = list(token_inner.subtree)
                            # print(symptom_phrase)
    print("Patient ID: {}\nSymptoms: {}".format(patient_id, symptoms))

groups = impressionNotes.grouped['subject_id']['groups']

for group in groups:
    processPatientNotes(group)


# raw_texts = list(map(lambda x: x['report_text'], impressionNotes))
#
# testTexts = [
#     'The first sentence. The second sentence. The patient presented in May with seizure and weakness, but not any vision change.',
#     'The fifth sentence. The sixth sentence. The patient presented in June with blue hair and ice cream.'
# ]
#
# # docs = nlp(raw_texts)
# doc = nlp('The first sentence. The second sentence. The patient presented in may with seizure and weakness.')
#
# for sent in doc.sents:
#     for token in sent:
#         if token.lemma_ == 'present':
#             for token_inner in sent:
#                 if token_inner.text == 'with' and token_inner.head.lemma_ == 'present':
#                     phrase_left = token_inner.left_edge.i
#                     phrase_right = token_inner.right_edge.i
#                     edge_phrase = doc[phrase_left + 1 : phrase_right + 1]
#                     print(edge_phrase)
#                     symptom_phrase = list(token_inner.subtree)
#                     print(symptom_phrase)
#
#
# # If 'present' has a child preposition 'with' get all the children of 'with'.


# validated notes

