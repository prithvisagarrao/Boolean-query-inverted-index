import sys
import operator

class Node:
    def __init__(self,data):
        self.item = data
        self.ref = None
        self.tf = 1

class LinkedList:
    def __init__(self):
        self.head = None

    def traverselist(self):
        arr = []
        if self.head is None:
            return
        else:
            n = self.head
            while n is not None:
                arr.append(n.item)

                n = n.ref
        return arr

    def insert(self,data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node

            return
        n = self.head
        while n.ref is not None:
            if n.item == new_node.item:
                n.tf +=1
                return
            n = n.ref
        if n.item == data:
            n.tf +=1
            return
        n.ref = new_node

    def count(self):
        if self.head is None:
            return 0
        count = 0
        n = self.head
        while n is not None:
            count = count +1
            n = n.ref
        return count

    def gettf(self,data):
        if self.head is None:
            return -1
        n = self.head
        while n is not None:
            if n.item == data:
                return n.tf
            n = n.ref





def get_postings_list(terms, inverted_index):
    # with open("input.txt", 'r') as ip:
    #     query_line = ip.readline()
    #     while query_line:
    #         terms = query_line.split()
    outstring = ""
    for term in terms:
        pl = inverted_index[term]
        #print("Get Postings")
        #print(term)
        pl_arr = pl.traverselist()
        #print("Postings list: "," ".join(pl_arr))
        outstring += "GetPostings\n%s\nPostings list: %s\n" %(term," ".join(pl_arr))
    return outstring
            #query_line = ip.readline()

def intersect(pl_1,pl_2):
    answer= LinkedList()
    list1 = pl_1.head
    list2 = pl_2.head
    count = 0
    while list1 is not None and list2 is not None:
        if list1.item == list2.item:
            answer.insert(list1.item)
            list1 = list1.ref
            list2 = list2.ref
            count+=1
        else:
            if list1.item < list2.item:
                list1 = list1.ref
                count += 1
            else:
                list2 = list2.ref
                count += 1
    return answer,count

def merge(pl_1,pl_2):
    answer = LinkedList()
    list1 = pl_1.head
    list2 = pl_2.head
    count = 0
    while list1 is not None and list2 is not None:
        if list1.item == list2.item:
            answer.insert(list1.item)
            list1 = list1.ref
            list2 = list2.ref
            count += 1
        else:
            if list1.item < list2.item:
                answer.insert(list1.item)
                list1 = list1.ref
                count += 1
            else:
                answer.insert(list2.item)
                list2 = list2.ref
                count += 1
    if list1 is not None:
        while list1 is not  None:
            answer.insert(list1.item)
            list1 = list1.ref

    elif list2 is not None:
        while list2 is not None:
            answer.insert(list2.item)
            list2 = list2.ref

    return answer, count

def and_query(terms,posting_list_array,document_frequency):

    comparisons = 0
    result = None


    if len(posting_list_array)>0:
        result,count = intersect(posting_list_array[0],posting_list_array[1])
        comparisons += count
    for i in range(2,len(posting_list_array)):
        result,count = intersect(result,posting_list_array[i])
        comparisons +=count

    score = {}
    no_of_docs = len(document_frequency)
    no_of_docs_with_term_t = 0



    daat_list = result.traverselist()
    if daat_list is not None:

        for daat in daat_list:
            tf = 0
            df = 0
            tfidf_daat = 0
            for pl in posting_list_array:
                tf = 0
                df = 0
                idf_term = 0
                tf_term = 0
                tfidf_term = 0
                tf_or = pl.gettf(daat)
                if tf_or is not None:
                    tf += tf_or

                t_appears_in_doc = tf
                no_of_terms_in_doc = document_frequency[daat]
                tf_term = t_appears_in_doc / no_of_terms_in_doc



                no_of_docs_with_term_t = pl.count()
                idf_term = no_of_docs / no_of_docs_with_term_t

                tfidf_term = tf_term * idf_term
                tfidf_daat+= tfidf_term



            df += document_frequency[daat]
            tf_score = tf / df
            idf = no_of_docs / no_of_docs_with_term_t
            score[daat] = tfidf_daat

    xx = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
    xxx = []


    for xi in xx:

        xxx.append(xi[0])


    # print("DaatAnd")
    # print(" ".join(terms))
    # print("Results: ", " ".join(daat_list) if daat_list is not None else None)
    # print("Number of documents in results: ", result.count())
    # print("Number of comparisons: ", comparisons)
    outstring = "DaatAnd\n%s\nResults: %s\nNumber of documents in results: %d\nNumber of comparisons: %d\nTF-IDF\nResults: %s\n" % (
    " ".join(terms), " ".join(daat_list) if daat_list is not None else "empty", result.count(), comparisons," ".join(xxx) if len(xxx) !=0 else "empty")
    return outstring


def or_query(terms,posting_list_array,document_frequency):

    comparisons = 0
    result = None

    if len(posting_list_array) > 0:
        result, count = merge(posting_list_array[0], posting_list_array[1])
        comparisons += count
    for i in range(2, len(posting_list_array)):
        result, count = merge(result, posting_list_array[i])
        comparisons += count


    score = {}
    no_of_docs = len(document_frequency)
    no_of_docs_with_term_t = 0


    daat_list = result.traverselist()
    if daat_list is not None:

        for daat in daat_list:
            tf = 0
            df = 0
            tfidf_daat = 0
            for pl in posting_list_array:
                tf = 0
                df = 0
                idf_term = 0
                tf_term = 0
                tfidf_term = 0
                tf_or = pl.gettf(daat)
                if tf_or is not None:
                    tf += tf_or

                t_appears_in_doc = tf
                no_of_terms_in_doc = document_frequency[daat]
                tf_term = t_appears_in_doc / no_of_terms_in_doc

                no_of_docs_with_term_t = pl.count()
                idf_term = no_of_docs / no_of_docs_with_term_t

                tfidf_term = tf_term * idf_term
                tfidf_daat += tfidf_term

            df += document_frequency[daat]
            tf_score = tf / df
            idf = no_of_docs / no_of_docs_with_term_t
            score[daat] = tfidf_daat

    xx = sorted(score.items(), key=operator.itemgetter(1), reverse=True)
    xxx = []
    for xi in xx:

        xxx.append(xi[0])


    # print("DaatOr")
    # print(" ".join(terms))
    # print("Results: ", " ".join(daat_list) if daat_list is not None else None)
    # print("Number of documents in results: ", result.count())
    # print("Number of comparisons: ", comparisons)
    outstring = "DaatOr\n%s\nResults: %s\nNumber of documents in results: %d\nNumber of comparisons: %d\nTF-IDF\nResults: %s\n\n" %(" ".join(terms)," ".join(daat_list) if daat_list is not None else "empty",result.count(),comparisons," ".join(xxx) if len(xxx) !=0  else "empty")
    return outstring



if __name__ == '__main__':

    sysargs = sys.argv
    data_path = sysargs[1]
    output_file = sysargs[2]
    inputfile = sysargs[3]
    document_frequency = {}

    inverted_index = {}
    #posting_list_array = []
    terms_list = []
    with open(data_path, 'r') as fp:
        line = fp.readline()
        while line:
            val = line.split("\t")
            if val[0]:
                docID = val[0]
            if val[1]:
                sentence = val[1]
            sentence_split = sentence.split()
            document_frequency[docID] = len(sentence_split)

            for term in sentence_split:

                if term in inverted_index:
                    posting_list = inverted_index[term]
                    posting_list.insert(docID)
                else:
                    new_list = LinkedList()
                    new_list.insert(docID)
                    inverted_index[term] = new_list

            line = fp.readline()

    # for key, value in inverted_index.items():
    #     gg = value.traverselist()
    #     print(key ,":", gg)

    with open(inputfile, 'r') as ip:
        with open(output_file, 'w') as op:
            query_line = ip.readline()
            while query_line:
                posting_list_array = []
                terms = query_line.split()

                outstring_getpostings = get_postings_list(terms, inverted_index)
                op.write(outstring_getpostings)
                for term in terms:
                    pl = inverted_index[term]
                    posting_list_array.append(pl)
                outstringand = and_query(terms,posting_list_array,document_frequency)
                outstringor = or_query(terms,posting_list_array,document_frequency)
                op.write(outstringand)
                op.write(outstringor)
                query_line = ip.readline()



# ll = LinkedList()
#
# ll.insert("sss")
# ll.insert(44)
# ll.insert(55)
#
# ll.traverselist()

