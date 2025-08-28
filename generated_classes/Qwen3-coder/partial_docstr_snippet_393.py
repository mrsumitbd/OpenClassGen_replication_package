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
        import numpy as np
        from scipy.sparse import csr_matrix
        
        # Get the original term-document matrix
        if non_text:
            orig_term_doc_mat = self.term_doc_matrix.get_metadata_term_doc_mat()
        else:
            orig_term_doc_mat = self.term_doc_matrix.get_term_doc_mat()
        
        # Convert doc_domains to numpy array
        doc_domains = np.array(doc_domains)
        
        # Get unique domains
        unique_domains = np.unique(doc_domains)
        
        # Create mapping from domain to column indices
        domain_to_indices = {}
        for domain in unique_domains:
            domain_to_indices[domain] = np.where(doc_domains == domain)[0]
        
        # Create new matrix by summing columns for each domain
        new_columns = []
        for domain in unique_domains:
            indices = domain_to_indices[domain]
            # Sum the columns corresponding to this domain
            domain_column = orig_term_doc_mat[:, indices].sum(axis=1)
            new_columns.append(domain_column)
        
        # Stack the columns to create the new matrix
        if new_columns:
            new_term_doc_mat = csr_matrix(np.hstack(new_columns))
        else:
            # If no columns, return empty matrix with appropriate shape
            new_term_doc_mat = csr_matrix((orig_term_doc_mat.shape[0], 0))
        
        return new_term_doc_mat