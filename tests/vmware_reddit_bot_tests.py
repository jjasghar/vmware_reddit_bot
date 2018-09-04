"Test file for the VMware Reddit bot"
import os
import sys
import io
import unittest
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock

import vmware_reddit_bot as bot

class VMwareRedditBotTest(unittest.TestCase):
    "Tests for VMware Reddit bot"
    def setUp(self):
        "Test #bot_login"
        os.environ['CLIENT_ID'] = 'fake_client_id'
        os.environ['CLIENT_SECRET'] = 'fake_client_secret'
        os.environ['PASSWORD'] = 'fake_password'
        os.environ['REDDIT_USERNAME'] = 'fake_reddit_username'
        os.environ['SUBREDDITS'] = "test test2"

    @staticmethod
    def test_bot_login():
        "Test #bot_login"
        with patch('praw.Reddit') as mock_praw:
            bot.bot_login()
            agent = '<console:branding_bot:0.0.1 (by /u/fake_reddit_username)'
            mock_praw.assert_called_with(client_id='fake_client_id',
                                         client_secret='fake_client_secret',
                                         password='fake_password',
                                         user_agent=agent,
                                         username='branding_bot')
    @patch('time.sleep')
    def test_handle_rate_limit(self, mock_time):
        "Test #handle_rate_limit"
        output_capture = io.StringIO()
        sys.stdout = output_capture
        bot.handle_rate_limit('10 seconds')
        self.assertEqual(output_capture.getvalue(), '10 seconds\n')
        mock_time.assert_called_with(10)

        output_capture = io.StringIO()
        sys.stdout = output_capture
        bot.handle_rate_limit('10 minutes')
        self.assertEqual(output_capture.getvalue(), '10 minutes\n')
        mock_time.assert_called_with(600)

    @patch('builtins.open')
    def test_save_comment(self, mock_open):
        "Test #save_comment"
        mock_open.return_value = MagicMock()
        file_handle = mock_open.return_value.__enter__.return_value

        self.assertEqual(bot.save_comment(["one"], "two"), ["one", "two"])

        mock_open.assert_called_with("comments_replied_to.txt", "a")
        file_handle.write.assert_called_with("two\n")

    @patch('praw.Reddit')
    def test_check_comment(self, mock_praw):
        "Test #check_comment"

        # True if VMWare (and author is not bot and we have not replied already)
        mock_comment = MagicMock(body=" VMWare", id='1')
        mock_comment.author.name = 'user'
        self.assertTrue(bot.check_comment(mock_comment, mock_praw, []))

        # False if VMware
        mock_comment = MagicMock(body="VMware", id='1')
        mock_comment.author.name = 'user'
        self.assertFalse(bot.check_comment(mock_comment, mock_praw, []))

        # False if bot is comment author
        mock_comment = MagicMock(body="VMWare", id='1')
        mock_comment.author.name = 'bot'
        mock_praw.user.me.return_value.name = 'bot'
        self.assertFalse(bot.check_comment(mock_comment, mock_praw, []))

        # False if already replied
        mock_comment = MagicMock(body="VMWare", id='1')
        mock_comment.author.name = 'user'
        self.assertFalse(bot.check_comment(mock_comment, mock_praw, ['1']))

    @patch('builtins.open')
    @patch('os.path')
    def test_get_saved_comments(self, mock_path, mock_open):
        "Test #get_saved_comments"
        with self.assertRaisesRegex(RuntimeError, ".*Cannot find.*"):
            mock_path.isfile.return_value = False
            bot.get_saved_comments()

        mock_open.return_value = MagicMock()
        mock_path.isfile.return_value = True
        file_handle = mock_open.return_value.__enter__.return_value
        file_handle.read.return_value = "comment1\ncomment2"
        self.assertEqual(bot.get_saved_comments(), ['comment1', 'comment2'])


    # TODO: Write tests for #run_bot

if __name__ == '__main__':
    unittest.main()
