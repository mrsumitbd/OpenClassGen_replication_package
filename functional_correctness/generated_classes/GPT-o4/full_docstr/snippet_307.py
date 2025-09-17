class SubtitleFormatter(object):
    '''Base subtitle formatter class
    '''

    def format(self, subtitles):
        '''Turn a string containing the subs xml document into the formatted
        subtitle string

        @param str|crunchyroll.models.StyledSubtitle sub_xml_text
        @return str
        '''
        if isinstance(subtitles, StyledSubtitle):
            styled = subtitles
        elif isinstance(subtitles, str):
            styled = StyledSubtitle.from_string(subtitles)
        else:
            raise TypeError(
                "subtitles must be a StyledSubtitle or XML string"
            )
        return self._format(styled)

    def _format(self, styled_subtitle):
        '''Do the actual formatting on the parsed xml document, should be
        overridden by subclasses

        @param crunchyroll.models.StyledSubtitle styled_subtitle
        @return str
        '''
        raise NotImplementedError("Subclasses must implement _format()")