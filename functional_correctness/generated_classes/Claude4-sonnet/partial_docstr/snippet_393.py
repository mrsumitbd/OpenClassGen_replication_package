class CombineDocsIntoDomains(object):

    def __init__(self, term_doc_matrix):
        '''
        Parameters
        ----------
        term_doc_matrix : TermDocMatrix
        '''
        self.term_doc_matrix = term_doc_matrix

    def get_new_term_doc_mat(self, doc_domains, non_text: bool = False):
        '''
        Combines documents together that are in the same domain

        Parameters
        ----------
        doc_domains : array-like
        non_text: bool

        Returns
        -------
        scipy.sparse.csr_matrix
        '''
        if non_text:
            X = self.term_doc_matrix.get_metadata_doc_mat()
        else:
            X = self.term_doc_matrix.get_term_doc_mat()
        
        doc_domains = np.array(doc_domains)
        unique_domains = np.unique(doc_domains)
        
        combined_matrix = []
        for domain in unique_domains:
            domain_mask = doc_domains == domain
            domain_docs = X[:, domain_mask]
            combined_domain = domain_docs.sum(axis=1)
            combined_matrix.append(combined_domain)
        
        combined_matrix = sparse.hstack(combined_matrix)
        return combined_matrix.tocsr()