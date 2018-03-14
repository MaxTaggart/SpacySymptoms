import pysolr
import spacy

nlp = spacy.load('en')

solr = pysolr.Solr('https://solr.ahmn.healthcatalyst.net/solr/report_core/', timeout=10, verify=False)

impressionNotes = solr.search('presents presented presenting', **{'rows' : 1000000, 'group': 'true', 'group.field' : 'subject_id'})


def processPatientNotes(result_group):
    patient_id = result_group['groupValue']
    symptoms = []
    for result in result_group['doclist']['docs']:
        noteText = result['report_text']
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

groups = impressionNotes['subject_id']['groups']

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
