class AsynchronousResponseIterator:
    def __init__(self, response_buffer_manager):
        self.response_buffer_manager = response_buffer_manager
        self.current_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_index >= len(self.response_buffer_manager.buffer):
            if self.response_buffer_manager.is_complete:
                raise StopIteration
            else:
                self.response_buffer_manager.wait_for_data()
                if self.current_index >= len(self.response_buffer_manager.buffer):
                    raise StopIteration
        
        item = self.response_buffer_manager.buffer[self.current_index]
        self.current_index += 1
        return item

    @property
    def end_of_buffered(self):
        return self.current_index >= len(self.response_buffer_manager.buffer)