#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from webapp2 import WSGIApplication, Route
from contollers import *


config = dict()
config['webapp2_extras.sessions'] = {
    'secret_key': '23940wetjq235213095wetgaseihtaewrtweq5rw1',
}

PAGE_RE = r'<link:/(?:[a-zA-Z0-9_-]+/?)*>'

app = WSGIApplication([
    Route(r'/login<:/?>', LoginPage),
    Route(r'/signup<:/?>', RegisterPage),
    Route(r'/logout<:/?>', Logout),
    Route(r'/_edit<:/?>' + PAGE_RE, EditPage),
    Route(r'/_history<:/?>' + PAGE_RE, HistoryPage),
    Route(r'/_delete<:/?>' + PAGE_RE, DeletePage),
    Route(r'/test_login', TestLogin),
    Route('' + PAGE_RE, PageContent)

], config=config, debug=True)
