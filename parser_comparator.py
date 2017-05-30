# coding: utf-8

__author__ = "maobedkova"

import numpy

# path = 'C:/Users/Maria/OneDrive/HSE/Projects/Sketches/corpora/'

# conll_text = 'UD-all.conll'
# txt_text = 'raw_text.txt'
#
# golden_standard_file = 'UD-all.conll'
# udpipe_file = 'parsed_udpipe.conll'
# rusyntax_file = 'parsed_rusyntax.conll'
# syntaxnet_file = 'changed_syntaxnet.conll'


def form_dataset(input_file, output_file):
    """The function for writing a raw text from conll dataset"""
    print ('=== Text formation ===')
    with open(input_file, 'r', encoding='utf-8') as f:
        punct_mark = 0
        for line in f:
            if len(line) == 1:
                continue
            splitted = line.strip().split('\t')
            with open(output_file, 'a', encoding='utf-8') as w:
                # Every sentence from a new line
                if splitted[0] == '1':
                    if splitted[1] in '"(':
                        punct_mark = 1
                        w.write('\n' + splitted[1])
                    else:
                        w.write('\n' + splitted[1])
                else:
                    # Mind punctuation to form a text with right spaces
                    if splitted[1] in '")(':
                        if punct_mark == 2:
                            punct_mark = 0  # there is no opening punctuation
                            w.write(splitted[1])
                        elif punct_mark == 0:
                            punct_mark = 1  # there is an opening punctuation
                            w.write(' ' + splitted[1])
                    elif splitted[7] == 'punct':
                        w.write(splitted[1])
                    else:
                        if punct_mark == 1:
                            punct_mark = 2  # there are some words within punctuation marks
                            w.write(splitted[1])
                        else:
                            w.write(' ' + splitted[1])


def syntaxnet_debugger(input_file, output_file):
    """The function for debugging improper splitting for SyntaxNet"""
    f = open(input_file, 'r', encoding='utf-8')
    with open(output_file, 'w', encoding='utf-8') as w:
        mem_line = ''
        mark = 0
        for line in f:
            if len(line) == 1:
                mark += 1
                if mark > 3:
                    mem_line = ''
                    mark = 1
                else:
                    w.write(line)
            else:
                if line.split('\t')[0] == '1':
                    mark += 1
                    mem_line = line
                else:
                    if mark == 1 or mark == 2:
                        mark = 0
                        w.write(mem_line)
                        w.write(line)
                    elif mark == 0:
                        w.write(line)


def compare_parsers(golden_standard_file, udpipe_file)#, syntaxnet_file, rusyntax_file):
    '''The function for comparing different syntactic parsers'''

    def count_accuracy(gs_arr, sp_arr, true, false, accuracy, accuracy_rel):
        """The function for counting an accuracy score for every sentence and on the whole"""
        rel = 0
        rel_head = 0
        for i in range(0, len(gs_arr)):
            if gs_arr[i] == sp_arr[i]:
                true += 1
                rel += 1
                rel_head += 1
                if gs_arr[i] == '0' and sp_arr[i] == '0':
                    rel_head += 1
            else:
                false += 1
        accuracy_rel.append(float(rel_head) / (len(gs_arr) + 1))
        accuracy.append(float(rel) / len(gs_arr))
        return true, false, accuracy, accuracy_rel

    def find_equivalent_line(w, n, sp_line, gs_line, sp_arr, gs_arr, true, false, accuracy, accuracy_rel):
        """The function for finding equivalent lines in the golden standard and in a parser output"""
        gs_splitted = gs_line.strip().split('\t')
        sp_splitted = sp_line.strip().split('\t')
        if gs_splitted[1] == sp_splitted[1] and gs_splitted[0] == sp_splitted[0]:
            w.write ('GOT! ' + gs_splitted[1] + ' ' + sp_splitted[1] + '\n')
            gs_arr.append(gs_splitted[6])
            sp_arr.append(sp_splitted[6])
            n = 1
            mark = 1
        else:
            mark = 0
        return n, mark, gs_arr, sp_arr, true, false, accuracy, accuracy_rel

    def flow(parser_file):
        """The function for skipping not empty lines"""
        for line in parser_file:
            if len(line) == 1:
                break

    def iter_file(w, parser_file, n, mark, gs_line,
                  arr, gs_arr, true, false, accuracy, accuracy_rel):
        """The function for iterating a parser file"""
        if gs_line.split('\t')[0] == '1':
            if gs_arr != []:
                true, false, accuracy, accuracy_rel = count_accuracy(gs_arr, arr,
                                                                     true, false,
                                                                     accuracy, accuracy_rel)
                arr = []
                gs_arr = []
                w.write (str(true) + ' ' + str(false) + ' ' + str(accuracy) + '\n')
        for line in parser_file:
            if not line.startswith('#'):
                if not len(line) == 1:
                    if gs_line.split('\t')[0] == '1' and gs_line.split('\t')[1] != line.split('\t')[1]:
                        n = 1
                        mark = 0
                        continue
                    else:
                        w.write(line)
                        n, mark,\
                        gs_arr, arr, \
                        true, false, \
                        accuracy, accuracy_rel = \
                            find_equivalent_line(w, n,
                                                 line, gs_line,
                                                 arr, gs_arr,
                                                 true, false,
                                                 accuracy, accuracy_rel)
            if len(line) == 1 and len(gs_line) != 1:
                if gs_line.split('\t')[0] != '1':
                    arr = []
                    gs_arr = []
                    break
            if n == 1:
                n = 0
                break
        return n, mark, gs_arr, arr, true, false, accuracy, accuracy_rel

    # Different UDpipe scores
    ud_true = 0
    ud_false = 0
    ud_accuracy = []
    ud_accuracy_rel = []

    # Different SyntaxNet scores
    # sn_true = 0
    # sn_false = 0
    # sn_accuracy = []
    # sn_accuracy_rel = []

    # Different RuSyntax scores
    # rs_true = 0
    # rs_false = 0
    # rs_accuracy = []
    # rs_accuracy_rel = []

    # Golden standard, UDpipe, SyntaxNet and RuSyntax arrays
    gs_ud_arr = []
    # gs_sn_arr = []
    # gs_rs_arr = []
    ud_arr = []
    # sn_arr = []
    # rs_arr = []

    # Marking for match
    # rs_mark = 0
    # sn_mark = 0
    ud_mark = 0

    # Marking for skipping after match
    n = 0

    # Marking for skipping after mismatch
    quit_mark = 0

    # Opening parser`s files
    ud_file = open(udpipe_file,  'r', encoding='utf-8')
    # sn_file = open(syntaxnet_file,  'r', encoding='utf-8')
    # rs_file = open(rusyntax_file,  'r', encoding='utf-8')

    # Writing down the results
    with open('parsers_results.txt', 'w', encoding='utf-8') as w:
        # Opening the golden standard
        with open(golden_standard_file, 'r', encoding='utf-8') as gs_file:
            for gs_line in gs_file:
                if quit_mark == 1:
                    if len(gs_line) == 1:
                        if ud_mark == 1:
                            flow(ud_file)
                        # if sn_mark == 1:
                        #     flow(sn_file)
                        # if rs_mark == 1:
                        #     flow(rs_file)
                        # quit_mark = 0
                    continue
                if len(gs_line) == 1:
                    continue
                # w.write ('==NEW GS==' + gs_line)
                # Comparison of the golden standard with UDpipe
                # w.write('UD!')
                n, ud_mark, gs_ud_arr, ud_arr, ud_true, ud_false, ud_accuracy, ud_accuracy_rel = \
                    iter_file(w, ud_file, n, ud_mark, gs_line, ud_arr, gs_ud_arr,
                              ud_true, ud_false, ud_accuracy, ud_accuracy_rel)
                # Comparison of the golden standard with SyntaxNet
                # w.write ('SN!')
                # n, sn_mark, gs_sn_arr, sn_arr, sn_true, sn_false, sn_accuracy, sn_accuracy_rel = \
                #     iter_file(w, sn_file, n, sn_mark, gs_line, sn_arr, gs_sn_arr,
                #               sn_true, sn_false, sn_accuracy, sn_accuracy_rel)
                # # Comparison of the golden standard with RuSyntax
                # w.write ('RS!')
                # n, rs_mark, gs_rs_arr, rs_arr, rs_true, rs_false, rs_accuracy, rs_accuracy_rel = \
                #     iter_file(w, rs_file, n, rs_mark, gs_line, rs_arr, gs_rs_arr,
                #               rs_true, rs_false, rs_accuracy, rs_accuracy_rel)
                # If some of parsers have different tokenization examples are not considered
                # if (ud_mark + sn_mark + rs_mark) < 3:
                if ud_mark == 0:
                    gs_ud_arr = []
                    # gs_sn_arr = []
                    # gs_rs_arr = []
                    ud_arr = []
                    # sn_arr = []
                    # rs_arr = []
                    quit_mark = 1
                # if len(ud_accuracy) == 1200:
                #     break

        w.write('\nThe number of sentences processed: ' + str(len(ud_accuracy)) + '\n\n')

        # w.write('=== Accuracy for UDpipe ===\n')
        w.write('Accuracy for the whole text: ' + str(float(ud_true) / float(ud_true + ud_false)) + '\n')
        w.write('Mean accuracy for every sentence: ' + str(numpy.mean(ud_accuracy)) + '\n')
        w.write('Mean accuracy for every sentence with higher weight for root: ' + str(numpy.mean(ud_accuracy_rel)) + '\n\n')

        # w.write('=== Accuracy for SyntaxNet ===\n')
        # w.write('Accuracy for the whole text: ' + str(float(sn_true) / float(sn_true + sn_false)) + '\n')
        # w.write('Mean accuracy for every sentence: ' + str(numpy.mean(sn_accuracy)) + '\n')
        # w.write('Mean accuracy for every sentence with higher weight for root: ' + str(numpy.mean(sn_accuracy_rel)) + '\n\n')
        #
        # w.write('=== Accuracy for RuSyntax ===\n')
        # w.write('Accuracy for the whole text: ' + str(float(rs_true) / float(rs_true + rs_false)) + '\n')
        # w.write('Mean accuracy for every sentence: ' + str(numpy.mean(rs_accuracy)) + '\n')
        # w.write('Mean accuracy for every sentence with higher weight for root: ' + str(numpy.mean(rs_accuracy_rel)) + '\n')


if __name__ == '__main__':
    compare_parsers(golden_standard_file, udpipe_file)#, syntaxnet_file, rusyntax_file)