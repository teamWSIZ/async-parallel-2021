"""
Dane w systemie galerii

Users
  userid
  name
  pass_sha256
  token
  active    # nieaktywny nie może się zalogować

Pictures
  pictureid
  data
  filename
  description
  creator_userid    #FK, kreator i właściciel obrazka - opcje "w" (zapisu/update/delete dla obrazka)
  created

Tags
  tagid
  tagname

PictureTag
  pictureid #FK
  tagid     #FK

dla kluczy obcych: https://www.sqlite.org/foreignkeys.html
cascade -- potencjalnie są!

"""
import datetime
from dataclasses import dataclass


@dataclass
class User:
    userid: int
    name: str
    pass_sha256: str
    token: str
    active: bool  # nieaktywny nie może się zalogować


@dataclass
class Pictures:
    pictureid: int
    data: bytes # pełny obrazek
    data_thumbnail: bytes
    filename: str
    description: str
    creator_userid: int  # kreator i właściciel obrazka - opcje "w" (zapisu/update/delete dla obrazka)
    created: datetime.datetime
    updated: datetime.datetime


@dataclass
class Tags:
    tagid: int
    tagname: str


@dataclass
class PictureTag:
    pictureid: int
    tagid: int  # pary (pictureid, tagid) powinny być unique, https://www.sqlitetutorial.net/sqlite-unique-constraint/
