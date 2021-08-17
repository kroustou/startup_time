#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from startup_time import startup_time

BASIC_FILE = [
    "Mar  2 09:00:00 nxengine NX[2335]: [Test|CallbackManager.cpp:102|0x59280b40] 1.5GB of virtual memory used",
    "Mar  2 10:32:58 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] starting nxengine 4.0.1.2 (x86) from [/usr/bin/nxengine]",
    "Mar  2 10:32:59 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] nxengine is running ",
]

UNEVEN_EVENTS = [
    "Mar  2 09:00:00 nxengine NX[2335]: [Test|CallbackManager.cpp:102|0x59280b40] 1.5GB of virtual memory used",
    "Mar  2 10:32:58 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] starting nxengine 4.0.1.2 (x86) from [/usr/bin/nxengine]",
    "Mar  2 10:32:59 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] nxengine is running ",
    "Mar  2 10:35:59 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] nxengine is running ",
]


START_AFTER_RUNNING_EVENTS = [
    "Mar  2 09:00:00 nxengine NX[2335]: [Test|CallbackManager.cpp:102|0x59280b40] 1.5GB of virtual memory used",
    "Mar  2 10:31:59 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] nxengine is running ",
    "Mar  2 10:32:58 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] starting nxengine 4.0.1.2 (x86) from [/usr/bin/nxengine]",
    "Mar  2 10:32:59 nxengine NX[1287]: [Test|NxEngineMain.cpp:122|0xb88ec60] nxengine is running ",
]


class TestStartupTime(unittest.TestCase):

    @patch('startup_time.open')
    def test_basic(self, m_open):
        m_open().__enter__().readlines.return_value = BASIC_FILE
        result = startup_time('nxengine', 'path')
        self.assertEqual(result[0].total_seconds(), 1)

    @patch('startup_time.open')
    def test_logfile_does_not_exist_handled(self, m_open):
        m_open.side_effect =  IOError("No such file")
        startup_time('nxengine', 'path')

    @patch('startup_time.open')
    def test_uneven_events(self, m_open):
        m_open().__enter__().readlines.return_value = UNEVEN_EVENTS
        result = startup_time('nxengine', 'path')
        self.assertEqual(result[0].total_seconds(), 1)

    @patch('startup_time.open')
    def test_start_after_running(self, m_open):
        m_open().__enter__().readlines.return_value = START_AFTER_RUNNING_EVENTS
        result = startup_time('nxengine', 'path')
        self.assertEqual(result[0].total_seconds(), 1)


if __name__ == "__main__":
    unittest.main()
