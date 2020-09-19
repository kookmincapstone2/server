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
    "student_id": 20153159,
    "phone": "01012341234"
}
```

응답
```
{ }

200 ok
400 요청 형식 맞지 않음
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
    "name": "tester"
}

200 ok
400 요청 형식 맞지 않음
404 존재하지 않는 계정
```