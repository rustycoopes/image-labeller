import dropbox
import logging
class RussDropBox():

    def __init__(self, api_key, recurse = True, max_file_count = 10000000, batch_size = 10):
        self._recurse = recurse
        self._max_file_count = max_file_count
        self._api_key = api_key
        self._batch_size = batch_size

    def get_image_paths(self):
        dbx = dropbox.Dropbox(self._api_key)
        logging.info('calling into dropbox - recurse {}, max files {}, batch_size {}'.format(self._recurse, self._max_file_count, self._batch_size))
        response = dbx.files_list_folder('' , recursive=self._recurse, limit=self._batch_size,)

        totalfile_count = 0
        logging.info('Getting more files from dbx, current count {} - max set at {}'.format(totalfile_count, self._max_file_count))
        
        for entry in response.entries:
            if totalfile_count > self._max_file_count:
                logging.info('Max file count reached, exiting')
                return ''
            totalfile_count = totalfile_count + 1
            if self.is_image(entry.path_lower):
                logging.debug('yield file {}, current count {}'.format(entry.path_lower, totalfile_count))
                yield entry.path_lower


        while response.has_more:
            response = dbx.files_list_folder_continue(response.cursor )
            logging.info('Getting more files from dbx, current count {} - max set at {}'.format(totalfile_count, self._max_file_count))
            for entry in response.entries:
                if totalfile_count > self._max_file_count:
                    logging.info('Max file count reached, exiting')
                    return ''
                totalfile_count = totalfile_count + 1
                if self.is_image(entry.path_lower):
                    logging.debug('yield file {}, current count {}'.format(entry.path_lower, totalfile_count))
                    yield entry.path_lower

    def get_image(self, path):
        dbx = dropbox.Dropbox(self._api_key)
        file = dbx.files_download(path)
        return file[1].content

    def is_image(self, filepath):
        return filepath.endswith(".jpg")