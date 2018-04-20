class FileUtils:
    @staticmethod
    def get_filename_from_path(path):
        return path.split('/')[-1]