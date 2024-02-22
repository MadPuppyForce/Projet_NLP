from jiwer import wer,cer
import csv
import numpy as np
import language_tool_python

#load cvs file avec colonne noisy_text et corrected_text
def load_csv_file(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append(row)
    return data




data = load_csv_file('projetNLP_test_data.csv')
noisy_text = []
corrected_text = []
for i in range(len(data)):
    noisy_text.append(data[i]['noisy_text'])
    corrected_text.append(data[i]['corrected_text'])
    gemini = data[i]['gemini_with_context']

tool = language_tool_python.LanguageTool('en-FR')

error_CER_list = list()
error_WER_list = list()
for i in range(len(noisy_text)):
    reference = corrected_text[i]
    hypothesis = gemini[i]
    #hypothesis = tool.correct(noisy_text[i])
    error_WER_list.append(wer(reference, hypothesis))
    error_CER_list.append(cer(reference,hypothesis))

error_WER = np.mean(error_WER_list)
error_CER = np.mean(error_CER_list)

error_WER = round(error_WER*100, 4)
error_CER = round(error_CER*100,4)



print("WER:",error_WER,"%")
print("CER:",error_CER,"%")


