class CombineDocsIntoDomains(object):
    def __init__(self, term_doc_matrix):
        """
        Parameters
        ----------
        term_doc_matrix : TermDocMatrix
        """
        self.tdm = term_doc_matrix

    def get_new_term_doc_mat(self, doc_domains, non_text: bool = False):
        """
        Combines documents together that are in the same domain

        Parameters
        ----------
        doc_domains : array-like
        non_text: bool

        Returns
        -------
        scipy.sparse.csr_matrix
        """
        domains = np.array(doc_domains)
        unique_domains, inverse = np.unique(domains, return_inverse=True)

        if non_text:
            if not hasattr(self.tdm, 'non_text_mat'):
                raise AttributeError("TermDocMatrix has no attribute 'non_text_mat'")
            mat = self.tdm.non_text_mat
        else:
            if not hasattr(self.tdm, 'mat'):
                raise AttributeError("TermDocMatrix has no attribute 'mat'")
            mat = self.tdm.mat

        cols = []
        for i in range(len(unique_domains)):
            idx = np.where(inverse == i)[0]
            sub = mat[:, idx]
            # sum over the document axis (columns)
            summed = sub.sum(axis=1)
            arr = np.array(summed)
            col = csr_matrix(arr)
            cols.append(col)

        new_mat = hstack(cols, format='csr')
        return new_mat