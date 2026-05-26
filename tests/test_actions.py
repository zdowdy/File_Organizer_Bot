import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))                       #finds the project files

import unittest
from unittest.mock import MagicMock, patch
from actions import handle_conflict, organize_file

class TestHandleConflict(unittest.TestCase):
    def test_no_conflict(self):                                             #If destination doesnt exists return it unchanged
        mock_path=MagicMock()
        mock_path.exists.return_value=False
        mock_path.stem='resume'
        mock_path.suffix='.pdf'
        mock_path.parent=Path('Downloads/Career')
        result=handle_conflict(mock_path)
        self.assertEqual(result, mock_path)

    def test_one_conflict(self):                                            #If destination exists once return it with name(_2)
        parent=Path('Downloads/Career')
        original=parent/'resume.pdf'

        with patch.object(Path, 'exists', side_effect=[True, False]):       #replaces .exists() on all path objects with True the first time it is called the Flase the second
            result=handle_conflict(original)
            self.assertEqual(result.name, 'resume_2.pdf')
    
    def test_two_conflicts(self):                                           #If destination exists once return it with name(_3)
        parent=Path('Downloads/Career')                     
        original=parent/'resume.pdf'
                                                                            #issue with test never finishing using patch.object updated code
        call_count=0

        def fake_exists(self):
            nonlocal call_count
            call_count+=1
            return call_count<=2                                            #True for the first 2 calls

        with patch.object(Path, 'exists', fake_exists):
            result = handle_conflict(original)
            self.assertEqual(result.name, 'resume_3.pdf')

    
class TestOrganizeFile(unittest.TestCase):
#Important method for this section is patch:used in unit testing to temporaily replace real objects or functions with mock objects
    def make_mock_file(self,name):                                          #Creates mock file
        mock=MagicMock()
        mock.name=name
        mock.stem=Path(name).stem
        mock.suffix=Path(name).suffix
        mock.stat.return_value.st_mtime=1700000000.0
        return mock
    
    def test_dry_run_does_not_move(self):                                   #dry_run=True should never call shutil.move               
        f=self.make_mock_file('photo.jpg')

        with patch('actions.shutil.move') as mock_move:
            organize_file(f, 'C:/Users/ziero/Downloads', dry_run=True)
            mock_move.assert_not_called()

    def test_none_categiry_skips_file(self):                                #Test that desktop.ini never gets moved since it in SKIP_FILE
        f=self.make_mock_file('desktop.ini')

        with patch('actions.shutil.move') as mock_move:
            organize_file(f, 'C:/Users/ziero/Downloads', dry_run=False)
            mock_move.assert_not_called()

    def test_live_run_calls_move(self):                                     #Patches three things so they dont actually run shutil.move,Path.mkdir, and Path.exists confirms shutil.move was called only once
        f=self.make_mock_file('photo.jpg')

        with patch('actions.shutil.move') as mock_move:
            with patch('actions.Path.mkdir'):
                with patch('actions.Path.exists', return_value=False):
                    organize_file(f, 'C:/Users/ziero/Downloads', dry_run=False)
                    mock_move.assert_called_once()

if __name__ =='__main__':
    unittest.main()
