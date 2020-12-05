# flask를 이용한 REST API서버  
## 필요 패키지  
DB : PostgreSQL  
reference link - https://github.com/snowplow/snowplow/wiki/Setting-up-PostgreSQL
### 윈도우
```
https://www.postgresql.org/download/
다 next해서 설치
```
### 리눅스
```
$ sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs
```
```
user : postgres
pw : root
database name : test
port : 5432
```
## 필요한 모듈 설치  
### 윈도우
```
pip install -r requirments.txt  
```
## 개발서버 실행 방법
### 윈도우
```
set MODE=DEV
python manage.py
```
## API
### ping
/api/ping  
get: 서버 정상작동하는지 테스트
```
{}
```
200: ok
### test
/api/test
get, post, put, delete: 삽입한 데이터 확인하고 싶을 때 사용
```
{
    자유: 자유
}
```

### authorization
[GET] /api/authorization/email  
이메일 중복 검사

요청
```
{
    "email": "test@test.test"
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
409 이미 사용중인 이메일
```

[GET] /api/authorization/phone  
전화번호 중복 검사

요청
```
{
    "phone": "01012341234"
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
409 이미 사용중인 전화번호
```
[POST] /api/authorization/signup  
회원 가입

요청
```
{
    "email": "test@test.test",
    "pw": "test123!@#",
    "name": "tester",
    "student_id": "20153159",
    "phone": "01012341234",
    "rank": "teacher" or "student"
}
```

응답
```
{ }

200 ok
401 이미 존재하는 이메일 or 이미 존재하는 핸드폰번호
400 요청 형식 맞지 않음 or  teacher, student 중 하나가 아님
```

[POST] /api/authorization/login  
로그인

요청
```
{
    "email": "test@test.test",
    "pw": "test123!@#"
}
```

응답
```
{
    "id": 1,
    "name": "tester",
    "rank": "teacher"
}

200 ok
400 요청 형식 맞지 않음
404 존재하지 않는 계정
```

### room
[POST] /api/room/management  
방 생성

요청
```
{
    "user_id": 1,
    "title": "test_room_title",
    ("maximum_population": 60)
}
```

응답
```
{
    "room_id": 1,
    "master_id": 1,
    "title": "test_room_title",
    "maximum_population": 60,
    "invite_code": uuid
}

200 ok
400 요청 형식 맞지 않음
404 해당 유저 존재하지 않음
```

[GET] /api/room/management  
방 정보 받아오기

요청
```
{
    "room_id": 1,
}
```

응답
```
{
    "room_id": 1,
    "master_id": 1,
    "title": "test_title",
    "maximum_population": 30,
    "invite_code": uuid
}
```


[PUT] /api/room/management  
자신이 생성한 방 수정

요청
```
{
    "user_id": 1,
    "room_id": 1,
    "title": "modified_title",
    "maximum_population": "50"
}
```

응답
```
{
    "room_id": 1,
    "master_id": 1,
    "title": "modified_title",
    "maximum_population": 50,
    "invite_code": uuid
}

200 ok
400 요청 형식 맞지 않음
403 해당 유저가 해당 방의 마스가 아님
404 해당 유저 존재하지 않음 or 해당 방 존재하지 않음
```

[DELETE] /api/room/management  
자신이 생선한 방 제거

요청
```
{
    "user_id": 1,
    "room_id": 1
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
403 해당 유저가 해당 방의 마스터가 아님
404 해당 방이 존재하지 않음
```

[POST] /api/room/member/management  
방에 가입

요청
```
{
    "user_id": 1,
    "invite_code": uuid
}
```

응답
```
{
    "room_id": 1,
    "master_id": 1,
    "title": "test_title",
    "maximum_population": 50,
    "invite_code": uuid
}

200 ok
400 요청 형식 맞지 않음
404 해당 유저 존재하지 않음 or 존재하지 않는 초대 코드
409 이미 가입된 방 or 최대 가입 인원수 초과
```

[GET] /api/room/member/management  
가입된 방 모두 보기

요청
```
{
    "user_id": 1
}
```

응답
```
{
    "0": {
        "room_id": 1,
        "master_id": 1,
        "title": "test_title",
        "maximum_population": 30,
        "invite_code": uuid
    },
    "1": {...},
}

200 ok
400 요청 형식 맞지 않음
404 해당 유저 존재하지 않음 or 가입된 방이 없음
```

[DELETE] /api/room/member/management  
방 탈퇴

요청
```
{
    "user_id": 1,
    "room_id": 1,
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
404 해당 유저 존재하지 않음 or 해당 방 존재하지 않음 or 가입되지 않은 방
```

[POST] /api/room/attendance/check  
출석체크 생성 ( 선생용 )

요청
```
{
    "user_id": 1,
    "room_id": 1,
    "pass_num": "123445678"
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
403 방의 마스터가 아님
404 해당 유저 or 해당 방 존재하지 않음
```

[PUT] /api/room/attendance/check  
출석체크 ( 학생용 )

요청
```
{
    "user_id": 1,
    "room_id": 1,
    "pass_num": "12345678"
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
404 해당 유저 or 해당 방 or 해당 출석코드 존재하지 않음
```

[GET] /api/room/attendance/check  
출석체크 현황 확인

요청
```
{
    "user_id": 1,
    "room_id": 1
}
```

응답
```
{
    "checked": {
        1: {
            "user_id": 1,
            "name": "tester",
            "rank": "student"
        }, ...
    },
    "unchecked": {
        2: {
            "user_id": 2,
            "name": "tester2",
            "rank": "student"
        }, ...
    }
}
```

[GET] /api/room/member/all  
방에 가입된 모든 멤버를 보여줌

요청  
```
{
    "room_id": 1
}
```

응답  
```
{
    "User": {   1:  {
                    "user_id": 1,
                    "name": "tester",
                    "rank": "student"
                    "rate_info": {
                        "checke": 1,
                        "unchecked": 0,
                        "rate": 1.0,
                    }
                }, ...
        }
    }
}

200 ok
400 요청 형식 맞지 않음
404 해당 방 또는 해당 방에 가입된 멤버가 없음
```

[GET] /api/room/member/attendance/rate  
방 멤버들 출석률을 나타내는 함수

요청
```
{
    "room_id": 1
}
```

응답
```
{
    "1": {
        "checked": 1,
        "unchecked": 0,
        "rate": 1.0
    }, ...
}

200 ok
400 요청 형식 맞지 않음
404 해당 방에 가입된 멤버 없음
```

[GET] /api/room/attendance/check/all  
학생 한명의 출석체크 현황을 보여줌

요청
```
{
    "user_id": 1,
    "room_id": 1
}
```  

응답
```
{
    "Date": {2020-12-06": {
        'attendance_check_id': 1,
        'attendance_check_is_checked': True
    }, ...
    }
}

200 ok
400 요청 형식 맞지 않음
404 유저 또는 방 또는 출석체크가 존재하지 않음
```

[PUT] /api/room/attendance/check/close  
현재 유효한 출석체크를 무효하게 만듦

요청
```
{
    "user_id": 1,
    "room_id": 1
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
403 해당 유저가 방의 마스터가 아님
404 유저 또는 방 또는 유효한 출석체크가 존재하지 않음
```