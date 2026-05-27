import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))                               #finds the project files

from classifier import classify_file, classify_folder
from unittest.mock import MagicMock
import unittest


class TestClassifyFile(unittest.TestCase):
    def make_mock_file(self, name, mtime=1700000000.0):
        mock=MagicMock()                                                            #creates a blank fake object taht we can change how we like to test with
        mock.name=name                                                              #takes full name of file      EX 'resume.pdf'
        mock.stem=Path(name).stem                                                   #takes the stem of file       EX 'resume'
        mock.suffix=Path(name).suffix                                               #takes suffix of fiile        EX '.pdf'
        mock.stat.return_value.st_mtime=mtime                                       #(mock.stat) a fake method returns (.return_value) and (.st_mtime=mtime) sets modified time
        return mock

    def test_pdf_goes_to_documents(self):                                           #Functions that test were a file goes
        f = self.make_mock_file('lecture_notes.pdf')                                #Makes the mock file and names it
        self.assertEqual(classify_file(f), 'Documents')                             #This is the actual test it call classify_file on the mock file and confirms the results match

    def test_image_goes_to_images(self):
        f = self.make_mock_file('photo.jpg')
        self.assertEqual(classify_file(f), 'Images')

    def test_exe_goes_to_apps(self):
        f = self.make_mock_file('setup.exe')
        self.assertEqual(classify_file(f), 'Apps')

    def test_resume_goes_to_career(self):
        f = self.make_mock_file('my_resume.pdf')
        self.assertEqual(classify_file(f), 'Career')

    def test_cover_letter_goes_to_career(self):
        f = self.make_mock_file('cover_letter.pdf')
        self.assertEqual(classify_file(f), 'Career')

    def test_tax_goes_to_finance(self):
        f = self.make_mock_file('tax_notification.pdf')
        self.assertEqual(classify_file(f), 'Finance')

    def test_immunization_goes_to_health(self):
        f = self.make_mock_file('immunization_record.pdf')
        self.assertEqual(classify_file(f), 'Health')

    def test_game_rar_goes_to_game_files(self):
        f = self.make_mock_file('elden_ring.rar')
        self.assertEqual(classify_file(f), 'Game Files')

    def test_desktop_ini_is_skipped(self):
        f = self.make_mock_file('desktop.ini')
        self.assertIsNone(classify_file(f))

    def test_unknown_file_goes_to_unsorted(self):
        f = self.make_mock_file('mystery_file.xyz')
        self.assertIn('Unsorted', classify_file(f))

    def test_matlab_goes_to_code(self):
        f = self.make_mock_file('matlab.m')
        self.assertEqual(classify_file(f), 'Code')
if __name__=='__main__':
    unittest.main()